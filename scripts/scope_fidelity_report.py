#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
DB = ROOT / 'api' / 'botstore.db'
OUT_JSON = ROOT / 'research' / 'scope-fidelity-report.json'
OUT_MD = ROOT / 'research' / 'scope-fidelity-report.md'


def main() -> int:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    aa = conn.execute('SELECT requested_scope, decision FROM actionauthorization').fetchall()
    outcomes = conn.execute('SELECT observed_scopes_json, incident_flag FROM outcomereport').fetchall()

    total_auth = len(aa)
    unknown_scope = sum(1 for r in aa if (r['requested_scope'] or '').strip().lower() in {'', 'unknown'})
    denied = sum(1 for r in aa if (r['decision'] or '').strip().lower() == 'deny')

    total_out = len(outcomes)
    observed_nonempty = 0
    incident_with_observed = 0
    for r in outcomes:
        scopes = []
        try:
            scopes = json.loads(r['observed_scopes_json'] or '[]')
        except Exception:
            scopes = []
        if isinstance(scopes, list) and len(scopes) > 0:
            observed_nonempty += 1
            if bool(r['incident_flag']):
                incident_with_observed += 1

    report = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'action_authorization': {
            'total': total_auth,
            'unknown_scope_count': unknown_scope,
            'unknown_scope_rate': (unknown_scope / total_auth) if total_auth else 0.0,
            'denied_count': denied,
        },
        'outcome_scope_fidelity': {
            'total_outcomes': total_out,
            'observed_nonempty_count': observed_nonempty,
            'observed_nonempty_rate': (observed_nonempty / total_out) if total_out else 0.0,
            'incident_with_observed_count': incident_with_observed,
        },
        'pilot_gate': {
            'unknown_scope_rate_max': 0.0,
            'observed_nonempty_rate_min': 0.95,
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2))

    md = [
        '# Scope Fidelity Report',
        '',
        f"- Generated: {report['generated_at']}",
        '',
        '## Action authorization',
        f"- total: {total_auth}",
        f"- unknown scope count: {unknown_scope}",
        f"- unknown scope rate: {report['action_authorization']['unknown_scope_rate']:.4f}",
        f"- denied count: {denied}",
        '',
        '## Outcome scope fidelity',
        f"- total outcomes: {total_out}",
        f"- observed non-empty count: {observed_nonempty}",
        f"- observed non-empty rate: {report['outcome_scope_fidelity']['observed_nonempty_rate']:.4f}",
        f"- incident with observed count: {incident_with_observed}",
    ]
    OUT_MD.write_text('\n'.join(md) + '\n')
    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
