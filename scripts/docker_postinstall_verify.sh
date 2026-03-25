#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/.openclaw/workspace/botstore}"
cd "$ROOT"

echo "[1/6] Docker binaries"
docker --version
docker compose version

echo "[2/6] Docker engine status"
if ! docker info >/dev/null 2>&1; then
  echo "Docker engine is not running. Start Docker Desktop first." >&2
  exit 1
fi

echo "[3/6] Compose up"
docker compose up -d --build

echo "[4/6] Health check"
for i in {1..30}; do
  code=$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8787/health || true)
  if [[ "$code" == "200" ]]; then
    break
  fi
  sleep 2
done
curl -sS http://127.0.0.1:8787/health

echo "[5/6] Queue job smoke"
JOB_JSON=$(curl -sS -X POST http://127.0.0.1:8787/jobs/enqueue \
  -H "Content-Type: application/json" \
  -d '{"job_type":"ranking_eval_ci","payload":{}}')
echo "$JOB_JSON"
JOB_ID=$(echo "$JOB_JSON" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read()).get("job_id",""))')

if [[ -n "$JOB_ID" ]]; then
  for i in {1..20}; do
    ST=$(curl -sS "http://127.0.0.1:8787/jobs/$JOB_ID")
    echo "$ST"
    STATUS=$(echo "$ST" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read()).get("status",""))')
    [[ "$STATUS" == "succeeded" || "$STATUS" == "failed" ]] && break
    sleep 3
  done
fi

echo "[6/6] Full gate"
python3 scripts/ci_gate_run_all.py

echo "DONE"
