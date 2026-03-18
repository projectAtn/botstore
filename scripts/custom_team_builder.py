#!/usr/bin/env python3
import argparse
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8787"
ROLES_IN = ROOT / "research" / "singular-role-agent-offerings-v1.json"
OUT_DEFAULT = ROOT / "research" / "custom-team-built.json"


def http_json(path: str):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def build_team(name: str, objective: str, selected_role_slugs: list[str], risk: str):
    role_catalog = json.loads(ROLES_IN.read_text())["agents"]
    role_by_slug = {r["slug"]: r for r in role_catalog}

    roles = []
    shared = set()
    for rs in selected_role_slugs:
        r = role_by_slug.get(rs)
        if not r:
            continue
        roles.append(
            {
                "role": r["role"],
                "personality_slug": r["personality_slug"],
                "owned_skills": r.get("starter_skills", []),
                "deliverables": ["status-report", "action-items"],
            }
        )
        for sk in r.get("suggested_shared_skills", []):
            shared.add(sk)

    return {
        "slug": slugify(name),
        "title": name,
        "purpose": objective,
        "team_type": "custom",
        "shared_skills": sorted(shared),
        "roles": roles,
        "risk_level": risk,
    }


def validate_team(team: dict):
    catalog = http_json("/catalog")
    slug_to_scopes = {p["slug"]: p.get("scopes", []) for p in catalog}

    skill_slugs = set(team.get("shared_skills", []))
    for r in team.get("roles", []):
        for sk in r.get("owned_skills", []):
            skill_slugs.add(sk)

    scopes = set()
    for s in skill_slugs:
        scopes.update(slug_to_scopes.get(s, []))

    warnings = []
    if len(team.get("roles", [])) < 2:
        warnings.append("Team should usually include at least 2 roles")
    if team.get("risk_level") in {"medium", "high"} and not any(
        ("compliance" in (r.get("personality_slug") or "") or "privacy" in (r.get("personality_slug") or ""))
        for r in team.get("roles", [])
    ):
        warnings.append("Medium/high risk teams should include governance/privacy personality")
    if not scopes:
        warnings.append("No capabilities detected from selected skills")

    return {
        "ok": True,
        "warnings": warnings,
        "capability_count": len(scopes),
        "skill_count": len(skill_slugs),
        "role_count": len(team.get("roles", [])),
    }


def main():
    ap = argparse.ArgumentParser(description="Build a custom team from singular role-agent offerings")
    ap.add_argument("--name", required=True)
    ap.add_argument("--objective", required=True)
    ap.add_argument("--roles", required=True, help="Comma-separated role slugs from singular-role-agent-offerings-v1.json")
    ap.add_argument("--risk", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    args = ap.parse_args()

    selected = [x.strip() for x in args.roles.split(",") if x.strip()]
    team = build_team(args.name, args.objective, selected, args.risk)
    check = validate_team(team)

    out = Path(args.out)
    out.write_text(json.dumps({"team": team, "validation": check}, indent=2))
    print(f"Wrote {out}")
    print(json.dumps(check, indent=2))


if __name__ == "__main__":
    main()
