#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT_DIR = ROOT / 'research'


def req(base: str, method: str, path: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode('utf-8')
    r = urllib.request.Request(base.rstrip('/') + path, data=data, method=method, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(r, timeout=30) as resp:
        raw = resp.read().decode('utf-8')
        return json.loads(raw) if raw else {}


def main() -> int:
    ap = argparse.ArgumentParser(description='Policy SLO controller with automatic rollback trigger')
    ap.add_argument('--base-url', default=os.getenv('BOTSTORE_API', 'http://127.0.0.1:8787'))
    ap.add_argument('--bundle-id', default='default')
    ap.add_argument('--tenant-id', default='default')
    ap.add_argument('--lookback-days', type=int, default=30)
    ap.add_argument('--quarantine-rate-max', type=float, default=0.30)
    ap.add_argument('--approval-latency-max-min', type=float, default=10.0)
    ap.add_argument('--deny-rate-max', type=float, default=0.70)
    ap.add_argument('--activation-failure-rate-max', type=float, default=0.20)
    ap.add_argument('--force-trigger', action='store_true', help='force rollback trigger (demo/testing)')
    ap.add_argument('--dry-run', action='store_true', help='evaluate only, do not rollback')
    args = ap.parse_args()

    ts = datetime.now(timezone.utc).isoformat()
    status = req(args.base_url, 'GET', f"/status/control-plane?{urllib.parse.urlencode({'tenant_id': args.tenant_id, 'lookback_days': args.lookback_days})}")
    dlog = req(args.base_url, 'GET', f"/policy/decision-log?{urllib.parse.urlencode({'tenant_id': args.tenant_id, 'limit': 500})}")

    rows = dlog.get('rows', []) if isinstance(dlog, dict) else []
    total = len(rows)
    deny = sum(1 for r in rows if str(r.get('effect', '')).lower() == 'deny')
    deny_rate = (deny / total) if total else 0.0

    safety = status.get('safety', {}) if isinstance(status, dict) else {}
    latency = status.get('latency', {}) if isinstance(status, dict) else {}

    quarantine_rate = float(safety.get('quarantine_rate', 0.0) or 0.0)
    approval_latency = latency.get('approval_latency_minutes_avg', None)
    approval_latency = None if approval_latency is None else float(approval_latency)

    # activation failure proxy: failed + rolled_back over total outcomes from status context if present
    total_outcomes = int(safety.get('total_outcomes', 0) or 0)
    # we currently approximate activation failure from deny and quarantine pressure in absence of explicit metric
    activation_failure_rate_proxy = max(0.0, min(1.0, quarantine_rate))

    triggers = []
    if quarantine_rate > args.quarantine_rate_max:
        triggers.append(f'quarantine_rate_spike:{quarantine_rate:.4f}>{args.quarantine_rate_max:.4f}')
    if approval_latency is not None and approval_latency > args.approval_latency_max_min:
        triggers.append(f'approval_latency_spike:{approval_latency:.3f}>{args.approval_latency_max_min:.3f}')
    if deny_rate > args.deny_rate_max:
        triggers.append(f'deny_rate_spike:{deny_rate:.4f}>{args.deny_rate_max:.4f}')
    if activation_failure_rate_proxy > args.activation_failure_rate_max:
        triggers.append(f'activation_failure_proxy_spike:{activation_failure_rate_proxy:.4f}>{args.activation_failure_rate_max:.4f}')
    if args.force_trigger:
        triggers.append('force_trigger')

    rollback_resp = None
    rolled_back = False
    if triggers and not args.dry_run:
        rollback_resp = req(args.base_url, 'POST', f"/policy/bundles/{args.bundle_id}/rollback", {})
        rolled_back = bool(rollback_resp.get('ok'))

    artifact = {
        'generated_at': ts,
        'base_url': args.base_url,
        'tenant_id': args.tenant_id,
        'bundle_id': args.bundle_id,
        'dry_run': args.dry_run,
        'thresholds': {
            'quarantine_rate_max': args.quarantine_rate_max,
            'approval_latency_max_min': args.approval_latency_max_min,
            'deny_rate_max': args.deny_rate_max,
            'activation_failure_rate_max': args.activation_failure_rate_max,
        },
        'observed': {
            'quarantine_rate': quarantine_rate,
            'approval_latency_minutes_avg': approval_latency,
            'deny_rate': deny_rate,
            'activation_failure_rate_proxy': activation_failure_rate_proxy,
            'decision_samples': total,
            'total_outcomes': total_outcomes,
        },
        'triggers': triggers,
        'rollback_invoked': bool(triggers) and not args.dry_run,
        'rollback_result_ok': rolled_back,
        'rollback_response': rollback_resp,
    }

    out_json = OUT_DIR / 'policy-slo-controller-report.json'
    out_md = OUT_DIR / 'policy-slo-controller-report.md'
    out_json.write_text(json.dumps(artifact, indent=2))
    out_md.write_text('\n'.join([
        '# Policy SLO Controller Report',
        '',
        f"- Generated: {ts}",
        f"- Bundle: {args.bundle_id}",
        f"- Dry run: {args.dry_run}",
        f"- Triggers: {', '.join(triggers) if triggers else 'none'}",
        f"- Rollback invoked: {artifact['rollback_invoked']}",
        f"- Rollback ok: {rolled_back}",
    ]) + '\n')

    print(f'Wrote {out_json}')
    print(f'Wrote {out_md}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
