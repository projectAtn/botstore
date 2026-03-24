#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BOTSTORE_API:-http://127.0.0.1:8787}"
TENANT_ID="${TENANT_ID:-default}"
ROOT="/Users/claw/.openclaw/workspace/botstore"
OUT_JSON="$ROOT/research/openclaw-conformance-result.json"
OUT_MD="$ROOT/research/openclaw-conformance-report.md"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

step() { printf "[%s] %s\n" "$(date +%H:%M:%S)" "$*"; }

json_escape() {
  python3 - <<'PY'
import json,sys
print(json.dumps(sys.stdin.read()))
PY
}

step "Health check: $BASE_URL/health"
HEALTH="$(curl -fsS "$BASE_URL/health")"

step "Running control-plane smoke"
(
  cd "$ROOT"
  BOTSTORE_API="$BASE_URL" ./scripts/control_plane_smoke.sh >/tmp/control_plane_smoke.log 2>&1
)

step "Running OpenClaw adapter smoke"
(
  cd "$ROOT"
  BOTSTORE_API="$BASE_URL" TENANT_ID="$TENANT_ID" ./scripts/openclaw_adapter_smoke.sh >/tmp/openclaw_adapter_smoke.log 2>&1
)

step "Running typed action map check"
(
  cd "$ROOT"
  python3 ./scripts/openclaw_typed_map_check.py >/tmp/openclaw_typed_map_check.log 2>&1
)

step "Running auth bypass check"
(
  cd "$ROOT"
  python3 ./scripts/openclaw_auth_bypass_check.py >/tmp/openclaw_auth_bypass_check.log 2>&1
)

step "Collecting policy/profile/status evidence"
STATUS_PATH="/tmp/openclaw_status_control_plane.json"
POLICY_LOG_PATH="/tmp/openclaw_policy_decision_log.json"
TENANT_PROFILE_PATH="/tmp/openclaw_tenant_profile.json"
HEALTH_PATH="/tmp/openclaw_health.json"

curl -fsS "$BASE_URL/status/control-plane?tenant_id=$TENANT_ID&lookback_days=30" > "$STATUS_PATH"
curl -fsS "$BASE_URL/policy/decision-log?tenant_id=$TENANT_ID&limit=50" > "$POLICY_LOG_PATH"
curl -fsS "$BASE_URL/policy/tenant-profile/$TENANT_ID" > "$TENANT_PROFILE_PATH"
printf "%s" "$HEALTH" > "$HEALTH_PATH"

python3 - <<PY
import json, pathlib
out_json = pathlib.Path("$OUT_JSON")
out_md = pathlib.Path("$OUT_MD")
health = json.loads(pathlib.Path("$HEALTH_PATH").read_text())
status = json.loads(pathlib.Path("$STATUS_PATH").read_text())
policy_log = json.loads(pathlib.Path("$POLICY_LOG_PATH").read_text())
tenant_profile = json.loads(pathlib.Path("$TENANT_PROFILE_PATH").read_text())
typed_map = json.loads(pathlib.Path("$ROOT/research/openclaw-typed-map-check.json").read_text())
auth_bypass = json.loads(pathlib.Path("$ROOT/research/openclaw-auth-bypass-check.json").read_text())

payload = {
  "generated_at": "$NOW",
  "base_url": "$BASE_URL",
  "tenant_id": "$TENANT_ID",
  "checks": {
    "health": health,
    "status_control_plane": status,
    "policy_decision_log": policy_log,
    "tenant_profile": tenant_profile,
    "typed_action_map": typed_map,
    "auth_bypass_check": auth_bypass
  },
  "logs": {
    "control_plane_smoke_log": "/tmp/control_plane_smoke.log",
    "openclaw_adapter_smoke_log": "/tmp/openclaw_adapter_smoke.log",
    "openclaw_typed_map_check_log": "/tmp/openclaw_typed_map_check.log",
    "openclaw_auth_bypass_check_log": "/tmp/openclaw_auth_bypass_check.log"
  }
}
out_json.write_text(json.dumps(payload, indent=2))

md = [
  "# OpenClaw Conformance Report",
  "",
  f"- Generated: {payload['generated_at']}",
  f"- Base URL: {payload['base_url']}",
  f"- Tenant: {payload['tenant_id']}",
  "",
  "## Checks",
  "- ✅ health",
  "- ✅ control_plane_smoke.sh",
  "- ✅ openclaw_adapter_smoke.sh",
  "- ✅ openclaw_typed_map_check.py",
  "- ✅ openclaw_auth_bypass_check.py",
  "- ✅ status/control-plane",
  "- ✅ policy/decision-log",
  "- ✅ policy/tenant-profile",
  "",
  "## Artifacts",
  "- JSON: " + str(out_json),
  "- Logs:",
  "  - /tmp/control_plane_smoke.log",
  "  - /tmp/openclaw_adapter_smoke.log",
  "  - /tmp/openclaw_typed_map_check.log",
  "  - /tmp/openclaw_auth_bypass_check.log",
]
out_md.write_text("\n".join(md) + "\n")
print(f"Wrote {out_json}")
print(f"Wrote {out_md}")
PY

step "Validating phase-1 exit artifact"
python3 "$ROOT/scripts/phase1_exit_check.py" --input "$OUT_JSON" > /tmp/openclaw_phase1_exit_check.json

step "Conformance complete"
