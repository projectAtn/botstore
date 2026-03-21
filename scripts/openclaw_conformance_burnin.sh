#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/claw/.openclaw/workspace/botstore"
RUNS="${RUNS:-5}"
BOTSTORE_API="${BOTSTORE_API:-http://127.0.0.1:8787}"
TENANT_ID="${TENANT_ID:-default}"
OUT_DIR="$ROOT/research/qa-loop/openclaw-burnin"

mkdir -p "$OUT_DIR"

echo "[burnin] runs=$RUNS api=$BOTSTORE_API tenant=$TENANT_ID"

for i in $(seq 1 "$RUNS"); do
  ts="$(date -u +%Y%m%dT%H%M%SZ)"
  echo "[burnin] run $i/$RUNS @ $ts"
  (
    cd "$ROOT"
    BOTSTORE_API="$BOTSTORE_API" TENANT_ID="$TENANT_ID" ./scripts/openclaw_conformance.sh
  )
  cp "$ROOT/research/openclaw-conformance-result.json" "$OUT_DIR/run-${i}-${ts}.json"
  cp "$ROOT/research/openclaw-conformance-report.md" "$OUT_DIR/run-${i}-${ts}.md"

done

python3 "$ROOT/scripts/phase1_go_nogo.py" --glob "$OUT_DIR/*.json" --out-json "$OUT_DIR/summary.json" --out-md "$OUT_DIR/summary.md"

echo "[burnin] complete"
echo "[burnin] summary: $OUT_DIR/summary.json"
