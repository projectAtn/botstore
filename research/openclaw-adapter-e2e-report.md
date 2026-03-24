# OpenClaw Adapter E2E

- Time: 2026-03-24T14:23:02.827085+00:00
- API: http://127.0.0.1:8787
- Attempt: `att_34334cdbbc3c45ab`
- Runtime: `openclaw` band `B`

## Resolve
```json
{
  "ok": true,
  "attempt_id": "att_34334cdbbc3c45ab",
  "task_id": "task-openclaw-smoke-1774362182",
  "tenant_id": "default",
  "runtime": {
    "runtime_id": "openclaw",
    "runtime_version": "0.2.0",
    "runtime_band": "B"
  },
  "candidate_snapshot_id": "cand_10812ce2fa33",
  "install_target": "agent_workspace",
  "activation_mode": "immediate_hot",
  "selected": {
    "pack_id": 165,
    "pack_slug": "smoke-deploy-guardian-1774286365710723000",
    "pack_version_id": 39,
    "artifact_digest": "sha256:eeb63402000b1991df82ad4564717b3fa2dbcbd3a1836b6718c4cafbe1460a91",
    "verification_tier": "tier2_verified",
    "risk_level": "medium",
    "capabilities_declared": [
      "deploy.rollback",
      "incident.triage"
    ],
    "scopes_requested": [
      "log.read",
      "message.send"
    ],
    "actions_supported": [
      "deploy.rollback",
      "message.send"
    ],
    "policy_effect": "allow_with_approval",
    "policy_reasons": [
      "sensitive_or_low_verification"
    ],
    "policy_blocking": [],
    "score": 0.92
  },
  "selection": {
    "mode": "safe_bucket_baseline",
    "propensity": 0.95,
    "safe_bucket_size": 3
  },
  "policy": {
    "schema_version": "bps-0.1",
    "decision_id": 26,
    "effect": "allow_with_approval",
    "reason_codes": [
      "sensitive_or_low_verification"
    ],
    "blocking_conditions": [],
    "required_approvals": [
      "install"
    ],
    "minimum_verification_tier": "tier1_signed",
    "runtime_requirements": {
      "runtime_band_max": "B"
    },
    "policy_hash": "b57737771ff2eee6ac61a921b43e1941c3df9091d39308f77853837e465de92b"
  },
  "approval_grant": {
    "grant_id": "gr_dfc24f53220441",
    "expires_at": "2026-03-24T15:23:02.793046+00:00",
    "signature": "-n1vqZ9Fqu_WKBUJvRnaxh2cJyalogO4oadMNH7enRI"
  },
  "install_status": "pending_approval",
  "activation_status": "pending",
  "status": "approval_required"
}
```

## Authorize
```json
{
  "decision": "allow_with_runtime_proof",
  "reason": "approved with signed grant",
  "grant_token": "eyJncmFudF9pZCI6ICJncl9lOTZlZGViNTZmZWE0NiIsICJhdHRlbXB0X2lkIjogImF0dF8zNDMzNGNkYmJjM2M0NWFiIiwgInRlbmFudF9pZCI6ICJkZWZhdWx0IiwgImFydGlmYWN0X2RpZ2VzdCI6ICJzaGEyNTY6ZWViNjM0MDIwMDBiMTk5MWRmODJhZDQ1NjQ3MTdiM2ZhMmRiY2JkM2ExODM2YjY3MThjNGNhZmJlMTQ2MGE5MSIsICJwYWNrX3ZlcnNpb25faWQiOiAzOSwgImFsbG93ZWRfc2NvcGVzIjogWyJtZXNzYWdlLnNlbmQiXSwgImFsbG93ZWRfYWN0aW9ucyI6IFsibWVzc2FnZS5zZW5kIl0sICJydW50aW1lX2lkIjogIm9wZW5jbGF3IiwgInJ1bnRpbWVfYmFuZCI6ICJCIiwgImV4cGlyZXNfYXQiOiAiMjAyNi0wMy0yNFQxNToyMzowMi44MDA4MzkrMDA6MDAiLCAicG9saWN5X2hhc2giOiAiNGU3YWZiYTc3NjQ2MjFkZDNiNThlZTIzMWQzMzhmMTI0NmNhNGMwNmZiMmFkZjFmNWI4MTNlNDg5MDEwMTk4YiIsICJqdXN0aWZpY2F0aW9uIjogIm9wZW5jbGF3IGFkYXB0ZXIgc21va2UiLCAic2lnbmF0dXJlIjogIk00SWE1NmxfMGVsNFZESk82dG00V0FjQ2E2b1Q0OGkxMW5lOC1DUmRUMVUifQ==",
  "grant_id": "gr_e96edeb56fea46",
  "expires_at": "2026-03-24T15:23:02.800839+00:00"
}
```

## Approval pause
```json
{
  "ok": true,
  "checkpoint_id": "chk_7552983fbfc342c0",
  "attempt_id": "att_34334cdbbc3c45ab",
  "status": "paused",
  "expires_at": "2026-03-24T14:53:02.804697+00:00"
}
```

## Approval resume
```json
{
  "ok": true,
  "checkpoint_id": "chk_7552983fbfc342c0",
  "attempt_id": "att_34334cdbbc3c45ab",
  "status": "resumed",
  "attempt_status": "approval_granted"
}
```

## Outcome violation
```json
{
  "ok": true,
  "outcome_report_id": 42,
  "attempt_id": "att_34334cdbbc3c45ab",
  "reward": -1.0,
  "quarantined": true,
  "undeclared_scopes": [
    "payment.charge"
  ]
}
```

## Rollback
```json
{
  "ok": true,
  "rollback_receipt": {
    "attempt_id": "att_34334cdbbc3c45ab",
    "tenant_id": "default",
    "rollback_status": "rolled_back",
    "reason": "scope_violation_quarantine",
    "rolled_at": "2026-03-24T14:23:02.817574+00:00",
    "runtime_id": "openclaw",
    "install_target": "agent_workspace",
    "activation_mode": "immediate_hot"
  }
}
```

Decision log rows: 16
