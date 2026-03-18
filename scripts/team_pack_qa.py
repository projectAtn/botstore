#!/usr/bin/env python3
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8787"
TEAM_IN = ROOT / "research" / "team-packs-v1.json"
SCENARIOS_IN = ROOT / "research" / "team-pack-qa-scenarios-v1.json"
OUT_JSON = ROOT / "research" / "team-pack-qa-result-v1.json"
OUT_MD = ROOT / "research" / "team-pack-qa-report-v1.md"
PATCHED_OUT = ROOT / "research" / "team-packs-v2.json"


def http_json(path: str):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def score_scenario(team: dict, scen: dict, slug_to_scopes: dict):
    # Capabilities from shared skills + role owned skills
    skill_slugs = set(team.get("shared_skills", []))
    for role in team.get("roles", []):
        skill_slugs.update(role.get("owned_skills", []))

    caps = set()
    for slug in skill_slugs:
        caps.update(slug_to_scopes.get(slug, []))

    req_caps = set(scen.get("required_capabilities", []))
    cap_cov = len(caps.intersection(req_caps)) / max(len(req_caps), 1)

    # Role coverage
    team_roles = {norm(r.get("role", "")) for r in team.get("roles", [])}
    req_roles = {norm(r) for r in scen.get("required_roles", [])}
    role_cov = len(team_roles.intersection(req_roles)) / max(len(req_roles), 1)

    # Artifact coverage against role deliverables
    all_delivs = set()
    for r in team.get("roles", []):
        for d in r.get("deliverables", []):
            all_delivs.add(norm(d))
    req_art = {norm(a) for a in scen.get("expected_artifacts", [])}
    art_cov = len(all_delivs.intersection(req_art)) / max(len(req_art), 1)

    score = round(0.5 * cap_cov + 0.3 * role_cov + 0.2 * art_cov, 3)
    return {
        "score": score,
        "capability_coverage": round(cap_cov, 3),
        "role_coverage": round(role_cov, 3),
        "artifact_coverage": round(art_cov, 3),
        "missing_capabilities": sorted(req_caps - caps),
        "missing_roles": sorted(req_roles - team_roles),
        "missing_artifacts": sorted(req_art - all_delivs),
        "pass": score >= 0.8,
    }


def build_capability_index(catalog: list[dict]):
    idx = {}
    for p in catalog:
        for c in p.get("scopes", []):
            idx.setdefault(c, []).append(p.get("slug"))
    return idx


def suggest_patch(team: dict, scenario_eval: dict, cap_idx: dict):
    suggestions = []
    for cap in scenario_eval.get("missing_capabilities", []):
        cands = cap_idx.get(cap, [])
        if cands:
            suggestions.append({"type": "capability", "capability": cap, "suggested_pack": cands[0]})
    for role in scenario_eval.get("missing_roles", []):
        suggestions.append({"type": "role", "role": role, "suggested_action": "add role/personality mapping"})
    for art in scenario_eval.get("missing_artifacts", []):
        suggestions.append({"type": "artifact", "artifact": art, "suggested_action": "add deliverable to matching role"})
    return suggestions


def apply_simple_autofix(team_data: dict, qa_result: dict, cap_idx: dict):
    by_slug = {t["slug"]: t for t in team_data["team_packs"]}
    for row in qa_result["scenarios"]:
        if row["pass"]:
            continue
        team = by_slug[row["team_slug"]]

        # add first suggested capability pack to shared skills
        sugg = suggest_patch(team, row, cap_idx)
        for s in sugg:
            if s["type"] == "capability":
                if s["suggested_pack"] not in team.get("shared_skills", []):
                    team.setdefault("shared_skills", []).append(s["suggested_pack"])
                    break

        # add placeholders for missing artifacts into first role deliverables
        if team.get("roles"):
            first_role = team["roles"][0]
            first_role.setdefault("deliverables", [])
            for art in row.get("missing_artifacts", []):
                if art not in [norm(x) for x in first_role["deliverables"]]:
                    first_role["deliverables"].append(art)

    return team_data


def main():
    team_data = json.loads(TEAM_IN.read_text())
    scenarios = json.loads(SCENARIOS_IN.read_text())["scenarios"]
    catalog = http_json("/catalog")

    slug_to_scopes = {p["slug"]: p.get("scopes", []) for p in catalog}
    cap_idx = build_capability_index(catalog)

    team_by_slug = {t["slug"]: t for t in team_data["team_packs"]}
    rows = []
    for scen in scenarios:
        team = team_by_slug[scen["team_slug"]]
        evalr = score_scenario(team, scen, slug_to_scopes)
        rows.append({"scenario_id": scen["id"], "team_slug": scen["team_slug"], **evalr})

    summary = {
        "total": len(rows),
        "pass": sum(1 for r in rows if r["pass"]),
        "avg_score": round(sum(r["score"] for r in rows) / max(len(rows), 1), 3),
    }

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "scenarios": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2))

    # Apply simple auto-fix if needed and re-evaluate
    fixed = apply_simple_autofix(json.loads(TEAM_IN.read_text()), payload, cap_idx)
    PATCHED_OUT.write_text(json.dumps(fixed, indent=2))

    # Re-score patched version
    team_by_slug2 = {t["slug"]: t for t in fixed["team_packs"]}
    rows2 = []
    for scen in scenarios:
        team = team_by_slug2[scen["team_slug"]]
        evalr = score_scenario(team, scen, slug_to_scopes)
        rows2.append({"scenario_id": scen["id"], "team_slug": scen["team_slug"], **evalr})

    summary2 = {
        "total": len(rows2),
        "pass": sum(1 for r in rows2 if r["pass"]),
        "avg_score": round(sum(r["score"] for r in rows2) / max(len(rows2), 1), 3),
    }

    report = [
        "# Team Pack QA Report v1",
        "",
        f"Generated: {payload['generatedAt']}",
        "",
        f"Initial pass: **{summary['pass']}/{summary['total']}** (avg {summary['avg_score']})",
        f"After autofix pass: **{summary2['pass']}/{summary2['total']}** (avg {summary2['avg_score']})",
        "",
        "## Scenario scores (initial)",
        "",
        "| scenario | team | score | cap | role | art | pass |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        report.append(
            f"| `{r['scenario_id']}` | `{r['team_slug']}` | {r['score']} | {r['capability_coverage']} | {r['role_coverage']} | {r['artifact_coverage']} | {'✅' if r['pass'] else '❌'} |"
        )

    report += ["", "## Scenario scores (after autofix)", "", "| scenario | team | score | cap | role | art | pass |", "|---|---|---:|---:|---:|---:|---|"]
    for r in rows2:
        report.append(
            f"| `{r['scenario_id']}` | `{r['team_slug']}` | {r['score']} | {r['capability_coverage']} | {r['role_coverage']} | {r['artifact_coverage']} | {'✅' if r['pass'] else '❌'} |"
        )

    OUT_MD.write_text("\n".join(report) + "\n")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {PATCHED_OUT}")
    print(f"Wrote {OUT_MD}")
    print(f"Initial: {summary['pass']}/{summary['total']} | Patched: {summary2['pass']}/{summary2['total']}")


if __name__ == "__main__":
    main()
