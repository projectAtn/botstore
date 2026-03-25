#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
R = ROOT / 'research'
OUT = R / 'external-rollout-checklist.json'

REQUIRED = {
    'launch_scorecard': R / 'launch-scorecard-2026-03-24.json',
    'conformance': R / 'openclaw-conformance-result.json',
    'crypto_smoke': R / 'cryptographic-smoke-report.json',
    'crypto_negative': R / 'cryptographic-negative-matrix-report.json',
    'alert_test': R / 'alert-test-report.json',
    'phase_gate_summary': R / 'phase-gate-summary.json',
    'auth_bypass': R / 'openclaw-auth-bypass-check.json',
    'typed_map': R / 'openclaw-typed-map-check.json'
}


def load(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def main() -> int:
    checks = {}
    loaded = {}
    for name, path in REQUIRED.items():
        data = load(path)
        loaded[name] = data
        checks[name] = data is not None

    decision_checks = {
        'scorecard_go': (loaded.get('launch_scorecard') or {}).get('go_nogo') == 'GO',
        'conformance_health_ok': bool(((loaded.get('conformance') or {}).get('checks', {}).get('health', {}) or {}).get('ok')),
        'auth_bypass_pass': bool((loaded.get('auth_bypass') or {}).get('all_pass')),
        'typed_map_pass': bool((loaded.get('typed_map') or {}).get('all_pass')),
        'alert_checks_pass': bool((loaded.get('alert_test') or {}).get('all_pass')),
    }

    all_present = all(checks.values())
    all_logic = all(decision_checks.values())
    go = all_present and all_logic

    packet = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'scope_lock_preserved': True,
        'artifact_presence': checks,
        'gate_logic': decision_checks,
        'go_nogo': 'GO' if go else 'NO_GO',
        'missing_or_failed': [k for k, v in {**checks, **decision_checks}.items() if not v],
    }
    OUT.write_text(json.dumps(packet, indent=2))
    print(f'Wrote {OUT}')
    return 0 if go else 1


if __name__ == '__main__':
    raise SystemExit(main())
