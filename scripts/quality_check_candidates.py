#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research" / "candidate-packs-v1.json"
OUT = ROOT / "research" / "candidate-packs-quality-report.md"

REQUIRED_FIELDS = [
    "slug", "title", "type", "problem", "includes", "scopes", "risk_level", "quality_tests"
]


def score_candidate(c: dict) -> tuple[int, list[str]]:
    score = 0
    notes = []

    missing = [f for f in REQUIRED_FIELDS if f not in c]
    if missing:
        notes.append(f"Missing fields: {', '.join(missing)}")
        return 0, notes

    score += 20

    if len(c.get("includes", [])) >= 4:
        score += 20
    else:
        notes.append("Includes list too short (<4)")

    if len(c.get("quality_tests", [])) >= 3:
        score += 20
    else:
        notes.append("Quality tests too short (<3)")

    scopes = c.get("scopes", [])
    if isinstance(scopes, list) and len(scopes) >= 1:
        score += 20
    else:
        notes.append("No scopes declared")

    if c.get("risk_level") in {"low", "medium", "high"}:
        score += 10
    else:
        notes.append("Invalid risk_level")

    if len(c.get("problem", "")) >= 30:
        score += 10
    else:
        notes.append("Problem statement too short")

    return score, notes


def main() -> int:
    data = json.loads(SRC.read_text())
    candidates = data.get("candidates", [])

    rows = []
    pass_count = 0
    for c in candidates:
        score, notes = score_candidate(c)
        verdict = "PASS" if score >= 75 else "REVIEW"
        if verdict == "PASS":
            pass_count += 1
        rows.append((c.get("slug", "?"), c.get("type", "?"), score, verdict, "; ".join(notes) if notes else "OK"))

    lines = [
        "# Candidate Pack Quality Report",
        "",
        f"Total candidates: {len(candidates)}",
        f"Pass (>=75): {pass_count}",
        "",
        "| slug | type | score | verdict | notes |",
        "|---|---:|---:|---|---|",
    ]

    for slug, typ, score, verdict, notes in rows:
        lines.append(f"| `{slug}` | {typ} | {score} | **{verdict}** | {notes} |")

    OUT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT}")
    print(f"Pass: {pass_count}/{len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
