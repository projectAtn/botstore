#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
RESEARCH = ROOT / 'research'
DEFAULT_OUT_DIR = RESEARCH / 'soak-48h'


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def point(ts: str | None, source: str, metric: str, value: float | int | bool | str) -> dict:
    return {
        'ts': ts,
        'source': source,
        'metric': metric,
        'value': value,
    }


def collect_policy_slo(path: Path, rows: list[dict]) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        return
    ts = data.get('generated_at')
    src = str(path.relative_to(ROOT))
    observed = data.get('observed') or {}
    rows.extend(
        [
            point(ts, src, 'policy.quarantine_rate', float(observed.get('quarantine_rate', 0.0) or 0.0)),
            point(ts, src, 'policy.approval_latency_minutes_avg', float(observed.get('approval_latency_minutes_avg', 0.0) or 0.0)),
            point(ts, src, 'policy.deny_rate', float(observed.get('deny_rate', 0.0) or 0.0)),
            point(ts, src, 'policy.activation_failure_rate_proxy', float(observed.get('activation_failure_rate_proxy', 0.0) or 0.0)),
            point(ts, src, 'policy.rollback_invoked', bool(data.get('rollback_invoked'))),
            point(ts, src, 'policy.rollback_result_ok', bool(data.get('rollback_result_ok'))),
            point(ts, src, 'policy.trigger_count', len(data.get('triggers') or [])),
        ]
    )


def collect_alert(path: Path, rows: list[dict]) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        return
    ts = data.get('generated_at')
    checks = data.get('checks') or {}
    passes = sum(1 for v in checks.values() if bool(v))
    total = len(checks)
    src = str(path.relative_to(ROOT))
    rows.extend(
        [
            point(ts, src, 'alert.all_pass', bool(data.get('all_pass'))),
            point(ts, src, 'alert.pass_count', passes),
            point(ts, src, 'alert.total_checks', total),
            point(ts, src, 'alert.pass_ratio', (passes / total) if total else 0.0),
        ]
    )


def collect_launch(path: Path, rows: list[dict]) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        return
    ts = data.get('generated_at')
    src = str(path.relative_to(ROOT))
    passes = int(data.get('pass_count', 0) or 0)
    total = int(data.get('total', 0) or 0)
    go = str(data.get('go_nogo', 'UNKNOWN')).upper() == 'GO'
    rows.extend(
        [
            point(ts, src, 'launch.pass_count', passes),
            point(ts, src, 'launch.total_checks', total),
            point(ts, src, 'launch.pass_ratio', (passes / total) if total else 0.0),
            point(ts, src, 'launch.go', go),
        ]
    )


def collect_phase_gate(path: Path, rows: list[dict]) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        return
    ts = data.get('generated_at')
    checks = data.get('checks') or {}
    passes = sum(1 for v in checks.values() if bool(v))
    total = len(checks)
    src = str(path.relative_to(ROOT))
    rows.extend(
        [
            point(ts, src, 'phase_gate.all_pass', bool(data.get('all_pass'))),
            point(ts, src, 'phase_gate.pass_count', passes),
            point(ts, src, 'phase_gate.total_checks', total),
            point(ts, src, 'phase_gate.pass_ratio', (passes / total) if total else 0.0),
            point(ts, src, 'phase_gate.go', str(data.get('go_nogo', 'UNKNOWN')).upper() == 'GO'),
        ]
    )


def collect_soak_summaries(rows: list[dict]) -> None:
    for summary_path in sorted((DEFAULT_OUT_DIR).glob('soak48h-*/summary.json')):
        data = load_json(summary_path)
        if not isinstance(data, dict):
            continue
        ts = data.get('ended_at') or data.get('generated_at') or data.get('started_at')
        src = str(summary_path.relative_to(ROOT))
        rows.extend(
            [
                point(ts, src, 'soak.executed_cycles', int(data.get('executed_cycles', 0) or 0)),
                point(ts, src, 'soak.cycle_ok', int(data.get('cycle_ok', 0) or 0)),
                point(ts, src, 'soak.cycle_failed', int(data.get('cycle_failed', 0) or 0)),
                point(ts, src, 'soak.failure_count', int(data.get('failure_count', 0) or 0)),
                point(ts, src, 'soak.mix_matches_plan', bool(data.get('mix_matches_plan'))),
            ]
        )


def parse_ts(value: str | None) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)


def summarize(rows: list[dict]) -> dict:
    numeric = defaultdict(list)
    latest_by_metric = {}

    for r in rows:
        key = r['metric']
        ts = parse_ts(r.get('ts'))
        prev = latest_by_metric.get(key)
        if prev is None or ts >= parse_ts(prev.get('ts')):
            latest_by_metric[key] = {'ts': r.get('ts'), 'value': r.get('value'), 'source': r.get('source')}
        if isinstance(r.get('value'), (int, float)):
            numeric[key].append(float(r['value']))

    stats = {}
    for key, vals in numeric.items():
        if not vals:
            continue
        stats[key] = {
            'count': len(vals),
            'min': min(vals),
            'max': max(vals),
            'avg': sum(vals) / len(vals),
        }

    return {
        'generated_at': utcnow(),
        'points': len(rows),
        'metrics': len({r['metric'] for r in rows}),
        'sources': sorted({r['source'] for r in rows}),
        'latest_by_metric': latest_by_metric,
        'numeric_stats': stats,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description='Export SLO metric time-series JSONL/summary from existing reports')
    ap.add_argument('--out-dir', default=str(DEFAULT_OUT_DIR))
    ap.add_argument('--jsonl-name', default='slo-series.jsonl')
    ap.add_argument('--summary-name', default='slo-series-summary.json')
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_jsonl = out_dir / args.jsonl_name
    out_summary = out_dir / args.summary_name

    rows: list[dict] = []

    for path in sorted(RESEARCH.glob('policy-slo-controller-report*.json')):
        collect_policy_slo(path, rows)
    for path in sorted(RESEARCH.glob('alert-test-report*.json')):
        collect_alert(path, rows)
    for path in sorted(RESEARCH.glob('launch-scorecard-*.json')):
        collect_launch(path, rows)
    for path in sorted(RESEARCH.glob('phase-gate-summary*.json')):
        collect_phase_gate(path, rows)
    collect_soak_summaries(rows)

    rows.sort(key=lambda r: (parse_ts(r.get('ts')), r['source'], r['metric']))

    with out_jsonl.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, separators=(',', ':')) + '\n')

    summary = summarize(rows)
    out_summary.write_text(json.dumps(summary, indent=2) + '\n')

    print(f'Wrote {out_jsonl}')
    print(f'Wrote {out_summary}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
