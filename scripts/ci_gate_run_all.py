#!/usr/bin/env python3
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research" / "ci-gate-run-all-report.json"

STEPS = [
    {
        "name": "regression_ci",
        "cmd": [sys.executable, str(ROOT / "scripts" / "regression_ci.py")],
        "required": True,
    },
    {
        "name": "ranking_eval_ci",
        "cmd": [sys.executable, str(ROOT / "scripts" / "ranking_eval_ci.py")],
        "required": True,
    },
    {
        "name": "pack_test_runner",
        "cmd": [sys.executable, str(ROOT / "scripts" / "pack_test_runner.py")],
        "required": True,
    },
]


def run_step(step: dict) -> dict:
    started = datetime.now(timezone.utc).isoformat()
    try:
        proc = subprocess.run(step["cmd"], cwd=ROOT, capture_output=True, text=True)
        return {
            "name": step["name"],
            "required": step.get("required", True),
            "started": started,
            "exit_code": proc.returncode,
            "ok": proc.returncode == 0,
            "stdout": proc.stdout[-8000:],
            "stderr": proc.stderr[-4000:],
        }
    except Exception as e:
        return {
            "name": step["name"],
            "required": step.get("required", True),
            "started": started,
            "exit_code": -1,
            "ok": False,
            "stdout": "",
            "stderr": f"Exception: {e}",
        }


def main() -> int:
    results = [run_step(s) for s in STEPS]
    required_failures = [r for r in results if r["required"] and not r["ok"]]

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "steps": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r["ok"]),
            "failed": sum(1 for r in results if not r["ok"]),
            "required_failed": len(required_failures),
            "status": "pass" if not required_failures else "fail",
        },
    }

    REPORT.write_text(json.dumps(payload, indent=2))

    print(f"Wrote {REPORT}")
    for r in results:
        marker = "✅" if r["ok"] else "❌"
        print(f"{marker} {r['name']} (exit={r['exit_code']})")

    if required_failures:
        print("\nRequired step failures:")
        for r in required_failures:
            print(f"- {r['name']}")
        return 1

    print("\nCI gate run-all: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
