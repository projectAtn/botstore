#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT_ROOT_DEFAULT = ROOT / 'research' / 'soak-48h'
DEFAULT_DURATION_HOURS = 48
DEFAULT_CYCLE_MINUTES = 20
DEFAULT_SEED = 'soak-48h-v1'

# Required deterministic scenario mix across the full run.
# Counts are computed exactly for the requested cycle count using largest remainder.
SCENARIO_WEIGHTS = {
    'steady_state': 0.50,
    'policy_pressure': 0.20,
    'trust_path': 0.15,
    'monitoring_probe': 0.10,
    'rollback_drill': 0.05,
}


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def parse_start(raw: str | None) -> datetime:
    if not raw:
        return utcnow()
    value = raw.strip().replace('Z', '+00:00')
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def seed_to_int(seed: str) -> int:
    digest = hashlib.sha256(seed.encode('utf-8')).digest()
    return int.from_bytes(digest[:8], 'big')


def compute_cycle_count(duration_hours: int, cycle_minutes: int, max_cycles: int | None) -> int:
    if duration_hours <= 0:
        raise ValueError('duration-hours must be > 0')
    if cycle_minutes <= 0:
        raise ValueError('cycle-minutes must be > 0')
    total = (duration_hours * 60) // cycle_minutes
    if total <= 0:
        raise ValueError('computed cycle count is zero; increase duration or decrease cycle-minutes')
    if max_cycles is not None:
        if max_cycles <= 0:
            raise ValueError('max-cycles must be > 0')
        total = min(total, max_cycles)
    return total


def compute_required_mix(total_cycles: int) -> dict[str, int]:
    exact = {name: weight * total_cycles for name, weight in SCENARIO_WEIGHTS.items()}
    base = {name: int(value) for name, value in exact.items()}
    assigned = sum(base.values())
    remainders = sorted(
        ((exact[name] - base[name], name) for name in SCENARIO_WEIGHTS),
        key=lambda item: (-item[0], item[1]),
    )
    idx = 0
    while assigned < total_cycles:
        _, name = remainders[idx % len(remainders)]
        base[name] += 1
        assigned += 1
        idx += 1
    return base


def scenario_commands(scenario: str, python_bin: str, base_url: str, tenant_id: str, bundle_id: str, dry_run_policy: bool) -> list[list[str]]:
    common = [python_bin]
    if scenario == 'steady_state':
        return [
            common + ['scripts/progress_heartbeat.py'],
            common + ['scripts/phase_gate_summary.py'],
            common + ['scripts/heartbeat_stale_check.py'],
        ]
    if scenario == 'policy_pressure':
        cmd = common + [
            'scripts/policy_slo_controller.py',
            '--base-url',
            base_url,
            '--tenant-id',
            tenant_id,
            '--bundle-id',
            bundle_id,
        ]
        if dry_run_policy:
            cmd.append('--dry-run')
        return [cmd, common + ['scripts/phase_gate_summary.py']]
    if scenario == 'trust_path':
        return [
            common + ['scripts/trust_chain_smoke.py'],
            common + ['scripts/trust_crypto_smoke.py'],
        ]
    if scenario == 'monitoring_probe':
        return [
            common + ['scripts/monitoring_alert_test.py'],
            common + ['scripts/launch_scorecard.py'],
        ]
    if scenario == 'rollback_drill':
        cmd = common + [
            'scripts/policy_slo_controller.py',
            '--base-url',
            base_url,
            '--tenant-id',
            tenant_id,
            '--bundle-id',
            bundle_id,
            '--force-trigger',
        ]
        if dry_run_policy:
            cmd.append('--dry-run')
        return [cmd]
    raise ValueError(f'unknown scenario: {scenario}')


def build_sequence(total_cycles: int, seed: str, required_mix: dict[str, int]) -> list[str]:
    pool: list[str] = []
    for name in SCENARIO_WEIGHTS:
        pool.extend([name] * required_mix[name])
    rng = random.Random(seed_to_int(seed))
    rng.shuffle(pool)
    return pool


