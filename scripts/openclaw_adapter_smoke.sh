#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/claw/.openclaw/workspace/botstore"
API="${BOTSTORE_API:-http://127.0.0.1:8787}"

printf "[openclaw-smoke] API=%s\n" "$API"

curl -fsS "$API/health" >/dev/null

(
  cd "$ROOT/plugin/python"
  BOTSTORE_API="$API" python3 demo_openclaw_adapter_e2e.py
)

echo "[openclaw-smoke] OK"
