#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_once() -> int:
    mode = os.getenv("WORKER_MODE", "qa_scheduler").strip().lower()
    if mode == "qa_scheduler":
        cmd = [sys.executable, str(ROOT / "scripts" / "ci_gate_run_all.py")]
    elif mode == "ranking_only":
        cmd = [sys.executable, str(ROOT / "scripts" / "ranking_eval_ci.py")]
    else:
        print(f"[{datetime.now(timezone.utc).isoformat()}] Unknown WORKER_MODE={mode}; sleeping")
        return 0

    print(f"[{datetime.now(timezone.utc).isoformat()}] worker run: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT)
    print(f"[{datetime.now(timezone.utc).isoformat()}] worker exit={proc.returncode}")
    return proc.returncode


def main() -> int:
    interval = int(os.getenv("WORKER_INTERVAL_SECONDS", "900"))
    run_immediately = os.getenv("WORKER_RUN_IMMEDIATELY", "true").lower() in {"1", "true", "yes"}

    if run_immediately:
        run_once()

    while True:
        time.sleep(max(30, interval))
        run_once()


if __name__ == "__main__":
    raise SystemExit(main())
