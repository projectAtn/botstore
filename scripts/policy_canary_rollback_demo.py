#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT_JSON = ROOT / 'research' / 'canary-rollback-demo-result.json'
OUT_MD = ROOT / 'research' / 'canary-rollback-demo-report.md'


def req(base: str, method: str, path: str, payload: dict) -> dict:
    r = urllib.request.Request(base.rstrip('/') + path, data=json.dumps(payload).encode('utf-8'), method=method, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(r, timeout=30) as resp:
        raw = resp.read().decode('utf-8')
        return json.loads(raw) if raw else {}


def main() -> int:
    base = os.getenv('BOTSTORE_API', 'http://127.0.0.1:8787')
    ts = str(time.time_ns())
    bundle_id = f'rollback-demo-{ts}'

    baseline = req(base, 'POST', '/policy/bundles', {
        'bundle_id': bundle_id,
        'version': '1.0.0',
        'spec': {'rules': []},
        'activate': True,
        'lifecycle_state': 'active'
    })

    candidate = req(base, 'POST', '/policy/bundles', {
        'bundle_id': bundle_id,
        'version': '1.1.0',
        'spec': {'rules': [{'rule_id': 'strict-deny', 'action_in': ['install'], 'scope_intersects': ['log.read'], 'effect': 'deny'}]},
        'activate': False,
        'lifecycle_state': 'draft'
    })

    req(base, 'POST', f"/policy/bundles/{candidate['id']}/transition", {'to_state': 'tested', 'activate': False})
    req(base, 'POST', f"/policy/bundles/{candidate['id']}/transition", {'to_state': 'shadow', 'activate': False})
    req(base, 'POST', f"/policy/bundles/{candidate['id']}/transition", {'to_state': 'canary', 'activate': False})
    activated = req(base, 'POST', f"/policy/bundles/{candidate['id']}/transition", {'to_state': 'active', 'activate': True})

    # force-trigger rollback via controller
    cmd = [
        'python3', str(ROOT / 'scripts' / 'policy_slo_controller.py'),
        '--base-url', base,
        '--bundle-id', bundle_id,
        '--tenant-id', 'default',
        '--force-trigger'
    ]
    subprocess.run(cmd, check=True)

    report = json.loads((ROOT / 'research' / 'policy-slo-controller-report.json').read_text())

    result = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'base_url': base,
        'bundle_id': bundle_id,
        'baseline_bundle_row_id': baseline.get('id'),
        'candidate_bundle_row_id': candidate.get('id'),
        'activated_bundle_row_id': activated.get('id'),
        'controller_report': report,
        'rollback_ok': bool(report.get('rollback_result_ok')),
    }

    OUT_JSON.write_text(json.dumps(result, indent=2))
    OUT_MD.write_text('\n'.join([
        '# Canary Rollback Demo Report',
        '',
        f"- Generated: {result['generated_at']}",
        f"- Bundle ID: {bundle_id}",
        f"- Rollback OK: {result['rollback_ok']}",
        f"- Trigger list: {', '.join(report.get('triggers', []))}",
    ]) + '\n')
    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0 if result['rollback_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
