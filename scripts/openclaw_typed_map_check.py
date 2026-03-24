#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT_JSON = ROOT / 'research' / 'openclaw-typed-map-check.json'
OUT_MD = ROOT / 'research' / 'openclaw-typed-map-check.md'

# Import adapter map
import sys
sys.path.insert(0, str(ROOT / 'plugin' / 'python'))
from adapters.openclaw_adapter import OpenClawAdapter  # type: ignore


def main() -> int:
    required_sensitive = [
        'message.send',
        'email.send',
        'social.post',
        'files.delete',
        'payment.charge',
    ]

    rows = []
    all_pass = True
    for key in required_sensitive:
        v = OpenClawAdapter.action_scope_map(key)
        ok = bool(v) and v.get('requested_scope') == key and v.get('action_class') == key and v.get('requested_scope') != 'unknown'
        rows.append({
            'key': key,
            'mapping': v,
            'pass': ok,
        })
        all_pass = all_pass and ok

    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'all_pass': all_pass,
        'required_sensitive': required_sensitive,
        'rows': rows,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2))
    OUT_MD.write_text(
        '\n'.join([
            '# OpenClaw Typed Action Map Check',
            '',
            f"- Generated: {payload['generated_at']}",
            f"- All pass: {all_pass}",
            '',
            '## Required sensitive keys',
        ] + [f"- {r['key']}: {'PASS' if r['pass'] else 'FAIL'}" for r in rows]) + '\n'
    )

    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0 if all_pass else 1


if __name__ == '__main__':
    raise SystemExit(main())
