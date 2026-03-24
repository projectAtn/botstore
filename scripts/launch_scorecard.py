#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
R = ROOT / 'research'
OUT_JSON = R / 'launch-scorecard-2026-03-24.json'
OUT_MD = R / 'launch-scorecard-2026-03-24.md'


def load_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return default if default is not None else {}


def main() -> int:
    conformance = load_json(R / 'openclaw-conformance-result.json', {})
    trust_smoke = load_json(R / 'trust-chain-smoke-result.json', {})
    trust_neg = load_json(R / 'trust-chain-negative-matrix-result.json', {})
    policy_fixture = load_json(R / 'policy-fixture-report.json', {})
    runtime2 = load_json(R / 'runtime2-certification-python-hostbot.json', {})

    checks = {
        'openclaw_conformance_ok': bool((conformance.get('checks', {}).get('health', {}) or {}).get('ok')),
        'typed_action_map_ok': bool((conformance.get('checks', {}).get('typed_action_map', {}) or {}).get('all_pass')),
        'auth_bypass_check_ok': bool((conformance.get('checks', {}).get('auth_bypass_check', {}) or {}).get('all_pass')),
        'trust_smoke_happy_path_ok': bool((trust_smoke.get('verify_local', {}) or {}).get('ok')) and bool((trust_smoke.get('positive_after_verify', {}) or {}).get('ok')),
        'trust_negative_matrix_ok': bool(trust_neg.get('all_pass')),
        'policy_fixtures_ok': bool(policy_fixture.get('all_pass')),
        'runtime2_l2_ok': bool((runtime2.get('runtime', {}) or {}).get('all_pass')),
    }

    pass_count = sum(1 for v in checks.values() if v)
    total = len(checks)
    go = pass_count == total

    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'checks': checks,
        'pass_count': pass_count,
        'total': total,
        'go_nogo': 'GO' if go else 'NO_GO',
        'notes': [
            'Scope lock preserved: OpenClaw reference runtime primary; runtime2 at lower trust level.',
            'No autonomous gateway/native-plugin install path introduced.',
            'Sensitive action mapping + auth-bypass checks included in conformance.',
        ],
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2))
    OUT_MD.write_text(
        '\n'.join([
            '# Launch Scorecard (2026-03-24)',
            '',
            f"- Generated: {payload['generated_at']}",
            f"- Result: **{payload['go_nogo']}** ({pass_count}/{total})",
            '',
            '## Checks',
            *[f"- {k}: {'PASS' if v else 'FAIL'}" for k, v in checks.items()],
            '',
            '## Notes',
            *[f"- {n}" for n in payload['notes']],
        ]) + '\n'
    )
    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0 if go else 1


if __name__ == '__main__':
    raise SystemExit(main())
