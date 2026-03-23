#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = os.getenv("BOTSTORE_API", "http://127.0.0.1:8787").rstrip("/")
ROOT = Path("/Users/claw/.openclaw/workspace/botstore")
OUT_JSON = ROOT / "research" / "trust-chain-negative-matrix-result.json"
OUT_MD = ROOT / "research" / "trust-chain-negative-matrix-report.md"


def _req(method: str, path: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload or {}).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def post(path: str, payload: dict) -> dict:
    return _req("POST", path, payload)


def put(path: str, payload: dict) -> dict:
    return _req("PUT", path, payload)


def main() -> int:
    ts = str(time.time_ns())
    creator = post("/creators", {"name": f"Trust Neg {ts}", "verification": "verified", "trust_score": 0.9})

    cases = [
        {
            "name": "missing_signature",
            "payload_template": {
                "artifact_uri": "oci://botstore/{slug}:1.0.1",
                "signature_refs": [],
                "sbom_ref": "sbom://local/{slug}.spdx.json",
                "attestation_refs": [
                    "att://build/{slug}",
                    "att://verify/{slug}",
                    "att://conformance/{slug}",
                    "att://qa/{slug}",
                    "att://prov/{slug}",
                ],
            },
            "expect_error": "missing_signature_refs",
        },
        {
            "name": "missing_sbom",
            "payload_template": {
                "artifact_uri": "oci://botstore/{slug}:1.0.1",
                "signature_refs": ["sig://local/{slug}"],
                "sbom_ref": None,
                "attestation_refs": [
                    "att://build/{slug}",
                    "att://verify/{slug}",
                    "att://conformance/{slug}",
                    "att://qa/{slug}",
                    "att://prov/{slug}",
                ],
            },
            "expect_error": "missing_sbom_ref",
        },
        {
            "name": "missing_conformance_attestation",
            "payload_template": {
                "artifact_uri": "oci://botstore/{slug}:1.0.1",
                "signature_refs": ["sig://local/{slug}"],
                "sbom_ref": "sbom://local/{slug}.spdx.json",
                "attestation_refs": [
                    "att://build/{slug}",
                    "att://verify/{slug}",
                    "att://qa/{slug}",
                    "att://prov/{slug}",
                ],
            },
            "expect_error": "missing_conformance_attestation",
        },
    ]

    results = []
    for idx, case in enumerate(cases, start=1):
        case_slug = f"trust-neg-{ts}-{idx}"
        pack = post(
            "/packs",
            {
                "slug": case_slug,
                "title": f"Trust Negative Matrix {idx}",
                "type": "skill",
                "version": "1.0.0",
                "description": "negative matrix",
                "risk_level": "medium",
                "scopes": ["log.read"],
                "creator_id": creator["id"],
            },
        )
        version = post(
            f"/packs/{pack['id']}/versions",
            {
                "semver": "1.0.1",
                "manifest_version": "v2",
                "capabilities_declared": [f"deploy.rollback.neg.{idx}.{ts}"],
                "scopes_requested": ["log.read"],
                "actions_supported": ["deploy.rollback"],
                "compatible_runtimes": ["openclaw"],
                "policy_requirements": {"runtime_band_max": "B"},
                "verification_tier": "tier2_verified",
            },
        )

        tpl = json.loads(json.dumps(case["payload_template"]))
        payload = {
            "artifact_uri": tpl["artifact_uri"].format(slug=case_slug),
            "signature_refs": [x.format(slug=case_slug) for x in tpl.get("signature_refs", [])],
            "sbom_ref": (tpl.get("sbom_ref").format(slug=case_slug) if isinstance(tpl.get("sbom_ref"), str) else None),
            "attestation_refs": [x.format(slug=case_slug) for x in tpl.get("attestation_refs", [])],
        }

        put(f"/packs/{pack['id']}/versions/{version['id']}/trust", payload)
        verify = post(f"/packs/{pack['id']}/versions/{version['id']}/trust/verify-local", {})
        ok = (verify.get("ok") is False) and (verify.get("verification_error") == case["expect_error"])
        results.append({
            "case": case["name"],
            "expected_error": case["expect_error"],
            "verify": verify,
            "pass": ok,
        })

    all_pass = all(r["pass"] for r in results)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": BASE,
        "pack_id": pack["id"],
        "pack_version_id": version["id"],
        "all_pass": all_pass,
        "results": results,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2))
    OUT_MD.write_text(
        "\n".join([
            "# Trust Chain Negative Matrix Report",
            "",
            f"- Generated: {payload['generated_at']}",
            f"- All pass: {all_pass}",
            "",
            "## Cases",
        ] + [f"- {r['case']}: {'PASS' if r['pass'] else 'FAIL'}" for r in results]) + "\n"
    )

    if not all_pass:
        raise SystemExit(1)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
