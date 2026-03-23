#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8787}"
TENANT_ID="${TENANT_ID:-default}"
RUNTIME_ID="${RUNTIME_ID:-openclaw}"
RUNTIME_BAND="${RUNTIME_BAND:-B}"
TS="$(date +%s%N)"

log() {
  printf "\n[%s] %s\n" "$(date +%H:%M:%S)" "$*"
}

json_get() {
  local path="$1"
  local payload="${2:-}"
  if [[ -z "$payload" ]]; then
    payload="$(cat)"
  fi
  python3 - "$path" "$payload" <<'PY'
import json, sys
path = sys.argv[1]
obj = json.loads(sys.argv[2])
cur = obj
for part in path.split('.'):
    if part == '':
        continue
    if isinstance(cur, list):
        idx = int(part)
        cur = cur[idx]
    elif isinstance(cur, dict):
        if part not in cur:
            raise KeyError(part)
        cur = cur[part]
    else:
        raise KeyError(part)
if isinstance(cur, (dict, list)):
    print(json.dumps(cur))
else:
    print(cur)
PY
}

api() {
  local method="$1"
  local path="$2"
  local data="${3:-}"
  if [[ -n "$data" ]]; then
    curl -fsS -X "$method" "$BASE_URL$path" \
      -H 'content-type: application/json' \
      -d "$data"
  else
    curl -fsS -X "$method" "$BASE_URL$path"
  fi
}

log "Checking API health at $BASE_URL"
health="$(api GET '/health')"
echo "$health" | json_get "ok" >/dev/null

CREATOR_NAME="Smoke Creator $TS"
PACK_SLUG="smoke-deploy-guardian-$TS"
TASK_ID="task-smoke-$TS"

log "Creating creator"
creator_resp="$(api POST '/creators' "$(cat <<JSON
{"name":"$CREATOR_NAME","verification":"verified","trust_score":0.95}
JSON
)")"
creator_id="$(echo "$creator_resp" | json_get 'id')"

log "Creating pack"
pack_resp="$(api POST '/packs' "$(cat <<JSON
{
  "slug":"$PACK_SLUG",
  "title":"Smoke Deploy Guardian",
  "type":"skill",
  "version":"1.0.0",
  "description":"Smoke test rollback + alerts",
  "risk_level":"medium",
  "scopes":["log.read","message.send"],
  "creator_id":$creator_id
}
JSON
)")"
pack_id="$(echo "$pack_resp" | json_get 'id')"

log "Creating explicit pack version"
version_resp="$(api POST "/packs/$pack_id/versions" "$(cat <<JSON
{
  "semver":"1.0.1",
  "manifest_version":"v2",
  "capabilities_declared":["deploy.rollback","incident.triage"],
  "scopes_requested":["log.read","message.send"],
  "actions_supported":["deploy.rollback","message.send"],
  "compatible_runtimes":["$RUNTIME_ID"],
  "policy_requirements":{"runtime_band_max":"B"},
  "verification_tier":"tier2_verified"
}
JSON
)")"
pack_version_id="$(echo "$version_resp" | json_get 'id')"
artifact_digest="$(echo "$version_resp" | json_get 'artifact_digest')"

log "Upserting trust evidence + local verify"
trust_resp="$(api PUT "/packs/$pack_id/versions/$pack_version_id/trust" "$(cat <<JSON
{
  "artifact_uri":"oci://botstore/$PACK_SLUG:1.0.1",
  "signature_refs":["sig://local/$PACK_SLUG"],
  "sbom_ref":"sbom://local/$PACK_SLUG.spdx.json",
  "attestation_refs":["att://build/$PACK_SLUG","att://verify/$PACK_SLUG","att://conformance/$PACK_SLUG","att://qa/$PACK_SLUG","att://prov/$PACK_SLUG"]
}
JSON
)")"
_="$(echo "$trust_resp" | json_get 'ok')"

verify_resp="$(api POST "/packs/$pack_id/versions/$pack_version_id/trust/verify-local" '{}')"
verify_ok="$(echo "$verify_resp" | json_get 'ok')"
if [[ "$verify_ok" != "True" && "$verify_ok" != "true" ]]; then
  echo "Expected trust verify ok=true, got: $verify_ok" >&2
  exit 1
