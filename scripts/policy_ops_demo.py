#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = os.getenv("BOTSTORE_API", "http://127.0.0.1:8787").rstrip("/")
ROOT = Path("/Users/claw/.openclaw/workspace/botstore")
OUT_JSON = ROOT / "research" / "policy-ops-demo-result.json"
OUT_MD = ROOT / "research" / "policy-ops-demo-report.md"


def req(method: str, path: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def post(path: str, payload: dict) -> dict:
    return req("POST", path, payload)


def main() -> int:
    ts = str(time.time_ns())
    bundle_id = f"ops-pilot-{ts}"

    baseline = post(
        "/policy/bundles",
        {
            "bundle_id": bundle_id,
            "version": "1.0.0",
            "spec": {
                "rules": [
                    {
                        "rule_id": "sensitive_send_requires_approval",
                        "action_in": ["install", "invoke"],
                        "scope_intersects": ["message.send", "email.send"],
                        "min_verification_tier": "tier1_signed",
                        "runtime_band_max": "B",
                        "effect": "allow_with_approval",
                        "require_approval": True,
                    }
                ]
            },
            "activate": True,
            "lifecycle_state": "active",
        },
    )

    candidate = post(
        "/policy/bundles",
        {
            "bundle_id": bundle_id,
            "version": "1.1.0",
            "spec": {
                "rules": [
                    {
                        "rule_id": "sensitive_send_requires_approval",
                        "action_in": ["install", "invoke"],
                        "scope_intersects": ["message.send", "email.send"],
                        "min_verification_tier": "tier1_signed",
                        "runtime_band_max": "B",
                        "effect": "allow_with_approval",
                        "require_approval": True,
                    },
                    {
                        "rule_id": "dangerous_delete_denied",
                        "action_in": ["install", "invoke"],
                        "scope_intersects": ["files.delete"],
                        "runtime_band_max": "B",
                        "effect": "deny",
                        "require_approval": False,
                    },
                ]
            },
            "activate": False,
            "lifecycle_state": "draft",
        },
    )

    tested = post(f"/policy/bundles/{candidate['id']}/transition", {"to_state": "tested", "activate": False})
    shadow = post(f"/policy/bundles/{candidate['id']}/transition", {"to_state": "shadow", "activate": False})

    replay = post(
        "/policy/replay-diff",
        {
            "candidate_bundle_row_id": candidate["id"],
            "baseline_bundle_row_id": baseline["id"],
            "sample_limit": 100,
        },
    )

    canary = post(f"/policy/bundles/{candidate['id']}/transition", {"to_state": "canary", "activate": False})
    activated = post(f"/policy/bundles/{candidate['id']}/transition", {"to_state": "active", "activate": True})
    rollback = post(f"/policy/bundles/{bundle_id}/rollback", {})

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": BASE,
        "bundle_id": bundle_id,
        "baseline": baseline,
        "candidate": candidate,
        "transitions": {
            "tested": tested,
            "shadow": shadow,
            "canary": canary,
            "activated": activated,
        },
        "replay_diff": {
            "sampled": replay.get("sampled"),
            "deltas": replay.get("deltas"),
        },
        "rollback": rollback,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2))
    OUT_MD.write_text(
        "\n".join([
            "# Policy Ops Demo Report",
            "",
            f"- Generated: {payload['generated_at']}",
            f"- Bundle: {bundle_id}",
            f"- Replay sampled: {replay.get('sampled')}",
            f"- Replay deltas: {replay.get('deltas')}",
            f"- Rollback: {rollback}",
        ])
        + "\n"
    )
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
