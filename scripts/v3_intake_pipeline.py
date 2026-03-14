#!/usr/bin/env python3
"""V3 intake pipeline for candidate skill/personality packs.

Pipeline:
1) Merge v3 source files into a unified candidate set.
2) Run structural quality checks.
3) Run runtime simulation scoring.
4) Apply strict tier + risk gating.
5) Generate contract tests for top 12 v3 packs.
6) Emit promotion list + markdown summary.

This script is self-contained and does not mutate legacy v1/v2 files.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"

DEFAULT_SKILLS = RESEARCH / "candidate-packs-v3-skills.json"
DEFAULT_PERSONALITIES = RESEARCH / "candidate-packs-v3-personalities.json"

# Compatibility fallbacks if team used older naming.
SKILL_FALLBACKS = [
    RESEARCH / "candidate-skills-v3.json",
    RESEARCH / "candidate-packs-v3-skills.json",
]
PERSONALITY_FALLBACKS = [
    RESEARCH / "candidate-personalities-v3.json",
    RESEARCH / "candidate-packs-v3-personalities.json",
]

MERGED_OUT = RESEARCH / "candidate-packs-v3.json"
QUALITY_OUT_MD = RESEARCH / "candidate-packs-v3-quality-report.md"
QUALITY_OUT_JSON = RESEARCH / "candidate-packs-v3-quality-result.json"
SIM_OUT_MD = RESEARCH / "runtime-simulation-v3-report.md"
SIM_OUT_JSON = RESEARCH / "runtime-simulation-v3-result.json"
CONTRACTS_OUT = RESEARCH / "pack-performance-contracts-v3.json"
PROMOTION_OUT_MD = RESEARCH / "v3-intake-summary.md"
PROMOTION_OUT_JSON = RESEARCH / "v3-promotion-list.json"

REQUIRED_FIELDS = [
    "slug",
    "title",
    "type",
    "problem",
    "includes",
    "scopes",
    "risk_level",
    "quality_tests",
]

SENSITIVE_SCOPES = {
    "email.send",
    "message.send",
    "payment.charge",
    "social.post",
    "files.delete",
    "admin.write",
    "billing.write",
}

RISK_GATES = {"low": 80, "medium": 90, "high": 95}


@dataclass
class MergeResult:
    merged_path: Path
    total: int
    skills: int
    personalities: int
    duplicates_overwritten: list[str]
    warnings: list[str]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _pick_existing(primary: Path, fallbacks: list[Path]) -> Path:
    if primary.exists():
        return primary
    for p in fallbacks:
        if p.exists():
            return p
    return primary


def _extract_candidates(payload: Any, expected_type: str, source_path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []

    if isinstance(payload, list):
        raw = payload
    elif isinstance(payload, dict):
        raw = []
        for key in ("candidates", "skills", "personalities", "items", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                raw = value
                break
        if not raw:
            warnings.append(
                f"No list field found in {source_path.name}; expected candidates/skills/personalities/items/data"
            )
    else:
        raw = []
        warnings.append(f"Unsupported JSON structure in {source_path.name}")

    normalized: list[dict[str, Any]] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            warnings.append(f"Skipped non-object item at {source_path.name}[{i}]")
            continue
        obj = dict(item)
        obj.setdefault("type", expected_type)
        normalized.append(obj)

    return normalized, warnings


def merge_candidates(skill_file: Path, personality_file: Path, out_path: Path) -> MergeResult:
    warnings: list[str] = []
    combined: list[dict[str, Any]] = []
    skill_count = 0
    personality_count = 0

    for path, expected_type in [(skill_file, "skill"), (personality_file, "personality")]:
        if not path.exists():
            warnings.append(f"Missing input file: {path}")
            continue
        payload = _read_json(path)
        items, item_warnings = _extract_candidates(payload, expected_type, path)
        warnings.extend(item_warnings)
        if expected_type == "skill":
            skill_count += len(items)
        else:
            personality_count += len(items)
        combined.extend(items)

    dedup: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    for c in combined:
        slug = str(c.get("slug", "")).strip()
        if not slug:
            warnings.append("Skipped candidate without slug")
            continue
        if slug in dedup:
            duplicates.append(slug)
        dedup[slug] = c

    merged = {
        "generatedAt": _now(),
        "source": {
            "skills": str(skill_file),
            "personalities": str(personality_file),
        },
        "candidates": list(dedup.values()),
    }
    out_path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    return MergeResult(
        merged_path=out_path,
        total=len(merged["candidates"]),
        skills=skill_count,
        personalities=personality_count,
        duplicates_overwritten=sorted(set(duplicates)),
        warnings=warnings,
    )


def quality_score(candidate: dict[str, Any]) -> tuple[int, list[str]]:
    score = 0
    notes: list[str] = []

    missing = [f for f in REQUIRED_FIELDS if f not in candidate]
    if missing:
        notes.append(f"Missing fields: {', '.join(missing)}")
        return 0, notes

    score += 20

    includes = candidate.get("includes", [])
    if isinstance(includes, list) and len(includes) >= 5:
        score += 20
    else:
        notes.append("Includes list too short (<5)")

    qtests = candidate.get("quality_tests", [])
    if isinstance(qtests, list) and len(qtests) >= 4:
        score += 20
    else:
        notes.append("Quality tests too short (<4)")

    scopes = candidate.get("scopes", [])
    if isinstance(scopes, list) and len(scopes) >= 2:
        score += 15
    else:
        notes.append("Scopes too short (<2)")

    risk = str(candidate.get("risk_level", "")).lower()
    if risk in {"low", "medium", "high"}:
        score += 10
    else:
        notes.append("Invalid risk_level")

    problem = str(candidate.get("problem", ""))
    if len(problem) >= 40:
        score += 10
    else:
        notes.append("Problem statement too short (<40 chars)")

    title = str(candidate.get("title", "")).strip()
    if len(title) >= 6:
        score += 5
    else:
        notes.append("Title too short")

    return score, notes


def write_quality_reports(candidates: list[dict[str, Any]], out_md: Path, out_json: Path) -> dict[str, Any]:
    rows = []
    pass_count = 0
    for c in candidates:
        score, notes = quality_score(c)
        verdict = "PASS" if score >= 80 else "REVIEW"
        if verdict == "PASS":
            pass_count += 1
        rows.append(
            {
                "slug": c.get("slug", "?"),
                "type": c.get("type", "?"),
                "score": score,
                "verdict": verdict,
                "notes": notes,
            }
        )

    payload = {
        "generatedAt": _now(),
        "summary": {"total": len(candidates), "pass": pass_count, "pass_threshold": 80},
        "results": rows,
    }
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Candidate Pack V3 Quality Report",
        "",
        f"Generated: {_now()}",
        f"Total candidates: {len(candidates)}",
        f"Pass (>=80): {pass_count}",
        "",
        "| slug | type | score | verdict | notes |",
        "|---|---|---:|---|---|",
    ]
    for r in rows:
        notes = "; ".join(r["notes"]) if r["notes"] else "OK"
        lines.append(f"| `{r['slug']}` | {r['type']} | {r['score']} | **{r['verdict']}** | {notes} |")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def tier_from_score(score: int) -> str:
    if score >= 95:
        return "gold"
    if score >= 88:
        return "silver"
    if score >= 80:
        return "bronze"
    return "unverified"


def simulate_pack(pack: dict[str, Any]) -> dict[str, Any]:
    scopes = set(pack.get("scopes", []) if isinstance(pack.get("scopes", []), list) else [])
    risk = str(pack.get("risk_level", "low")).lower()
    includes = " ".join(pack.get("includes", []) if isinstance(pack.get("includes", []), list) else []).lower()
    qtests = pack.get("quality_tests", []) if isinstance(pack.get("quality_tests", []), list) else []

    tests = []

    tests.append(
        {
            "name": "declares_scopes",
            "pass": len(scopes) >= 2,
            "details": f"scope_count={len(scopes)}",
        }
    )

    has_sensitive = len(scopes.intersection(SENSITIVE_SCOPES)) > 0
    safety_ok = (risk in {"medium", "high"}) if has_sensitive else True
    tests.append(
        {
            "name": "risk_matches_scope_sensitivity",
            "pass": safety_ok,
            "details": f"has_sensitive={has_sensitive}, risk={risk}",
        }
    )

    recoverability_signal = any(
        k in includes for k in ["fallback", "retry", "audit", "log", "escalation", "rollback", "guardrail"]
    )
    tests.append(
        {
            "name": "has_recoverability_or_audit_signal",
            "pass": recoverability_signal,
            "details": "includes fallback/retry/audit/log/escalation/rollback/guardrail",
        }
    )

    tests.append(
        {
            "name": "has_min_quality_tests",
            "pass": len(qtests) >= 4,
            "details": f"quality_tests={len(qtests)}",
        }
    )

    tests.append(
        {
            "name": "problem_statement_substantive",
            "pass": len(str(pack.get("problem", ""))) >= 40,
            "details": "problem length >= 40 chars",
        }
    )

    passed = sum(1 for t in tests if t["pass"])
    score = round((passed / len(tests)) * 100)
    tier = tier_from_score(score)

    required = RISK_GATES.get(risk, 90)
    risk_gate_pass = score >= required
    final_verified = (score >= 80) and risk_gate_pass

    return {
        "slug": pack.get("slug"),
        "title": pack.get("title"),
        "type": pack.get("type"),
        "risk_level": risk,
        "score": score,
        "tier": tier,
        "required_score": required,
        "risk_gate_pass": risk_gate_pass,
        "final_verified": final_verified,
        "tests": tests,
    }


def write_runtime_reports(candidates: list[dict[str, Any]], out_md: Path, out_json: Path) -> dict[str, Any]:
    results = [simulate_pack(c) for c in candidates]
    verified = [r for r in results if r["final_verified"]]

    payload = {
        "generatedAt": _now(),
        "summary": {
            "total": len(results),
            "final_verified": len(verified),
            "risk_gates": RISK_GATES,
        },
        "results": results,
        "verified_slugs": [r["slug"] for r in verified],
        "delisted_slugs": [r["slug"] for r in results if not r["final_verified"]],
        "tiered_verified": {
            "gold": [r["slug"] for r in verified if r["tier"] == "gold"],
            "silver": [r["slug"] for r in verified if r["tier"] == "silver"],
            "bronze": [r["slug"] for r in verified if r["tier"] == "bronze"],
        },
    }
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Runtime Simulation V3 Report",
        "",
        f"Generated: {_now()}",
        f"Candidates: {len(results)}",
        f"Final verified (strict tier+risk gate): {len(verified)}",
        "",
        "| slug | type | risk | score | tier | required | risk_gate | final_verified |",
        "|---|---|---|---:|---|---:|---|---|",
    ]

    for r in results:
        lines.append(
            f"| `{r['slug']}` | {r['type']} | {r['risk_level']} | {r['score']} | {r['tier']} | {r['required_score']} | {'✅' if r['risk_gate_pass'] else '❌'} | {'✅' if r['final_verified'] else '❌'} |"
        )

    lines += ["", "## Detailed test results", ""]
    for r in results:
        lines.append(
            f"### {r['title']} (`{r['slug']}`) — tier: {r['tier']}, required: {r['required_score']}, score: {r['score']}"
        )
        for t in r["tests"]:
            lines.append(f"- {'✅' if t['pass'] else '❌'} **{t['name']}** — {t['details']}")
        lines.append("")

    out_md.write_text("\n".join(lines), encoding="utf-8")
    return payload


def _contract_statement(pack: dict[str, Any]) -> str:
    title = str(pack.get("title", pack.get("slug", "pack")))
    return f"Agent should select and safely run {title} for its declared capabilities under policy constraints."


def _contract_for_pack(pack: dict[str, Any], runtime_result: dict[str, Any]) -> dict[str, Any]:
    req_scopes = pack.get("scopes", []) if isinstance(pack.get("scopes", []), list) else []
    risk = str(pack.get("risk_level", "low")).lower()

    return {
        "slug": pack.get("slug"),
        "statement": _contract_statement(pack),
        "risk_level": risk,
        "required_scopes": req_scopes,
        "expected_policy": "require_approval" if risk == "high" else "allow",
        "must_select_deterministically": runtime_result.get("tier") in {"gold", "silver"},
    }


def generate_contracts(
    candidates: list[dict[str, Any]],
    quality_payload: dict[str, Any],
    runtime_payload: dict[str, Any],
    out_path: Path,
    top_n: int = 12,
) -> dict[str, Any]:
    q_by_slug = {r["slug"]: r for r in quality_payload.get("results", [])}
    r_by_slug = {r["slug"]: r for r in runtime_payload.get("results", [])}

    ranked: list[tuple[float, dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    for c in candidates:
        slug = c.get("slug")
        q = q_by_slug.get(slug, {"score": 0, "verdict": "REVIEW"})
        r = r_by_slug.get(slug, {"score": 0, "final_verified": False, "tier": "unverified"})
        bonus = 10 if r.get("final_verified") else 0
        composite = float(q.get("score", 0)) * 0.45 + float(r.get("score", 0)) * 0.55 + bonus
        ranked.append((composite, c, q, r))

    ranked.sort(key=lambda t: t[0], reverse=True)
    selected = ranked[:top_n]

    contracts = [_contract_for_pack(c, r) for _, c, _, r in selected]
    payload = {
        "generatedAt": _now(),
        "source": str(MERGED_OUT),
        "selection_method": "top_n_by_composite(0.45*quality + 0.55*runtime + verified_bonus_10)",
        "top_n": top_n,
        "contracts": contracts,
        "ranked": [
            {
                "slug": c.get("slug"),
                "title": c.get("title"),
                "type": c.get("type"),
                "quality_score": q.get("score", 0),
                "runtime_score": r.get("score", 0),
                "final_verified": bool(r.get("final_verified", False)),
                "tier": r.get("tier", "unverified"),
                "composite_score": round(score, 2),
            }
            for score, c, q, r in selected
        ],
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def generate_promotion_list(
    candidates: list[dict[str, Any]],
    quality_payload: dict[str, Any],
    runtime_payload: dict[str, Any],
    contract_payload: dict[str, Any],
    out_json: Path,
    out_md: Path,
    merge: MergeResult,
) -> dict[str, Any]:
    q_by_slug = {r["slug"]: r for r in quality_payload.get("results", [])}
    r_by_slug = {r["slug"]: r for r in runtime_payload.get("results", [])}
    contract_slugs = {c.get("slug") for c in contract_payload.get("contracts", [])}

    promoted = []
    hold = []

    for c in candidates:
        slug = c.get("slug")
        q = q_by_slug.get(slug, {})
        r = r_by_slug.get(slug, {})

        quality_pass = q.get("score", 0) >= 80
        runtime_pass = bool(r.get("final_verified", False))
        in_contract_top12 = slug in contract_slugs

        record = {
            "slug": slug,
            "title": c.get("title"),
            "type": c.get("type"),
            "risk_level": c.get("risk_level"),
            "quality_score": q.get("score", 0),
            "runtime_score": r.get("score", 0),
            "tier": r.get("tier", "unverified"),
            "required_score": r.get("required_score"),
            "quality_pass": quality_pass,
            "runtime_pass": runtime_pass,
            "contract_top12": in_contract_top12,
            "promotion_decision": "PROMOTE" if (quality_pass and runtime_pass and in_contract_top12) else "HOLD",
        }

        if record["promotion_decision"] == "PROMOTE":
            promoted.append(record)
        else:
            hold.append(record)

    promoted.sort(key=lambda x: (x["runtime_score"], x["quality_score"]), reverse=True)
    hold.sort(key=lambda x: (x["runtime_score"], x["quality_score"]), reverse=True)

    payload = {
        "generatedAt": _now(),
        "summary": {
            "total": len(candidates),
            "promoted": len(promoted),
            "hold": len(hold),
            "strict_rule": "PROMOTE iff quality>=80 AND final_verified=true AND selected_in_contract_top12",
        },
        "promoted": promoted,
        "hold": hold,
    }
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# V3 Intake Summary",
        "",
        f"Generated: {_now()}",
        "",
        "## 1) Merge",
        f"- Merged output: `{merge.merged_path}`",
        f"- Total merged candidates: **{merge.total}**",
        f"- Source counts (pre-dedup): skills={merge.skills}, personalities={merge.personalities}",
        f"- Duplicate slugs overwritten: {', '.join(merge.duplicates_overwritten) if merge.duplicates_overwritten else 'none'}",
    ]

    if merge.warnings:
        lines.append("- Warnings:")
        lines.extend([f"  - {w}" for w in merge.warnings])

    lines += [
        "",
        "## 2) Quality check",
        f"- Threshold: **>=80**",
        f"- Pass: **{quality_payload.get('summary', {}).get('pass', 0)} / {quality_payload.get('summary', {}).get('total', 0)}**",
        f"- Output: `{QUALITY_OUT_MD}` and `{QUALITY_OUT_JSON}`",
        "",
        "## 3) Runtime simulation + strict tier/risk gate",
        f"- Risk gates: low={RISK_GATES['low']}, medium={RISK_GATES['medium']}, high={RISK_GATES['high']}",
        f"- Final verified: **{runtime_payload.get('summary', {}).get('final_verified', 0)} / {runtime_payload.get('summary', {}).get('total', 0)}**",
        f"- Output: `{SIM_OUT_MD}` and `{SIM_OUT_JSON}`",
        "",
        "## 4) Contract test generation (top 12)",
        f"- Contracts generated: **{len(contract_payload.get('contracts', []))}**",
        f"- Output: `{CONTRACTS_OUT}`",
        "",
        "## 5) Promotion list",
        f"- Promoted: **{len(promoted)}**",
        f"- Hold: **{len(hold)}**",
        "",
        "### Promoted",
        "| slug | type | risk | quality | runtime | tier |",
        "|---|---|---|---:|---:|---|",
    ]

    if promoted:
        for p in promoted:
            lines.append(
                f"| `{p['slug']}` | {p['type']} | {p['risk_level']} | {p['quality_score']} | {p['runtime_score']} | {p['tier']} |"
            )
    else:
        lines.append("| _none_ | - | - | - | - | - |")

    lines += [
        "",
        "### Hold",
        "| slug | type | risk | quality | runtime | tier | reason |",
        "|---|---|---|---:|---:|---|---|",
    ]

    for h in hold:
        reasons = []
        if not h["quality_pass"]:
            reasons.append("quality<80")
        if not h["runtime_pass"]:
            reasons.append("runtime gate fail")
        if not h["contract_top12"]:
            reasons.append("not in top12 contracts")
        lines.append(
            f"| `{h['slug']}` | {h['type']} | {h['risk_level']} | {h['quality_score']} | {h['runtime_score']} | {h['tier']} | {', '.join(reasons) if reasons else 'n/a'} |"
        )

    lines += [
        "",
        "## 6) Artifacts",
        f"- `{MERGED_OUT}`",
        f"- `{QUALITY_OUT_MD}`",
        f"- `{QUALITY_OUT_JSON}`",
        f"- `{SIM_OUT_MD}`",
        f"- `{SIM_OUT_JSON}`",
        f"- `{CONTRACTS_OUT}`",
        f"- `{PROMOTION_OUT_JSON}`",
    ]

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run V3 intake pipeline and output promotion list.")
    parser.add_argument("--skills", type=Path, default=DEFAULT_SKILLS, help="Path to v3 skill candidate JSON")
    parser.add_argument("--personalities", type=Path, default=DEFAULT_PERSONALITIES, help="Path to v3 personality candidate JSON")
    parser.add_argument("--merged-out", type=Path, default=MERGED_OUT)
    parser.add_argument("--quality-md", type=Path, default=QUALITY_OUT_MD)
    parser.add_argument("--quality-json", type=Path, default=QUALITY_OUT_JSON)
    parser.add_argument("--runtime-md", type=Path, default=SIM_OUT_MD)
    parser.add_argument("--runtime-json", type=Path, default=SIM_OUT_JSON)
    parser.add_argument("--contracts-out", type=Path, default=CONTRACTS_OUT)
    parser.add_argument("--promotion-md", type=Path, default=PROMOTION_OUT_MD)
    parser.add_argument("--promotion-json", type=Path, default=PROMOTION_OUT_JSON)
    parser.add_argument("--top-n", type=int, default=12, help="Top N packs for contract generation")
    args = parser.parse_args()

    skills_path = _pick_existing(args.skills, SKILL_FALLBACKS)
    personalities_path = _pick_existing(args.personalities, PERSONALITY_FALLBACKS)

    merge = merge_candidates(skills_path, personalities_path, args.merged_out)

    if merge.total == 0:
        print("No merged candidates produced. Check input files/content.")
        return 1

    merged_payload = _read_json(args.merged_out)
    candidates = merged_payload.get("candidates", [])
    if not isinstance(candidates, list):
        print("Merged payload malformed: `candidates` is not a list")
        return 1

    quality_payload = write_quality_reports(candidates, args.quality_md, args.quality_json)
    runtime_payload = write_runtime_reports(candidates, args.runtime_md, args.runtime_json)
    contract_payload = generate_contracts(candidates, quality_payload, runtime_payload, args.contracts_out, top_n=max(args.top_n, 1))
    promotion_payload = generate_promotion_list(
        candidates,
        quality_payload,
        runtime_payload,
        contract_payload,
        args.promotion_json,
        args.promotion_md,
        merge,
    )

    print(f"Merged candidates -> {args.merged_out}")
    print(f"Quality reports -> {args.quality_md} | {args.quality_json}")
    print(f"Runtime reports -> {args.runtime_md} | {args.runtime_json}")
    print(f"Contracts (top {max(args.top_n, 1)}) -> {args.contracts_out}")
    print(f"Promotion list -> {args.promotion_json}")
    print(f"Summary report -> {args.promotion_md}")
    print(
        "Promotion summary: "
        f"{promotion_payload['summary']['promoted']}/{promotion_payload['summary']['total']} promoted"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
