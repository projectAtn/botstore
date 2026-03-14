#!/usr/bin/env python3
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:8787"
ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "research" / "pack-performance-contracts.json"
OUT_MD = ROOT / "research" / "contract-task-report.md"
OUT_JSON = ROOT / "research" / "contract-task-result.json"


def http_json(path: str, method: str = "GET", payload=None):
    headers = {"Content-Type": "application/json"}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def find_pack_by_slug(catalog, slug):
    for p in catalog:
        if p.get("slug") == slug:
            return p
    return None


def min_score_for_risk(risk_level: str) -> int:
    table = {"low": 75, "medium": 90, "high": 95}
    return table.get((risk_level or "low").lower(), 90)


def run_contract(catalog, contract):
    slug = contract["slug"]
    pack = find_pack_by_slug(catalog, slug)
    checks = []
    risk_level = contract.get("risk_level", "low")
    must_deterministic = bool(contract.get("must_select_deterministically", False))

    if not pack:
        return {
            "slug": slug,
            "statement": contract["statement"],
            "pass": False,
            "score": 0,
            "checks": [{"name": "pack_exists", "pass": False, "details": "not found in catalog"}],
            "latency_ms": 0,
        }

    t0 = time.time()

    # 1) Contract scope coverage
    req_scopes = set(contract.get("required_scopes", []))
    pack_scopes = set(pack.get("scopes", []))
    coverage_ok = req_scopes.issubset(pack_scopes)
    checks.append({
        "name": "scope_coverage",
        "pass": coverage_ok,
        "details": f"required={sorted(req_scopes)}, pack={sorted(pack_scopes)}",
    })

    # 2) Policy behavior check
    pol = http_json("/agent/policy-evaluate", "POST", {
        "user_id": "contract-test-user",
        "runtime": "openclaw",
        "pack_id": pack["id"],
    })
    expected = contract.get("expected_policy", "allow")
    policy_ok = pol.get("decision") == expected
    checks.append({
        "name": "policy_expectation",
        "pass": policy_ok,
        "details": f"expected={expected}, got={pol.get('decision')}",
    })

    # 3) Capability search should return this pack for required scopes
    search = http_json("/agent/search-capabilities", "POST", {
        "user_id": "contract-test-user",
        "runtime": "openclaw",
        "intent": contract.get("statement", ""),
        "missing_capabilities": list(req_scopes),
        "limit": 10,
    })
    result_slugs = [r.get("slug") for r in search.get("results", [])]
    discoverable_ok = slug in result_slugs
    checks.append({
        "name": "discoverable_by_required_capabilities",
        "pass": discoverable_ok,
        "details": f"top_results={result_slugs[:5]}",
    })

    # 4) Install-by-capability should include this pack when asked for its contract scopes
    install = http_json("/agent/install-by-capability", "POST", {
        "user_id": "contract-test-user",
        "runtime": "openclaw",
        "required_capabilities": list(req_scopes),
    })
    install_slugs = [i.get("slug") for i in install.get("installs", [])]
    install_ok = slug in install_slugs
    checks.append({
        "name": "install_by_capability_selects_pack",
        "pass": install_ok,
        "details": f"installed={install_slugs}",
    })

    deterministic_ok = (install_slugs and install_slugs[0] == slug)
    checks.append({
        "name": "deterministic_primary_selection",
        "pass": (deterministic_ok if must_deterministic else True),
        "details": f"required={must_deterministic}, first_installed={(install_slugs[0] if install_slugs else None)}",
    })

    passed = sum(1 for c in checks if c["pass"])
    score = round((passed / len(checks)) * 100)

    min_score = min_score_for_risk(risk_level)
    contract_pass = score >= min_score

    return {
        "slug": slug,
        "statement": contract["statement"],
        "pack_id": pack["id"],
        "risk_level": risk_level,
        "must_select_deterministically": must_deterministic,
        "min_score": min_score,
        "pass": contract_pass,
        "score": score,
        "checks": checks,
        "latency_ms": round((time.time() - t0) * 1000, 1),
    }


def main():
    payload = json.loads(CONTRACTS.read_text())
    contracts = payload.get("contracts", [])
    catalog = http_json("/catalog")

    results = [run_contract(catalog, c) for c in contracts]
    summary = {
        "total": len(results),
        "pass": sum(1 for r in results if r["pass"]),
        "avg_score": round(sum(r["score"] for r in results) / max(len(results), 1), 1),
    }

    OUT_JSON.write_text(json.dumps({"summary": summary, "results": results}, indent=2))

    lines = [
        "# Contract Task Runner Report",
        "",
        f"Total contracts: {summary['total']}",
        f"Pass: {summary['pass']}",
        f"Average score: {summary['avg_score']}",
        "",
        "| slug | risk | min_score | score | pass | latency_ms |",
        "|---|---|---:|---:|---|---:|",
    ]

    for r in results:
        lines.append(f"| `{r['slug']}` | {r['risk_level']} | {r['min_score']} | {r['score']} | {'✅' if r['pass'] else '❌'} | {r['latency_ms']} |")

    lines.append("\n## Details\n")
    for r in results:
        lines.append(f"### `{r['slug']}` — {r['statement']}")
        for c in r["checks"]:
            lines.append(f"- {'✅' if c['pass'] else '❌'} **{c['name']}** — {c['details']}")
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
