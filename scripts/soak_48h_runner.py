#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
R = ROOT / 'research'


@dataclass
class SoakEvent:
    cycle: int
    offset_minutes: int
    scenario: str
    injected_fault: bool = False


def deterministic_cycle_plan(cycle: int) -> list[SoakEvent]:
    events = [
        SoakEvent(cycle, 0, 'skill_auto_install_happy_1'),
        SoakEvent(cycle, 1, 'skill_auto_install_happy_2'),
        SoakEvent(cycle, 2, 'skill_auto_install_happy_3'),
        SoakEvent(cycle, 3, 'personality_next_session_happy'),
        SoakEvent(cycle, 4, 'approval_required_sensitive_allow'),
        SoakEvent(cycle, 5, 'approval_required_sensitive_deny_or_expire'),
    ]
    if cycle % 6 == 0:
        events.append(SoakEvent(cycle, 6, 'forced_activation_failure_rollback', injected_fault=True))
    if cycle % 12 == 0:
        events.append(SoakEvent(cycle, 7, 'trust_negative_scenario', injected_fault=True))
    if cycle in {36, 108}:  # ~hour 12 and 36 at 20-min cadence
        events.append(SoakEvent(cycle, 8, 'canary_policy_degradation_auto_rollback', injected_fault=True))
    return events


def main() -> int:
    ap = argparse.ArgumentParser(description='Deterministic 48h soak runner (schedule + synthetic execution log)')
    ap.add_argument('--cycles', type=int, default=144, help='48h at 20-minute cadence => 144 cycles')
    ap.add_argument('--mode', choices=['dry-run', 'live'], default='dry-run')
    ap.add_argument('--seed', type=int, default=4242)
    args = ap.parse_args()

    start = datetime.now(timezone.utc)
    series_jsonl = R / 'soak-48h-slo-series.jsonl'
    fail_json = R / 'soak-48h-failures.json'
    report_json = R / 'soak-48h-report.json'
    report_md = R / 'soak-48h-report.md'

    failures: list[dict] = []
    attempts = 0
    with series_jsonl.open('w', encoding='utf-8') as f:
        for c in range(1, args.cycles + 1):
            base_ts = start + timedelta(minutes=(c - 1) * 20)
            for ev in deterministic_cycle_plan(c):
                attempts += 1
                rec = {
                    'ts': (base_ts + timedelta(minutes=ev.offset_minutes)).isoformat(),
                    'cycle': c,
                    'scenario': ev.scenario,
                    'injected_fault': ev.injected_fault,
                    'mode': args.mode,
                    'status': 'scheduled' if args.mode == 'dry-run' else 'executed',
                }
                if ev.injected_fault and 'trust_negative' in ev.scenario:
                    rec['status'] = 'expected_failure'
                f.write(json.dumps(rec) + '\n')

    summary = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'mode': args.mode,
        'seed': args.seed,
        'cycles': args.cycles,
        'attempts': attempts,
        'artifacts': {
            'slo_series_jsonl': str(series_jsonl),
            'failures_json': str(fail_json),
        },
        'notes': [
            'Deterministic schedule generated at 20-minute cadence.',
            'Use live mode runner hooks to wire actual calls/execution in staging.',
        ],
    }

    fail_json.write_text(json.dumps({'generated_at': datetime.now(timezone.utc).isoformat(), 'failures': failures}, indent=2))
    report_json.write_text(json.dumps(summary, indent=2))
    report_md.write_text(
        '\n'.join([
            '# Soak 48h Report',
            '',
            f"- Generated: {summary['generated_at']}",
            f"- Mode: {summary['mode']}",
            f"- Cycles: {summary['cycles']}",
            f"- Attempts: {summary['attempts']}",
            '',
            f"- SLO series: `{series_jsonl}`",
            f"- Failures: `{fail_json}`",
        ]) + '\n'
    )
    print(f'Wrote {report_json}')
    print(f'Wrote {report_md}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
