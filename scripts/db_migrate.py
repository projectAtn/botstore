#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "api"


def main() -> int:
    cmd = ["alembic", "-c", "alembic.ini", "upgrade", "head"]
    env = os.environ.copy()
    print(f"Running: {' '.join(cmd)} in {API_DIR}")
    proc = subprocess.run(cmd, cwd=API_DIR, env=env)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
