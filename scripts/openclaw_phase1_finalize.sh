#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/claw/.openclaw/workspace/botstore"
BOTSTORE_API="${BOTSTORE_API:-http://127.0.0.1:8787}"
TENANT_ID="${TENANT_ID:-default}"
RUNS="${RUNS:-5}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
PACKET_DIR="$ROOT/research/phase1-finalize-$STAMP"

mkdir -p "$PACKET_DIR"

echo "[phase1-finalize] api=$BOTSTORE_API tenant=$TENANT_ID runs=$RUNS"

echo "[phase1-finalize] single-run conformance"
(
  cd "$ROOT"
  BOTSTORE_API="$BOTSTORE_API" TENANT_ID="$TENANT_ID" ./scripts/openclaw_conformance.sh
)

cp "$ROOT/research/openclaw-conformance-result.json" "$PACKET_DIR/openclaw-conformance-result.json"
cp "$ROOT/research/openclaw-conformance-report.md" "$PACKET_DIR/openclaw-conformance-report.md"

if [[ -f /tmp/openclaw_phase1_exit_check.json ]]; then
  cp /tmp/openclaw_phase1_exit_check.json "$PACKET_DIR/openclaw_phase1_exit_check.json"
fi

echo "[phase1-finalize] burn-in conformance"
(
  cd "$ROOT"
  BOTSTORE_API="$BOTSTORE_API" TENANT_ID="$TENANT_ID" RUNS="$RUNS" ./scripts/openclaw_conformance_burnin.sh
)

cp "$ROOT/research/qa-loop/openclaw-burnin/summary.json" "$PACKET_DIR/burnin-summary.json"
cp "$ROOT/research/qa-loop/openclaw-burnin/summary.md" "$PACKET_DIR/burnin-summary.md"

python3 - <<PY
import json
from pathlib import Path
packet = Path("$PACKET_DIR")
summary = json.loads((packet / "burnin-summary.json").read_text())
verdict = summary.get("go_nogo", "UNKNOWN")
md = [
  "# OpenClaw Phase-1 Finalization",
  "",
  f"- Stamp: $STAMP",
  f"- API: $BOTSTORE_API",
  f"- Tenant: $TENANT_ID",
  f"- Burn-in runs: $RUNS",
  f"- Verdict: **{verdict}**",
  "",
  "## Included artifacts",
  "- openclaw-conformance-result.json",
  "- openclaw-conformance-report.md",
  "- openclaw_phase1_exit_check.json (if present)",
  "- burnin-summary.json",
  "- burnin-summary.md",
]
(packet / "phase1-finalization-report.md").write_text("\n".join(md) + "\n")
print(f"Wrote {(packet / 'phase1-finalization-report.md')}")
PY

echo "[phase1-finalize] done"
echo "[phase1-finalize] packet: $PACKET_DIR"
