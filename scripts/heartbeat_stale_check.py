#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

HB = Path('/Users/claw/.openclaw/workspace/botstore/research/heartbeat.json')
MAX_AGE_MIN = 20


def main() -> int:
    if not HB.exists():
        raise SystemExit('stale: missing heartbeat.json')
    data = json.loads(HB.read_text())
    ts = data.get('generated_at')
    if not ts:
        raise SystemExit('stale: missing generated_at')
    t = datetime.fromisoformat(ts.replace('Z', '+00:00'))
    age = datetime.now(timezone.utc) - t
    if age > timedelta(minutes=MAX_AGE_MIN):
        raise SystemExit(f'stale: heartbeat age {age} > {MAX_AGE_MIN}m')
    print('ok: heartbeat fresh')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
