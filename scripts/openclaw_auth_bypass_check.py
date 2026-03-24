#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT_JSON = ROOT / 'research' / 'openclaw-auth-bypass-check.json'
OUT_MD = ROOT / 'research' / 'openclaw-auth-bypass-check.md'

import sys
sys.path.insert(0, str(ROOT / 'plugin' / 'python'))
from adapters.openclaw_adapter import OpenClawAdapter  # type: ignore


def main() -> int:
    rows = []

    # 1) Sensitive actions must be explicitly mapped
    sensitive = ['message.send', 'email.send', 'social.post', 'files.delete', 'payment.charge']
    for key in sensitive:
        m = OpenClawAdapter.action_scope_map(key)
        ok = m.get('requested_scope') == key and m.get('action_class') == key and m.get('requested_scope') != 'unknown'
        rows.append({'check': f'explicit_sensitive_map:{key}', 'pass': ok, 'mapping': m})

    # 2) Generic execution paths must not infer sensitive scopes
    generic = ['exec', 'browser.act']
    for key in generic:
        m = OpenClawAdapter.action_scope_map(key)
        inferred_sensitive = m.get('requested_scope') in set(sensitive)
        ok = not inferred_sensitive
        rows.append({'check': f'no_sensitive_inference:{key}', 'pass': ok, 'mapping': m})

    # 3) Unknown key must remain unknown (fail closed expectation upstream)
    m = OpenClawAdapter.action_scope_map('totally.unknown.tool')
    ok = m.get('requested_scope') == 'unknown'
    rows.append({'check': 'unknown_tool_maps_unknown', 'pass': ok, 'mapping': m})

    all_pass = all(r['pass'] for r in rows)
    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'all_pass': all_pass,
        'rows': rows,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2))
    OUT_MD.write_text('\n'.join([
        '# OpenClaw Auth Bypass Check',
        '',
        f"- Generated: {payload['generated_at']}",
        f"- All pass: {all_pass}",
        '',
        '## Checks',
        *[f"- {r['check']}: {'PASS' if r['pass'] else 'FAIL'}" for r in rows]
    ]) + '\n')
    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0 if all_pass else 1


if __name__ == '__main__':
    raise SystemExit(main())
