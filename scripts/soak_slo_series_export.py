#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
R = ROOT / 'research'


def load(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def main() -> int:
    status = load(R / 'openclaw-conformance-result.json')
    score = load(R / 'launch-scorecard-2026-03-24.json')
    controller = load(R / 'policy-slo-controller-report.json')

    out_jsonl = R / 'soak-48h-slo-series.export.jsonl'
    rows = [
        {
            'ts': datetime.now(timezone.utc).isoformat(),
            'metric': 'quarantine_rate',
            'value': (status.get('checks', {}).get('status_control_plane', {}).get('safety', {}) or {}).get('quarantine_rate'),
        },
        {
            'ts': datetime.now(timezone.utc).isoformat(),
            'metric': 'approval_latency_minutes_avg',
            'value': (status.get('checks', {}).get('status_control_plane', {}).get('latency', {}) or {}).get('approval_latency_minutes_avg'),
        },
        {
            'ts': datetime.now(timezone.utc).isoformat(),
            'metric': 'launch_go_nogo',
            'value': score.get('go_nogo'),
        },
        {
            'ts': datetime.now(timezone.utc).isoformat(),
            'metric': 'rollback_triggers',
            'value': controller.get('triggers', []),
        },
    ]
    with out_jsonl.open('w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    print(f'Wrote {out_jsonl}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
