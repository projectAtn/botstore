#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT_JSON = ROOT / 'research' / 'alert-test-report.json'
OUT_MD = ROOT / 'research' / 'alert-test-report.md'
BASE = 'http://127.0.0.1:8787'


def get(path: str) -> dict:
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def main() -> int:
    status = get('/status/control-plane?tenant_id=default&lookback_days=30')
    conformance = load(ROOT / 'research' / 'openclaw-conformance-result.json')
    typed = load(ROOT / 'research' / 'openclaw-typed-map-check.json')
    bypass = load(ROOT / 'research' / 'openclaw-auth-bypass-check.json')

    checks = {
        'status_endpoint_available': bool(status.get('ok')),
        'quarantine_rate_present': 'quarantine_rate' in (status.get('safety') or {}),
        'approval_latency_present': 'approval_latency_minutes_avg' in (status.get('latency') or {}),
        'typed_map_signal_present': 'all_pass' in typed,
        'auth_bypass_signal_present': 'all_pass' in bypass,
        'conformance_report_present': bool(conformance),
    }

    all_pass = all(checks.values())
    out = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'all_pass': all_pass,
        'checks': checks,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2))
    OUT_MD.write_text('\n'.join([
        '# Alert Test Report',
        '',
        f"- Generated: {out['generated_at']}",
        f"- All pass: {all_pass}",
        '',
        '## Checks',
        *[f"- {k}: {'PASS' if v else 'FAIL'}" for k, v in checks.items()]
    ]) + '\n')
    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0 if all_pass else 1


if __name__ == '__main__':
    raise SystemExit(main())