def run_command(cmd: list[str], cwd: Path, env: dict[str, str]) -> dict:
    started = utcnow()
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, env=env)
    ended = utcnow()
    return {
        'cmd': cmd,
        'returncode': proc.returncode,
        'started_at': started.isoformat(),
        'ended_at': ended.isoformat(),
        'duration_sec': round((ended - started).total_seconds(), 3),
        'stdout_tail': proc.stdout[-2000:] if proc.stdout else '',
        'stderr_tail': proc.stderr[-2000:] if proc.stderr else '',
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n')


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(row, separators=(',', ':')) + '\n')


def main() -> int:
    ap = argparse.ArgumentParser(description='Deterministic 48h soak runner with fixed 20-minute cycle scheduler')
    ap.add_argument('--mode', choices=['dry-run', 'live'], default='dry-run')
    ap.add_argument('--start-at', help='ISO8601 UTC timestamp; default now')
    ap.add_argument('--duration-hours', type=int, default=DEFAULT_DURATION_HOURS)
    ap.add_argument('--cycle-minutes', type=int, default=DEFAULT_CYCLE_MINUTES)
    ap.add_argument('--max-cycles', type=int, help='cap cycle count (useful for rehearsal)')
    ap.add_argument('--seed', default=DEFAULT_SEED)
    ap.add_argument('--base-url', default='http://127.0.0.1:8787')
    ap.add_argument('--tenant-id', default='default')
    ap.add_argument('--bundle-id', default='default')
    ap.add_argument('--out-root', default=str(OUT_ROOT_DEFAULT))
    ap.add_argument('--run-id', help='optional stable run id')
    ap.add_argument('--dry-run-policy-rollback', action='store_true', help='keep policy rollback commands in dry-run even during live soak')
    ap.add_argument('--stop-on-command-failure', action='store_true')
    args = ap.parse_args()

    start_at = parse_start(args.start_at)
    total_cycles = compute_cycle_count(args.duration_hours, args.cycle_minutes, args.max_cycles)
    required_mix = compute_required_mix(total_cycles)
    sequence = build_sequence(total_cycles, args.seed, required_mix)

    run_id = args.run_id or f"soak48h-{start_at.strftime('%Y%m%dT%H%M%SZ')}-{args.seed}"
    out_dir = Path(args.out_root) / run_id
    cycles_jsonl = out_dir / 'cycles.jsonl'
    failures_json = out_dir / 'failures.json'
    summary_json = out_dir / 'summary.json'
    schedule_json = out_dir / 'schedule.json'
    manifest_json = out_dir / 'manifest.json'

    manifest = {
        'run_id': run_id,
        'generated_at': utcnow().isoformat(),
        'mode': args.mode,
        'start_at': start_at.isoformat(),
        'duration_hours': args.duration_hours,
        'cycle_minutes': args.cycle_minutes,
        'total_cycles': total_cycles,
        'seed': args.seed,
        'base_url': args.base_url,
        'tenant_id': args.tenant_id,
        'bundle_id': args.bundle_id,
        'required_mix': required_mix,
        'scenario_weights': SCENARIO_WEIGHTS,
    }
    write_json(manifest_json, manifest)

    schedule_rows = []
    for idx, scenario in enumerate(sequence, start=1):
        due = start_at + timedelta(minutes=args.cycle_minutes * (idx - 1))
        commands = scenario_commands(
            scenario=scenario,
            python_bin=sys.executable,
            base_url=args.base_url,
            tenant_id=args.tenant_id,
            bundle_id=args.bundle_id,
            dry_run_policy=args.dry_run_policy_rollback,
        )
        schedule_rows.append(
            {
                'cycle_index': idx,
                'scenario': scenario,
                'scheduled_at': due.isoformat(),
                'commands': commands,
            }
        )
    write_json(schedule_json, {'run_id': run_id, 'cycles': schedule_rows})

    if args.mode == 'dry-run':
        summary = {
            'run_id': run_id,
            'mode': 'dry-run',
            'generated_at': utcnow().isoformat(),
            'planned_cycles': total_cycles,
            'planned_mix': dict(Counter(sequence)),
            'required_mix': required_mix,
            'status': 'planned',
            'artifacts': {
                'manifest': str(manifest_json.relative_to(ROOT)),
                'schedule': str(schedule_json.relative_to(ROOT)),
            },
        }
        write_json(summary_json, summary)
        print(f'Wrote {manifest_json}')
        print(f'Wrote {schedule_json}')
        print(f'Wrote {summary_json}')
        return 0

    env = os.environ.copy()
    env.update({'BOTSTORE_API': args.base_url})

    failure_rows: list[dict] = []
    observed = Counter()
    cycle_ok = 0
    cycle_failed = 0

    live_started = utcnow()
    for row in schedule_rows:
        due = datetime.fromisoformat(row['scheduled_at'])
        wait_s = (due - utcnow()).total_seconds()
        if wait_s > 0:
            time.sleep(wait_s)

        cycle_started = utcnow()
        command_results = []
        cycle_failed_here = False
        for cmd in row['commands']:
            result = run_command(cmd=cmd, cwd=ROOT, env=env)
            command_results.append(result)
            if result['returncode'] != 0:
                cycle_failed_here = True
                failure_rows.append(
                    {
                        'cycle_index': row['cycle_index'],
                        'scenario': row['scenario'],
                        'scheduled_at': row['scheduled_at'],
                        'command': cmd,
                        'returncode': result['returncode'],
                        'stderr_tail': result['stderr_tail'],
                    }
                )
                if args.stop_on_command_failure:
                    break

        cycle_ended = utcnow()
        observed[row['scenario']] += 1
        if cycle_failed_here:
            cycle_failed += 1
        else:
            cycle_ok += 1

        cycle_record = {
            'run_id': run_id,
            'cycle_index': row['cycle_index'],
            'scenario': row['scenario'],
            'scheduled_at': row['scheduled_at'],
            'started_at': cycle_started.isoformat(),
            'ended_at': cycle_ended.isoformat(),
            'cycle_duration_sec': round((cycle_ended - cycle_started).total_seconds(), 3),
            'ok': not cycle_failed_here,
            'commands': command_results,
        }
        append_jsonl(cycles_jsonl, cycle_record)

        if cycle_failed_here and args.stop_on_command_failure:
            break

    live_ended = utcnow()
    summary = {
        'run_id': run_id,
        'mode': 'live',
        'started_at': live_started.isoformat(),
        'ended_at': live_ended.isoformat(),
        'duration_sec': round((live_ended - live_started).total_seconds(), 3),
        'planned_cycles': total_cycles,
        'executed_cycles': cycle_ok + cycle_failed,
        'cycle_ok': cycle_ok,
        'cycle_failed': cycle_failed,
        'required_mix': required_mix,
        'observed_mix': dict(observed),
        'mix_matches_plan': dict(observed) == required_mix,
        'failure_count': len(failure_rows),
        'artifacts': {
            'manifest': str(manifest_json.relative_to(ROOT)),
            'schedule': str(schedule_json.relative_to(ROOT)),
            'cycles_jsonl': str(cycles_jsonl.relative_to(ROOT)),
            'failures': str(failures_json.relative_to(ROOT)),
        },
    }

    write_json(failures_json, {'run_id': run_id, 'failures': failure_rows})
    write_json(summary_json, summary)
    print(f'Wrote {cycles_jsonl}')
    print(f'Wrote {failures_json}')
    print(f'Wrote {summary_json}')

    return 0 if cycle_failed == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
