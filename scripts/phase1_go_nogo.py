#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path


def _num(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True, help="glob for conformance result json files")
    ap.add_argument("--out-json", default="research/qa-loop/openclaw-burnin/summary.json")
    ap.add_argument("--out-md", default="research/qa-loop/openclaw-burnin/summary.md")
    args = ap.parse_args()

    paths = sorted(glob.glob(args.glob))
    if not paths:
        raise SystemExit("no input files")

    tcrr_vals = []
    quarantine_vals = []
    approval_latency_vals = []
    all_ok = True

    for p in paths:
        data = json.loads(Path(p).read_text())
        checks = data.get("checks", {})
        health_ok = bool((checks.get("health") or {}).get("ok"))
        dlog_ok = bool((checks.get("policy_decision_log") or {}).get("ok"))
        all_ok = all_ok and health_ok and dlog_ok

        status = checks.get("status_control_plane", {})
        tcrr_vals.append(_num((status.get("north_star") or {}).get("trusted_capability_resolution_rate")))
        quarantine_vals.append(_num((status.get("safety") or {}).get("quarantine_rate")))

        lat = (status.get("latency") or {}).get("approval_latency_minutes_avg")
        if lat is not None:
            approval_latency_vals.append(_num(lat))

    runs = len(paths)
    summary = {
        "runs": runs,
        "all_health_and_policylog_ok": all_ok,
        "tcrr": {
            "min": min(tcrr_vals),
            "avg": sum(tcrr_vals) / max(len(tcrr_vals), 1),
            "max": max(tcrr_vals),
        },
        "quarantine_rate": {
            "min": min(quarantine_vals),
            "avg": sum(quarantine_vals) / max(len(quarantine_vals), 1),
            "max": max(quarantine_vals),
        },
        "approval_latency_minutes_avg": {
            "samples": len(approval_latency_vals),
            "avg": (sum(approval_latency_vals) / len(approval_latency_vals)) if approval_latency_vals else None,
        },
        "thresholds": {
            "all_ok_required": True,
            "quarantine_rate_max": 0.30,
            "approval_latency_minutes_avg_max": 10.0,
        },
    }

    go = summary["all_health_and_policylog_ok"]
    if summary["quarantine_rate"]["max"] > summary["thresholds"]["quarantine_rate_max"]:
        go = False
    avg_lat = summary["approval_latency_minutes_avg"]["avg"]
    if avg_lat is not None and avg_lat > summary["thresholds"]["approval_latency_minutes_avg_max"]:
        go = False

    summary["go_nogo"] = "GO" if go else "NO_GO"

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(summary, indent=2))

    out_md = Path(args.out_md)
    out_md.write_text(
        "\n".join(
            [
                "# OpenClaw Phase-1 Burn-in Summary",
                "",
                f"- Runs: {runs}",
                f"- Health + policy log all ok: {summary['all_health_and_policylog_ok']}",
                f"- TCRR avg: {summary['tcrr']['avg']:.4f}",
                f"- Quarantine rate max: {summary['quarantine_rate']['max']:.4f}",
                f"- Approval latency avg (min): {summary['approval_latency_minutes_avg']['avg']}",
                "",
                f"## Verdict: **{summary['go_nogo']}**",
                "",
                "Thresholds:",
                f"- quarantine_rate_max <= {summary['thresholds']['quarantine_rate_max']}",
                f"- approval_latency_minutes_avg_max <= {summary['thresholds']['approval_latency_minutes_avg_max']}",
            ]
        )
        + "\n"
    )

    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
