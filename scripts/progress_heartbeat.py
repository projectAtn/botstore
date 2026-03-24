#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT = ROOT / 'research' / 'heartbeat.json'


def latest_commit() -> str:
    try:
        out = subprocess.check_output(['git', '-C', '/Users/claw/.openclaw/workspace', 'log', '--oneline', '-n', '1', '--', 'botstore'], text=True)
        return out.strip()
    except Exception:
        return 'unknown'


def main() -> int:
    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'phase': 'next-cycle (A/B/C/D hardening)',
        'latest_botstore_commit': latest_commit(),
        'status': 'active',
    }
    OUT.write_text(json.dumps(payload, indent=2))
    print(f'Wrote {OUT}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
