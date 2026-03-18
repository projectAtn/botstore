#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "research" / "team-must-pass-policy-v1.json"
QA_RESULT = ROOT / "research" / "team-pack-qa-result-v3-high-pressure.json"
OUT = ROOT / "research" / "team-must-pass-gate-report-v1.json"


def main() -> int:
    policy = json.loads(POLICY.read_text())
    qa = json.loads(QA_RESULT.read_text())

    by_scenario = {r["scenario_id"]: r for r in qa.get("scenarios", [])}

    team_rows = []
    all_ok = True
    for t in policy.get("teams", []):
        team_slug = t["team_slug"]
        req = t.get("must_pass_scenarios", [])
        missing = []
        failed = []
        passed = 0
        for sid in req:
            row = by_scenario.get(sid)
            if not row:
                missing.append(sid)
                continue
            if row.get("pass"):
                passed += 1
            else:
                failed.append(sid)

        required_pass_count = int(t.get("required_pass_count", len(req)))
        ok = (passed >= required_pass_count) and (not missing) and (not failed)
        if not ok:
            all_ok = False

        team_rows.append(
            {
                "team_slug": team_slug,
                "required": len(req),
                "required_pass_count": required_pass_count,
                "passed": passed,
                "ok": ok,
                "failed_scenarios": failed,
                "missing_scenarios": missing,
            }
        )

    payload = {
        "status": "pass" if all_ok else "fail",
        "policy_file": str(POLICY.relative_to(ROOT)),
        "qa_result_file": str(QA_RESULT.relative_to(ROOT)),
        "teams": team_rows,
        "summary": {
            "total_teams": len(team_rows),
            "passed_teams": sum(1 for r in team_rows if r["ok"]),
            "failed_teams": sum(1 for r in team_rows if not r["ok"]),
        },
    }
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {OUT}")
    print(json.dumps(payload["summary"], indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
