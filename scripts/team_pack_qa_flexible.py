#!/usr/bin/env python3
import argparse
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = os.getenv("BOTSTORE_API_BASE", "http://127.0.0.1:8787")


def http_json(path: str):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def score_scenario(team: dict, scen: dict, slug_to_scopes: dict):
    skill_slugs = set(team.get("shared_skills", []))
    for role in team.get("roles", []):
        for sk in role.get("owned_skills", []):
            skill_slugs.add(sk)

    caps = set()
    for slug in skill_slugs:
        caps.update(slug_to_scopes.get(slug, []))

    req_caps = set(scen.get("required_capabilities", []))
    cap_cov = len(caps.intersection(req_caps)) / max(len(req_caps), 1)

    team_roles = {norm(r.get("role", "")) for r in team.get("roles", [])}
    req_roles = {norm(r) for r in scen.get("required_roles", [])}
    role_cov = len(team_roles.intersection(req_roles)) / max(len(req_roles), 1)

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


def build_capability_index(catalog):
    idx = {}
    for p in catalog:
        for c in p.get("scopes", []):
            idx.setdefault(c, []).append(p.get("slug"))
    return idx


def apply_autofix(team_data: dict, rows: list[dict], cap_idx: dict):
    by_slug = {t["slug"]: t for t in team_data["team_packs"]}
    for row in rows:
        if row["pass"]:
            continue
        team = by_slug[row["team_slug"]]

        # patch capabilities by adding first available skill
        for cap in row.get("missing_capabilities", []):
            cands = cap_idx.get(cap, [])
            if cands:
                if cands[0] not in team.get("shared_skills", []):
                    team.setdefault("shared_skills", []).append(cands[0])

        # patch artifacts by extending first role deliverables
        if team.get("roles"):
            first = team["roles"][0]
            first.setdefault("deliverables", [])
            known = {norm(x) for x in first["deliverables"]}
            for art in row.get("missing_artifacts", []):
                if art not in known:
                    first["deliverables"].append(art)
                    known.add(art)

    return team_data


def evaluate(team_data: dict, scenarios: list[dict], slug_to_scopes: dict):
    team_by_slug = {t["slug"]: t for t in team_data["team_packs"]}
    rows = []
    for scen in scenarios:
        team = team_by_slug.get(scen["team_slug"])
        if not team:
            rows.append(
                {
                    "scenario_id": scen["id"],
                    "team_slug": scen["team_slug"],
                    "score": 0.0,
                    "capability_coverage": 0.0,
                    "role_coverage": 0.0,
                    "artifact_coverage": 0.0,
                    "missing_capabilities": scen.get("required_capabilities", []),
                    "missing_roles": scen.get("required_roles", []),
                    "missing_artifacts": scen.get("expected_artifacts", []),
                    "pass": False,
                    "error": "team not found",
                }
            )
            continue
        evalr = score_scenario(team, scen, slug_to_scopes)
        rows.append({"scenario_id": scen["id"], "team_slug": scen["team_slug"], **evalr})

    summary = {
        "total": len(rows),
        "pass": sum(1 for r in rows if r["pass"]),
        "avg_score": round(sum(r["score"] for r in rows) / max(len(rows), 1), 3),
    }
    return rows, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teams", required=True, help="Path to team packs json")
    ap.add_argument("--scenarios", required=True, help="Path to scenarios json")
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--patched-out", required=False)
    args = ap.parse_args()

    team_data = json.loads(Path(args.teams).read_text())
    scenarios = json.loads(Path(args.scenarios).read_text())["scenarios"]
    catalog = http_json("/catalog")

    slug_to_scopes = {p["slug"]: p.get("scopes", []) for p in catalog}
    cap_idx = build_capability_index(catalog)

    rows, summary = evaluate(team_data, scenarios, slug_to_scopes)

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "scenarios": rows,
    }

    patched_summary = None
    if args.patched_out:
        patched_data = apply_autofix(json.loads(Path(args.teams).read_text()), rows, cap_idx)
        Path(args.patched_out).write_text(json.dumps(patched_data, indent=2))
        rows2, summary2 = evaluate(patched_data, scenarios, slug_to_scopes)
        payload["patched"] = {"summary": summary2, "scenarios": rows2}
        patched_summary = summary2

    Path(args.out_json).write_text(json.dumps(payload, indent=2))

    lines = [
        "# Team Pack QA Flexible Report",
        "",
        f"Generated: {payload['generatedAt']}",
        f"Initial pass: **{summary['pass']}/{summary['total']}** (avg {summary['avg_score']})",
    ]
    if patched_summary:
        lines.append(
            f"Patched pass: **{patched_summary['pass']}/{patched_summary['total']}** (avg {patched_summary['avg_score']})"
        )
    lines += [
        "",
        "| scenario | team | score | cap | role | art | pass |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| `{r['scenario_id']}` | `{r['team_slug']}` | {r['score']} | {r['capability_coverage']} | {r['role_coverage']} | {r['artifact_coverage']} | {'✅' if r['pass'] else '❌'} |"
        )

    Path(args.out_md).write_text("\n".join(lines) + "\n")
    print(f"Wrote {args.out_json}")
    if args.patched_out:
        print(f"Wrote {args.patched_out}")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
