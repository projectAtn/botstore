#!/usr/bin/env python3
"""V2 intake pipeline for candidate skill/personality packs.

Pipeline steps:
1) Merge v2 skill + personality candidate sources.
2) Run existing checks:
   - scripts/quality_check_candidates.py
   - scripts/runtime_simulation_verify.py
3) Produce intake summary report with pass/fail + delist recommendations.

By default this pipeline is non-destructive to existing v1 candidate source:
- It temporarily swaps research/candidate-packs-v1.json with merged v2 payload
  while checks run, then restores the original file.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
SCRIPTS = ROOT / "scripts"

DEFAULT_SKILLS = RESEARCH / "candidate-skills-v2.json"
DEFAULT_PERSONALITIES = RESEARCH / "candidate-personalities-v2.json"

MERGED_OUT = RESEARCH / "candidate-packs-v2.json"
SUMMARY_OUT = RESEARCH / "v2-intake-summary.md"

LEGACY_SOURCE = RESEARCH / "candidate-packs-v1.json"
BACKUP_SOURCE = RESEARCH / "candidate-packs-v1.backup-for-v2-intake.json"

QUALITY_JSON_HINT = RESEARCH / "candidate-packs-quality-report.md"
SIM_RESULT = RESEARCH / "runtime-simulation-result.json"
SIM_MD = RESEARCH / "runtime-simulation-report.md"


@dataclass
class MergeResult:
    merged_path: Path
    total: int
    skills: int
    personalities: int
    duplicates_overwritten: list[str]
    warnings: list[str]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_candidates(payload: Any, expected_type: str, source_path: Path) -> list[dict[str, Any]]:
    """Accept flexible payload structures and normalize to candidate list."""
    warnings: list[str] = []

    if isinstance(payload, list):
        raw = payload
    elif isinstance(payload, dict):
        for key in ("candidates", "skills", "personalities", "items", "data"):
            if isinstance(payload.get(key), list):
                raw = payload[key]
                break
        else:
            raw = []
            warnings.append(f"No list field found in {source_path.name}; expected candidates/skills/personalities/items/data")
    else:
        raw = []
        warnings.append(f"Unsupported JSON structure in {source_path.name}")

    normalized: list[dict[str, Any]] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            warnings.append(f"Skipped non-object item at {source_path.name}[{i}]")
            continue
        item = dict(item)
        item.setdefault("type", expected_type)
        normalized.append(item)

    return normalized


def merge_candidates(skill_file: Path, personality_file: Path, out_path: Path) -> MergeResult:
    warnings: list[str] = []

    sources: list[tuple[Path, str]] = [
        (skill_file, "skill"),
        (personality_file, "personality"),
    ]

    combined: list[dict[str, Any]] = []
    skill_count = 0
    personality_count = 0

    for path, expected_type in sources:
        if not path.exists():
            warnings.append(f"Missing input file: {path}")
            continue

        payload = _read_json(path)
        items = _extract_candidates(payload, expected_type, path)

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
        "generatedAt": datetime.now(timezone.utc).date().isoformat(),
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


def run_script(script_path: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    log = "\n".join(
        x for x in [proc.stdout.strip(), proc.stderr.strip()] if x
    )
    return proc.returncode == 0, log


def _load_runtime_result() -> dict[str, Any]:
    if not SIM_RESULT.exists():
        return {}
    try:
        return _read_json(SIM_RESULT)
    except Exception:
        return {}


def write_summary_report(
    out_path: Path,
    merge: MergeResult,
    quality_ok: bool,
    quality_log: str,
    sim_ok: bool,
    sim_log: str,
    runtime_payload: dict[str, Any],
) -> None:
    results = runtime_payload.get("results", []) if isinstance(runtime_payload, dict) else []
    verified = set(runtime_payload.get("verified_slugs", []) if isinstance(runtime_payload, dict) else [])
    delisted = set(runtime_payload.get("delisted_slugs", []) if isinstance(runtime_payload, dict) else [])

    lines: list[str] = [
        "# V2 Intake Pipeline Summary",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
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
        "## 2) Existing checks",
        f"- `quality_check_candidates.py`: {'PASS' if quality_ok else 'FAIL'}",
        f"- `runtime_simulation_verify.py`: {'PASS' if sim_ok else 'FAIL'}",
        "",
        "## 3) Runtime simulation outcome",
    ]

    if not results:
        lines.append("- No runtime simulation result payload found.")
    else:
        lines += [
            f"- Verified slugs: **{len(verified)}**",
            f"- Delist recommendations: **{len(delisted)}**",
            "",
            "| slug | risk | score | required | final_verified | recommendation |",
            "|---|---|---:|---:|---|---|",
        ]
        for r in results:
            slug = r.get("slug", "?")
            risk = r.get("risk_level", "?")
            score = r.get("score", "?")
            req = r.get("required_score", "?")
            fv = bool(r.get("final_verified", False))
            rec = "KEEP" if fv else "DELIST"
            lines.append(
                f"| `{slug}` | {risk} | {score} | {req} | {'✅' if fv else '❌'} | **{rec}** |"
            )

    lines += [
        "",
        "## 4) Execution logs (trimmed)",
        "",
        "### quality_check_candidates.py",
        "```text",
        (quality_log or "(no output)")[:4000],
        "```",
        "",
        "### runtime_simulation_verify.py",
        "```text",
        (sim_log or "(no output)")[:4000],
        "```",
        "",
        "## 5) Output artifacts",
        f"- `{QUALITY_JSON_HINT}`",
        f"- `{SIM_MD}`",
        f"- `{SIM_RESULT}`",
    ]

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge v2 candidate inputs, run checks, and summarize intake results.")
    parser.add_argument("--skills", type=Path, default=DEFAULT_SKILLS, help="Path to v2 skill candidate JSON")
    parser.add_argument("--personalities", type=Path, default=DEFAULT_PERSONALITIES, help="Path to v2 personality candidate JSON")
    parser.add_argument("--merged-out", type=Path, default=MERGED_OUT, help="Merged candidate output JSON path")
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT, help="Summary report output path")
    parser.add_argument("--in-place", action="store_true", help="Replace candidate-packs-v1.json with merged v2 (no restore)")
    args = parser.parse_args()

    merge = merge_candidates(args.skills, args.personalities, args.merged_out)

    if not merge.total:
        print("No merged candidates produced. Check input paths/content.")
        write_summary_report(args.summary_out, merge, False, "skipped", False, "skipped", {})
        return 1

    if LEGACY_SOURCE.exists():
        shutil.copy2(LEGACY_SOURCE, BACKUP_SOURCE)

    # Feed existing scripts by swapping expected input file.
    shutil.copy2(args.merged_out, LEGACY_SOURCE)

    quality_ok, quality_log = run_script(SCRIPTS / "quality_check_candidates.py")
    sim_ok, sim_log = run_script(SCRIPTS / "runtime_simulation_verify.py")

    runtime_payload = _load_runtime_result()
    write_summary_report(
        args.summary_out,
        merge,
        quality_ok,
        quality_log,
        sim_ok,
        sim_log,
        runtime_payload,
    )

    if not args.in_place and BACKUP_SOURCE.exists():
        shutil.move(BACKUP_SOURCE, LEGACY_SOURCE)
    elif args.in_place and BACKUP_SOURCE.exists():
        BACKUP_SOURCE.unlink(missing_ok=True)

    print(f"Merged candidates -> {args.merged_out}")
    print(f"Summary report -> {args.summary_out}")
    print(f"Checks: quality={'PASS' if quality_ok else 'FAIL'}, runtime={'PASS' if sim_ok else 'FAIL'}")

    return 0 if (quality_ok and sim_ok) else 2


if __name__ == "__main__":
    raise SystemExit(main())
