#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "research" / "candidate-packs-v1.json"
OUT = ROOT / "research" / "runtime-simulation-report.md"


def tier_from_score(score: int) -> str:
    if score >= 95:
        return "gold"
    if score >= 85:
        return "silver"
    if score >= 75:
        return "bronze"
    return "unverified"


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

    tier = tier_from_score(score)
    return {
        "slug": pack.get("slug"),
        "title": pack.get("title"),
        "type": pack.get("type"),
        "risk_level": pack.get("risk_level", "low"),
        "score": score,
        "tier": tier,
        "verified": score >= 75,
        "tests": tests,
    }


def main() -> int:
    data = json.loads(CANDIDATES.read_text())
    candidates = data.get("candidates", [])
    results = [simulate_pack(c) for c in candidates]

    min_by_risk = {"low": 75, "medium": 85, "high": 95}
    gated = []
    for r in results:
        req = min_by_risk.get(r.get("risk_level", "low"), 85)
        r["required_score"] = req
        r["risk_gate_pass"] = r["score"] >= req
        r["final_verified"] = bool(r["verified"] and r["risk_gate_pass"])
        gated.append(r)

    verified = [r for r in gated if r["final_verified"]]

    lines = [
        "# Runtime Simulation Verification Report",
        "",
        f"Candidates: {len(gated)}",
        f"Final verified (tier+risk gate): {len(verified)}",
        "",
        "| slug | type | risk | score | tier | risk_gate | final_verified |",
        "|---|---|---|---:|---|---|---|",
    ]

    for r in gated:
        lines.append(
            f"| `{r['slug']}` | {r['type']} | {r['risk_level']} | {r['score']} | {r['tier']} | {'✅' if r['risk_gate_pass'] else '❌'} | {'✅' if r['final_verified'] else '❌'} |"
        )

    lines += ["", "## Detailed test results", ""]
    for r in gated:
        lines.append(f"### {r['title']} (`{r['slug']}`) — tier: {r['tier']}, required: {r['required_score']}, score: {r['score']}")
        for t in r["tests"]:
            lines.append(f"- {'✅' if t['pass'] else '❌'} **{t['name']}** — {t['details']}")
        lines.append("")

    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT}")
    print(f"Verified: {len(verified)}/{len(gated)}")

    # Save machine-readable result for downstream gating
    payload = {
        "results": gated,
        "verified_slugs": [r["slug"] for r in verified],
        "delisted_slugs": [r["slug"] for r in gated if not r["final_verified"]],
        "tiered_verified": {
            "gold": [r["slug"] for r in verified if r["tier"] == "gold"],
            "silver": [r["slug"] for r in verified if r["tier"] == "silver"],
            "bronze": [r["slug"] for r in verified if r["tier"] == "bronze"],
        },
    }
    (ROOT / "research" / "runtime-simulation-result.json").write_text(json.dumps(payload, indent=2))
    print(f"Wrote {ROOT / 'research' / 'runtime-simulation-result.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