fi

log "Running install-by-capability-v2"
install_resp="$(api POST '/agent/install-by-capability-v2' "$(cat <<JSON
{
  "task_id":"$TASK_ID",
  "tenant_id":"$TENANT_ID",
  "user_id":"telegram:smoke-user",
  "agent_id":"agent-smoke",
  "runtime_id":"$RUNTIME_ID",
  "runtime_version":"0.2.0",
  "runtime_band":"$RUNTIME_BAND",
  "required_capabilities":["deploy.rollback"],
  "enable_safe_exploration":true,
  "exploration_rate":0.05
}
JSON
)")"
attempt_id="$(echo "$install_resp" | json_get 'attempt_id')"
selected_pack_version_id="$(echo "$install_resp" | json_get 'selected.pack_version_id')"
selected_digest="$(echo "$install_resp" | json_get 'selected.artifact_digest')"

log "Authorizing sensitive action"
auth_resp="$(api POST '/agent/action-authorize' "$(cat <<JSON
{
  "attempt_id":"$attempt_id",
  "pack_version_id":$selected_pack_version_id,
  "artifact_digest":"$selected_digest",
  "requested_action":"message.send",
  "requested_scope":"message.send",
  "justification":"smoke test notification"
}
JSON
)")"
# ensure decision key exists
_="$(echo "$auth_resp" | json_get 'decision')"

log "Submitting successful outcome-v2"
outcome_ok_resp="$(api POST '/agent/outcome-v2' "$(cat <<JSON
{
  "attempt_id":"$attempt_id",
  "task_id":"$TASK_ID",
  "tenant_id":"$TENANT_ID",
  "task_class":"ops.devops",
  "runtime_id":"$RUNTIME_ID",
  "runtime_version":"0.2.0",
  "result":"success",
  "latency_ms":1200,
  "human_intervention":"none",
  "task_completed_after_install":true,
  "observed_scopes":["log.read","message.send"],
  "side_effect_counts":{"alerts_sent":1},
  "incident_flag":false,
  "privacy_mode":"standard"
}
JSON
)")"
echo "$outcome_ok_resp" | json_get 'quarantined' >/dev/null

log "Submitting violating outcome-v2 to trigger quarantine"
outcome_bad_resp="$(api POST '/agent/outcome-v2' "$(cat <<JSON
{
  "attempt_id":"$attempt_id",
  "task_id":"${TASK_ID}-violation",
  "tenant_id":"$TENANT_ID",
  "runtime_id":"$RUNTIME_ID",
  "result":"fail",
  "task_completed_after_install":false,
  "observed_scopes":["payment.charge"],
  "incident_flag":true
}
JSON
)")"
qflag="$(echo "$outcome_bad_resp" | json_get 'quarantined')"
if [[ "$qflag" != "True" && "$qflag" != "true" ]]; then
  echo "Expected quarantine=true, got: $qflag" >&2
  exit 1
fi

log "Fetching analytics and policy logs"
status_resp="$(api GET "/status/control-plane?tenant_id=$TENANT_ID&lookback_days=30")"
replay_resp="$(api GET "/analytics/replay-dataset?tenant_id=$TENANT_ID&limit=50")"
shadow_resp="$(api GET "/analytics/shadow-ranker-eval?tenant_id=$TENANT_ID&limit=50")"
policy_log_resp="$(api GET "/policy/decision-log?tenant_id=$TENANT_ID&limit=50")"

# basic assertions
_="$(echo "$status_resp" | json_get 'north_star.trusted_capability_resolution_rate')"
_="$(echo "$replay_resp" | json_get 'count')"
_="$(echo "$shadow_resp" | json_get 'same_winner_rate')"
_="$(echo "$policy_log_resp" | json_get 'count')"

log "Smoke test passed"
echo "creator_id=$creator_id"
echo "pack_id=$pack_id"
echo "pack_version_id=$pack_version_id"
echo "attempt_id=$attempt_id"
echo "artifact_digest=$artifact_digest"
