#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOB_QUEUE_PATH = Path(os.getenv("JOB_QUEUE_PATH", str(ROOT / "research" / "job-queue.jsonl")))
JOB_STATUS_PATH = Path(os.getenv("JOB_STATUS_PATH", str(ROOT / "research" / "job-status.json")))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_cmd(cmd: list[str]) -> int:
    print(f"[{utc_now()}] worker run: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT)
    print(f"[{utc_now()}] worker exit={proc.returncode}")
    return proc.returncode


def load_status() -> dict:
    if not JOB_STATUS_PATH.exists():
        return {}
    try:
        return json.loads(JOB_STATUS_PATH.read_text())
    except Exception:
        return {}


def save_status(status: dict) -> None:
    JOB_STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    JOB_STATUS_PATH.write_text(json.dumps(status, indent=2))


def run_once() -> int:
    mode = os.getenv("WORKER_MODE", "qa_scheduler").strip().lower()
    if mode == "qa_scheduler":
        cmd = [sys.executable, str(ROOT / "scripts" / "ci_gate_run_all.py")]
    elif mode == "ranking_only":
        cmd = [sys.executable, str(ROOT / "scripts" / "ranking_eval_ci.py")]
    elif mode == "queue_consumer":
        return run_queue_once()
    else:
        print(f"[{utc_now()}] Unknown WORKER_MODE={mode}; sleeping")
        return 0

    return run_cmd(cmd)


def read_queue() -> list[dict]:
    if not JOB_QUEUE_PATH.exists():
        return []
    rows = []
    for line in JOB_QUEUE_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def map_job_to_cmd(job: dict) -> list[str] | None:
    jt = (job or {}).get("job_type")
    if jt == "ci_gate_run_all":
        return [sys.executable, str(ROOT / "scripts" / "ci_gate_run_all.py")]
    if jt == "ranking_eval_ci":
        return [sys.executable, str(ROOT / "scripts" / "ranking_eval_ci.py")]
    if jt == "team_qa_v3_plus_reddit":
        return [
            sys.executable,
            str(ROOT / "scripts" / "team_pack_qa_flexible.py"),
            "--teams",
            str(ROOT / "research" / "team-packs-v3.json"),
            "--scenarios",
            str(ROOT / "research" / "team-pack-qa-scenarios-v3-plus-reddit-intake.json"),
            "--out-json",
            str(ROOT / "research" / "team-pack-qa-result-v3-plus-reddit.json"),
            "--out-md",
            str(ROOT / "research" / "team-pack-qa-report-v3-plus-reddit.md"),
            "--patched-out",
            str(ROOT / "research" / "team-packs-v3-plus-reddit-patched.json"),
        ]
    return None


def run_queue_once() -> int:
    status = load_status()
    rows = read_queue()

    # pick first queued/unknown job
    target = None
    for r in rows:
        jid = r.get("job_id")
        st = (status.get(jid) or {}).get("status")
        if st in {"running", "succeeded"}:
            continue
        target = r
        break

    if not target:
        print(f"[{utc_now()}] queue_consumer: no queued jobs")
        return 0

    job_id = target.get("job_id")
    cmd = map_job_to_cmd(target)
    if not cmd:
        status[job_id] = {
            **(status.get(job_id) or {}),
            "job_id": job_id,
            "job_type": target.get("job_type"),
            "status": "failed",
            "error": f"unsupported job_type {target.get('job_type')}",
            "updated_at": utc_now(),
        }
        save_status(status)
        return 1

    status[job_id] = {
        **(status.get(job_id) or {}),
        "job_id": job_id,
        "job_type": target.get("job_type"),
        "status": "running",
        "started_at": utc_now(),
        "updated_at": utc_now(),
    }
    save_status(status)

    rc = run_cmd(cmd)
    status[job_id] = {
        **(status.get(job_id) or {}),
        "status": "succeeded" if rc == 0 else "failed",
        "exit_code": rc,
        "finished_at": utc_now(),
        "updated_at": utc_now(),
    }
    save_status(status)
    return rc


def main() -> int:
    interval = int(os.getenv("WORKER_INTERVAL_SECONDS", "900"))
    run_immediately = os.getenv("WORKER_RUN_IMMEDIATELY", "true").lower() in {"1", "true", "yes"}

    if run_immediately:
        run_once()

    while True:
        time.sleep(max(15, interval))
        run_once()


if __name__ == "__main__":
    raise SystemExit(main())
