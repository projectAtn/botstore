#!/usr/bin/env python3
"""Validate Phase-1 exit criteria from conformance artifacts.

Usage:
  python3 scripts/phase1_exit_check.py \
    --input research/openclaw-conformance-result.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="research/openclaw-conformance-result.json")
    args = ap.parse_args()

    path = Path(args.input)
    if not path.exists():
        _fail(f"missing artifact: {path}")

    payload = json.loads(path.read_text())
    checks = payload.get("checks", {})

    health = checks.get("health", {})
    if not health.get("ok"):
        _fail("health.ok is not true")

    status = checks.get("status_control_plane", {})
    north = status.get("north_star", {})
    safety = status.get("safety", {})
    latency = status.get("latency", {})

    if "trusted_capability_resolution_rate" not in north:
        _fail("missing TCRR in status_control_plane.north_star")
    if "quarantine_rate" not in safety:
        _fail("missing quarantine_rate in status_control_plane.safety")
    if "approval_latency_minutes_avg" not in latency:
        _fail("missing approval_latency_minutes_avg in status_control_plane.latency")

    dlog = checks.get("policy_decision_log", {})
    if dlog.get("ok") is not True:
        _fail("policy_decision_log.ok is not true")

    profile = checks.get("tenant_profile", {})
    if not profile.get("tenant_id"):
        _fail("tenant policy profile missing tenant_id")

    typed = checks.get("typed_action_map", {})
    if typed.get("all_pass") is not True:
        _fail("typed_action_map.all_pass is not true")

    bypass = checks.get("auth_bypass_check", {})
    if bypass.get("all_pass") is not True:
        _fail("auth_bypass_check.all_pass is not true")

    summary = {
        "ok": True,
        "artifact": str(path),
        "tenant_id": payload.get("tenant_id"),
        "tcrr": north.get("trusted_capability_resolution_rate"),
        "quarantine_rate": safety.get("quarantine_rate"),
        "approval_latency_minutes_avg": latency.get("approval_latency_minutes_avg"),
        "policy_decision_count": dlog.get("count"),
        "tenant_profile": {
            "profile_name": profile.get("profile_name"),
            "runtime_band_max_autonomous": profile.get("runtime_band_max_autonomous"),
        },
    }

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
