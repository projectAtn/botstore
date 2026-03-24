#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = os.getenv("BOTSTORE_API", "http://127.0.0.1:8787").rstrip("/")
ROOT = Path("/Users/claw/.openclaw/workspace/botstore")
FIXTURES_PATH = ROOT / "research" / "policy-fixtures-v1.json"
OUT_JSON = ROOT / "research" / "policy-fixture-report.json"
OUT_MD = ROOT / "research" / "policy-fixture-report.md"


def post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    fixtures = json.loads(FIXTURES_PATH.read_text()).get("fixtures", [])
    rows = []
    for f in fixtures:
        payload = {
            "subject": {"tenant_id": "default"},
            "resource": {
                "scopes_requested": f.get("requested_scopes", []),
                "verification_tier": f.get("verification_tier", "tier0_listed"),
            },
            "action": f.get("action", "install"),
            "context": {"runtime_band": f.get("runtime_band", "D")},
            "rules": [],
        }
        res = post("/policy/bps/evaluate", payload)
        ok = res.get("effect") == f.get("expected_effect")
        rows.append({
            "name": f.get("name"),
            "expected_effect": f.get("expected_effect"),
            "actual_effect": res.get("effect"),
            "pass": ok,
            "result": res,
        })

    all_pass = all(r["pass"] for r in rows)
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": BASE,
        "all_pass": all_pass,
        "count": len(rows),
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2))
    OUT_MD.write_text(
        "\n".join([
            "# Policy Fixture Report",
            "",
            f"- Generated: {out['generated_at']}",
            f"- All pass: {all_pass}",
            f"- Count: {len(rows)}",
            "",
            "## Cases",
        ] + [f"- {r['name']}: {'PASS' if r['pass'] else 'FAIL'} ({r['actual_effect']})" for r in rows]) + "\n"
    )
    if not all_pass:
        raise SystemExit(1)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
