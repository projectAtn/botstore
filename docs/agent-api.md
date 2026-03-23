# BotStore Agent API (autonomous mode)

## 1) Search missing capabilities
`POST /agent/search-capabilities`

```json
{
  "user_id": "telegram:8258812165",
  "runtime": "openclaw",
  "intent": "book flight and notify calendar",
  "missing_capabilities": ["calendar.write", "message.send"],
  "limit": 5
}
```

## 2) Install by capability (legacy)
`POST /agent/install-by-capability`

```json
{
  "user_id": "telegram:8258812165",
  "runtime": "openclaw",
  "required_capabilities": ["web.search", "calendar.write"]
}
```

## 3) Install by capability transaction (v2, digest-pinned)
`POST /agent/install-by-capability-v2`

```json
{
  "task_id": "task_abc123",
  "tenant_id": "default",
  "user_id": "telegram:8258812165",
  "agent_id": "agent-42",
  "runtime_id": "openclaw",
  "runtime_version": "0.2.0",
  "runtime_band": "B",
  "required_capabilities": ["calendar.ops", "crm.sync"],
  "limit": 10,
  "enable_safe_exploration": true,
  "exploration_rate": 0.05,
  "install_target_preference": "agent_workspace",
  "allow_gateway_plugin_store_autonomous": false
}
```

`enable_safe_exploration` only explores inside a policy-equivalent, lower/equal-risk, verified safe bucket.

Response includes:
- `attempt_id`
- `candidate_snapshot_id`
- selected `pack_version_id` + `artifact_digest`
- policy decision/explanations
- optional signed approval grant metadata

Trust precondition: candidate pack versions must be trust-verified (`verification_state=verified`).

## 4) Pack trust evidence + verification (required before autonomous install)
- `PUT /packs/{pack_id}/versions/{version_id}/trust`
- `POST /packs/{pack_id}/versions/{version_id}/trust/verify-local`

## 5) Action-time authorization (proof-carrying approval)
`POST /agent/action-authorize`

```json
{
  "attempt_id": "att_...",
  "pack_version_id": 12,
  "artifact_digest": "sha256:...",
  "requested_action": "message.send",
  "requested_scope": "message.send",
  "runtime_attestation": "optional",
  "justification": "Send escalation notice"
}
```

## 6) Approval checkpoint pause/resume (session-native approvals)
- `POST /agent/approval-checkpoint/pause`
- `POST /agent/approval-checkpoint/resume`

Use this when execution is paused awaiting human approval and must resume the same lane safely.

## 7) Evaluate policy before autonomous install/use
`POST /agent/policy-evaluate`

For native policy DSL evaluation, use:
`POST /policy/bps/evaluate`

Policy admin/export endpoints:
- `POST /policy/bundles`
- `GET /policy/bundles`
- `PUT /policy/tenant-profile`
- `GET /policy/tenant-profile/{tenant_id}`
- `GET /policy/decision-log`

Response includes structured policy explanation fields:
- `policy_schema_version`
- `reason_codes[]`
- `blocking_conditions[]`
- `required_approvals[]`
- `runtime_requirements`
- `policy_hash`

```json
{
  "user_id": "telegram:8258812165",
  "runtime": "openclaw",
  "pack_id": 2
}
```

## 8) Submit outcome telemetry (legacy)
`POST /agent/outcome`

```json
{
  "user_id": "telegram:8258812165",
  "task_id": "task_abc123",
  "runtime": "openclaw",
  "pack_id": 2,
  "success": true,
  "latency_ms": 1840
}
```

## 9) Submit outcome telemetry (v2, attempt-bound)
`POST /agent/outcome-v2`

```json
{
  "attempt_id": "att_...",
  "task_id": "task_abc123",
  "tenant_id": "default",
  "task_class": "ops.devops",
  "runtime_id": "openclaw",
  "runtime_version": "0.2.0",
  "result": "success",
  "latency_ms": 1840,
  "human_intervention": "none",
  "task_completed_after_install": true,
  "observed_scopes": ["log.read"],
  "side_effect_counts": {"deploy": 0},
  "incident_flag": false,
  "privacy_mode": "standard"
}
```

Safety enforcement: if `observed_scopes` is not a subset of allowed scopes, the attempt is quarantined and a trust incident is raised.

## 10) Rollback receipt
`POST /agent/rollback`

Use after failed activation or trust incident quarantine to produce deterministic rollback receipts.

## 11) Query compatibility quickly
`GET /agent/compatibility/{pack_id}?runtime=openclaw&version=0.1.0`

## 12) Control-plane KPI status
`GET /status/control-plane?tenant_id=default&lookback_days=30`

Returns:
- Trusted Capability Resolution Rate (TCRR)
- quarantine rate
- average approval latency
- exploration regret proxy

## 13) Shadow-ranker hook (offline comparison)
`GET /analytics/shadow-ranker-eval?tenant_id=default&limit=300`

Returns baseline-vs-shadow agreement metrics and placeholder reward-delta diagnostics.

## 14) Export replay dataset (for offline policy/ranker evaluation)
`GET /analytics/replay-dataset?tenant_id=default&limit=500`

Returns candidate-level rows with:
- attempt context
- candidate score/features
- selected action flag
- propensity
- policy hash/effect
- outcome/reward

---

Use these endpoints inside autonomous loops:
- detect gap → search → install → execute → report outcome.
