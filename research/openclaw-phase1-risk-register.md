# OpenClaw Phase 1 Risk Register

Generated: 2026-03-20

## R1: Sensitive execution via untyped tool path
- Risk: a side-effecting action bypasses typed mapping and pre-action authorization.
- Mitigation: fail closed for unknown side-effecting mappings; enforce `/agent/action-authorize` for sensitive scopes.
- Status: mitigated in adapter mapping, needs runtime middleware wiring validation.

## R2: Weak observed-scope fidelity
- Risk: runtime reports incomplete scopes, reducing trust quality.
- Mitigation: treat low-fidelity runtimes as weaker trust bands; keep sensitive autonomy constrained.
- Status: open (requires runtime certification harness).

## R3: Concurrent duplicate installs
- Risk: repeated gap resolution races create redundant installs.
- Mitigation: idempotency keys based on task/session+capability hash+pack version.
- Status: partial (control plane logs attempt-level, dedicated idempotency gate still to formalize).

## R4: Approval deadlock
- Risk: run pauses for approval but never resumes cleanly.
- Mitigation: explicit TTL + resume checkpoint keyed by attempt/session.
- Status: open (phase 2).

## R5: Policy drift impact
- Risk: policy bundle changes unintentionally alter allow/deny rates.
- Mitigation: shadow + replay diff + canary + rollback pointer.
- Status: partial (bundle registry/log exists; rollout automation pending).

## R6: Trust-chain incomplete in install path
- Risk: digest exists but signature/attestation gates are not fully mandatory.
- Mitigation: phase-2 install gate for signature/SBOM/attestation.
- Status: open.
