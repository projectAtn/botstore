# External Rollout Gate Checklist v1

## Must be green before broader external rollout

### Admission and trust
- production trust mode enabled
- exact issuer + exact workflow identity pinning enabled
- signature bundle/transparency proof required
- required attestation set verified fail-closed
- digest-bound cryptographic VerificationReceipt required for install admission

### Runtime and safety
- scope lock unchanged
- resolver tool optional/allowlisted
- pre-execution action-authorize still mandatory
- no autonomous gateway/native-plugin installs
- typed sensitive action map complete
- auth-bypass sentinel passing
- quarantine-on-observed-scope-mismatch mandatory

### Observability and operations
- OTLP diagnostics enabled
- dashboard and alerts live
- correlation IDs present across artifacts
- policy_slo_controller live
- rollback pointer validated

### Readiness evidence
- 48h deterministic unattended soak passed
- 7-day limited external canary passed
- no stale heartbeat during canary
- outcome-v2 completeness >= 98%
- no unexpected quarantines in happy-path traffic
