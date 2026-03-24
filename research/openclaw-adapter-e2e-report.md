# OpenClaw Adapter E2E

- Time: 2026-03-24T11:36:13.865944+00:00
- API: http://127.0.0.1:8787
- Attempt: `att_f35a62c607654a8b`
- Runtime: `openclaw` band `B`

## Resolve
```json
{
  "ok": true,
  "attempt_id": "att_f35a62c607654a8b",
  "task_id": "task-openclaw-smoke-1774352173",
  "tenant_id": "default",
  "runtime": {
    "runtime_id": "openclaw",
    "runtime_version": "0.2.0",
    "runtime_band": "B"
  },
  "candidate_snapshot_id": "cand_e51027c1201a",
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
    "decision_id": 25,
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
    "policy_hash": "1f05bc584351340d9023a1f88b13d2372729eaa2ddc76f64ff178fd9ae87e21a"
  },
  "approval_grant": {
    "grant_id": "gr_51547703d9394b",
    "expires_at": "2026-03-24T12:36:13.831324+00:00",
    "signature": "OgdhP_TdKKK2TJnpAsIdqIYovpyAjrw0s8BE8bbJsQE"
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
  "grant_token": "eyJncmFudF9pZCI6ICJncl81M2UyYmNlY2JjNmU0NSIsICJhdHRlbXB0X2lkIjogImF0dF9mMzVhNjJjNjA3NjU0YThiIiwgInRlbmFudF9pZCI6ICJkZWZhdWx0IiwgImFydGlmYWN0X2RpZ2VzdCI6ICJzaGEyNTY6ZWViNjM0MDIwMDBiMTk5MWRmODJhZDQ1NjQ3MTdiM2ZhMmRiY2JkM2ExODM2YjY3MThjNGNhZmJlMTQ2MGE5MSIsICJwYWNrX3ZlcnNpb25faWQiOiAzOSwgImFsbG93ZWRfc2NvcGVzIjogWyJtZXNzYWdlLnNlbmQiXSwgImFsbG93ZWRfYWN0aW9ucyI6IFsibWVzc2FnZS5zZW5kIl0sICJydW50aW1lX2lkIjogIm9wZW5jbGF3IiwgInJ1bnRpbWVfYmFuZCI6ICJCIiwgImV4cGlyZXNfYXQiOiAiMjAyNi0wMy0yNFQxMjozNjoxMy44MzY5MzkrMDA6MDAiLCAicG9saWN5X2hhc2giOiAiOGUwOGY1Y2YzNWU3YjMzOWE3YjZiN2E5YmM1MTNkMDlmZDI5ZWE3ZjE0MGM4ZTNkNjYzMWE5OTZiZjA3ZjQyMSIsICJqdXN0aWZpY2F0aW9uIjogIm9wZW5jbGF3IGFkYXB0ZXIgc21va2UiLCAic2lnbmF0dXJlIjogImdaeTlFSWpFT1R4YURUdXduSnV1ODN0TktGcnR0WW1iRTh2N3FyV0JxTmcifQ==",
  "grant_id": "gr_53e2bcecbc6e45",
  "expires_at": "2026-03-24T12:36:13.836939+00:00"
}
```

## Approval pause
```json
{
  "ok": true,
  "checkpoint_id": "chk_0396d32869ea485b",
  "attempt_id": "att_f35a62c607654a8b",
  "status": "paused",
  "expires_at": "2026-03-24T12:06:13.843386+00:00"
}
```

## Approval resume
```json
{
  "ok": true,
  "checkpoint_id": "chk_0396d32869ea485b",
  "attempt_id": "att_f35a62c607654a8b",
  "status": "resumed",
  "attempt_status": "approval_granted"
}
```

## Outcome violation
```json
{
  "ok": true,
  "outcome_report_id": 40,
  "attempt_id": "att_f35a62c607654a8b",
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
    "attempt_id": "att_f35a62c607654a8b",
    "tenant_id": "default",
    "rollback_status": "rolled_back",
    "reason": "scope_violation_quarantine",
    "rolled_at": "2026-03-24T11:36:13.855029+00:00",
    "runtime_id": "openclaw",
    "install_target": "agent_workspace",
    "activation_mode": "immediate_hot"
  }
}
```

Decision log rows: 16
