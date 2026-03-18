#!/usr/bin/env bash
set -euo pipefail

cd /app/api

echo "[start_api] running db migrations"
python /app/scripts/db_migrate.py || echo "[start_api] migration step failed; continuing (startup fallback enabled)"

echo "[start_api] starting uvicorn"
exec uvicorn app.main:app --host 0.0.0.0 --port 8787
