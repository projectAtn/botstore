#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
R = ROOT / 'research'
OUT_JSON = R / 'phase-gate-summary.json'
OUT_MD = R / 'phase-gate-summary.md'


def load(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def main() -> int:
    score = load(R / 'launch-scorecard-2026-03-24.json')
    conformance = load(R / 'openclaw-conformance-result.json')
    trust_smoke = load(R / 'cryptographic-smoke-report.json')
    trust_neg = load(R / 'cryptographic-negative-matrix-report.json')
    heartbeat = load(R / 'heartbeat.json')

    summary = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'go_nogo': score.get('go_nogo', 'UNKNOWN'),
        'checks': {
            'scorecard_present': bool(score),
            'conformance_present': bool(conformance),
            'crypto_smoke_present': bool(trust_smoke),
            'crypto_negative_present': bool(trust_neg),
            'heartbeat_present': bool(heartbeat),
        },
        'latest_heartbeat_at': heartbeat.get('generated_at'),
    }
    summary['all_pass'] = all(summary['checks'].values())

    OUT_JSON.write_text(json.dumps(summary, indent=2))
    OUT_MD.write_text('\n'.join([
        '# Phase Gate Summary',
        '',
        f"- Generated: {summary['generated_at']}",
        f"- GO/NO_GO: {summary['go_nogo']}",
        f"- All required artifacts present: {summary['all_pass']}",
    ]) + '\n')

    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
