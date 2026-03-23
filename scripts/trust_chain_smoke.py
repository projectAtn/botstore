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
OUT_JSON = ROOT / "research" / "trust-chain-smoke-result.json"
OUT_MD = ROOT / "research" / "trust-chain-smoke-report.md"


def post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def put(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode("utf-8"),
        method="PUT",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def must(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(msg)


def main() -> int:
    ts = str(time.time_ns())
    slug = f"trust-smoke-{ts}"

    creator = post("/creators", {"name": f"Trust Smoke {ts}", "verification": "verified", "trust_score": 0.9})
    pack = post(
        "/packs",
        {
            "slug": slug,
            "title": "Trust Smoke Pack",
            "type": "skill",
            "version": "1.0.0",
            "description": "Trust chain smoke",
            "risk_level": "medium",
            "scopes": ["log.read", "message.send"],
            "creator_id": creator["id"],
        },
    )
    version = post(
        f"/packs/{pack['id']}/versions",
        {
            "semver": "1.0.1",
            "manifest_version": "v2",
            "capabilities_declared": ["deploy.rollback"],
            "scopes_requested": ["log.read", "message.send"],
            "actions_supported": ["deploy.rollback", "message.send"],
            "compatible_runtimes": ["openclaw"],
            "policy_requirements": {"runtime_band_max": "B"},
            "verification_tier": "tier2_verified",
        },
    )

    negative = post(
        "/agent/install-by-capability-v2",
        {
            "task_id": f"trust-neg-{ts}",
            "tenant_id": "default",
            "user_id": "telegram:trust-smoke",
            "agent_id": "agent-trust-smoke",
            "runtime_id": "openclaw",
            "runtime_version": "0.2.0",
            "runtime_band": "B",
            "required_capabilities": ["deploy.rollback"],
        },
    )
    must(negative.get("ok") is False, "negative trust gate should fail closed before verification")

    trust = put(
        f"/packs/{pack['id']}/versions/{version['id']}/trust",
        {
            "artifact_uri": f"oci://botstore/{slug}:1.0.1",
            "signature_refs": [f"sig://local/{slug}"],
            "sbom_ref": f"sbom://local/{slug}.spdx.json",
            "attestation_refs": [f"att://build/{slug}", f"att://qa/{slug}", f"att://prov/{slug}"],
        },
    )
    verify = post(f"/packs/{pack['id']}/versions/{version['id']}/trust/verify-local", {})
    must(bool(verify.get("ok")), "verify-local should pass after trust evidence upsert")

    positive = post(
        "/agent/install-by-capability-v2",
        {
            "task_id": f"trust-pos-{ts}",
            "tenant_id": "default",
            "user_id": "telegram:trust-smoke",
            "agent_id": "agent-trust-smoke",
            "runtime_id": "openclaw",
            "runtime_version": "0.2.0",
            "runtime_band": "B",
            "required_capabilities": ["deploy.rollback"],
        },
    )
    must(bool(positive.get("ok")), "positive install should pass after trust verification")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": BASE,
        "pack_id": pack["id"],
        "pack_version_id": version["id"],
        "negative_before_verify": negative,
        "trust_upsert": trust,
        "verify_local": verify,
        "positive_after_verify": positive,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2))
    OUT_MD.write_text(
        "\n".join(
            [
                "# Trust Chain Smoke Report",
                "",
                f"- Generated: {payload['generated_at']}",
                f"- Base URL: {BASE}",
                f"- Pack: {pack['id']} version {version['id']}",
                "",
                "## Assertions",
                "- negative install before verification: PASS (fail closed)",
                "- trust verify local: PASS",
                "- positive install after verification: PASS",
            ]
        )
        + "\n"
    )
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
