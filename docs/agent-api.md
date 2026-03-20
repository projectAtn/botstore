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
  "limit": 10
}
```

Response includes:
- `attempt_id`
- `candidate_snapshot_id`
- selected `pack_version_id` + `artifact_digest`
- policy decision/explanations
- optional signed approval grant metadata

## 4) Action-time authorization (proof-carrying approval)
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

## 5) Evaluate policy before autonomous install/use
`POST /agent/policy-evaluate`

```json
{
  "user_id": "telegram:8258812165",
  "runtime": "openclaw",
  "pack_id": 2
}
```

## 6) Submit outcome telemetry (legacy)
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

## 7) Submit outcome telemetry (v2, attempt-bound)
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

## 8) Query compatibility quickly
`GET /agent/compatibility/{pack_id}?runtime=openclaw&version=0.1.0`

---

Use these endpoints inside autonomous loops:
- detect gap → search → install → execute → report outcome.
