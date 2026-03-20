# BotStore Adapter Contract v1 (Draft)

Status: draft

Defines the runtime-facing lifecycle methods every adapter should implement.

## Required methods

### 1) install
Input:
- `attempt_id`
- `pack_version_id`
- `artifact_digest`
- `runtime_id`
- `runtime_version`

Output:
- install result
- integrity verification status

### 2) activate
Input:
- `attempt_id`
- runtime binding details

Output:
- activation status

### 3) rollback
Input:
- `attempt_id`
- reason

Output:
- rollback status

### 4) observe_scopes
Input:
- runtime execution context

Output:
- `observed_scopes[]`

### 5) action_authorize
Input:
- `attempt_id`
- `pack_version_id`
- `artifact_digest`
- `requested_action`
- `requested_scope`
- runtime proof/attestation

Output:
- allow / deny / allow_with_runtime_proof
- grant token when required

### 6) outcome_report
Input:
- `attempt_id`
- task result fields
- observed scope evidence

Output:
- ingestion ack

### 7) compatibility_probe
Input:
- `pack_version_id`
- runtime metadata

Output:
- compatibility status + constraints

## Non-negotiable invariant
If `observed_scopes` is not subset of granted/allowed scopes:
- stop execution
- emit trust incident
- quarantine attempt
- request rollback

## Suggested AdapterResult envelope
```json
{
  "ok": true,
  "attempt_id": "att_...",
  "status": "activated",
  "runtime_id": "openclaw",
  "details": {}
}
```
