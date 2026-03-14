#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "research" / "candidate-packs-v1.json"
OUT = ROOT / "research" / "runtime-simulation-report.md"


def simulate_pack(pack: dict) -> dict:
    scopes = set(pack.get("scopes", []))
    risk = pack.get("risk_level", "low")
    includes = " ".join(pack.get("includes", [])).lower()

    tests = []

    # Scenario 1: Capability declaration sanity
    tests.append({
        "name": "declares_scopes",
        "pass": len(scopes) > 0,
        "details": f"scope_count={len(scopes)}"
    })

    # Scenario 2: Safety alignment
    sensitive = {"email.send", "message.send", "payment.charge", "social.post", "files.delete"}
    has_sensitive = len(scopes.intersection(sensitive)) > 0
    safety_ok = (risk in {"medium", "high"}) if has_sensitive else True
    tests.append({
        "name": "risk_matches_scope_sensitivity",
        "pass": safety_ok,
        "details": f"has_sensitive={has_sensitive}, risk={risk}"
    })

    # Scenario 3: Recoverability / observability hints
    recoverability_signal = any(k in includes for k in ["fallback", "retry", "audit", "log", "escalation", "rollback"])
    tests.append({
        "name": "has_recoverability_or_audit_signal",
        "pass": recoverability_signal,
        "details": "includes fallback/retry/audit/log/escalation/rollback"
    })

    # Scenario 4: Testability
    qtests = pack.get("quality_tests", [])
    tests.append({
        "name": "has_min_quality_tests",
        "pass": len(qtests) >= 3,
        "details": f"quality_tests={len(qtests)}"
    })

    passed = sum(1 for t in tests if t["pass"])
    score = round((passed / len(tests)) * 100)

    return {
        "slug": pack.get("slug"),
        "title": pack.get("title"),
        "type": pack.get("type"),
        "score": score,
        "verified": score >= 75,
        "tests": tests,
    }


def main() -> int:
    data = json.loads(CANDIDATES.read_text())
    candidates = data.get("candidates", [])
    results = [simulate_pack(c) for c in candidates]

    verified = [r for r in results if r["verified"]]

    lines = [
        "# Runtime Simulation Verification Report",
        "",
        f"Candidates: {len(results)}",
        f"Verified (>=75): {len(verified)}",
        "",
        "| slug | type | score | verified |",
        "|---|---|---:|---|",
    ]

    for r in results:
        lines.append(f"| `{r['slug']}` | {r['type']} | {r['score']} | {'✅' if r['verified'] else '❌'} |")

    lines += ["", "## Detailed test results", ""]
    for r in results:
        lines.append(f"### {r['title']} (`{r['slug']}`)")
        for t in r["tests"]:
            lines.append(f"- {'✅' if t['pass'] else '❌'} **{t['name']}** — {t['details']}")
        lines.append("")

    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT}")
    print(f"Verified: {len(verified)}/{len(results)}")

    # Save machine-readable result for downstream gating
    payload = {"results": results, "verified_slugs": [r["slug"] for r in verified]}
    (ROOT / "research" / "runtime-simulation-result.json").write_text(json.dumps(payload, indent=2))
    print(f"Wrote {ROOT / 'research' / 'runtime-simulation-result.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
