# Implementation Agent Brief — 2026-03-25

Status accepted from governance direction: 
- GO: staging rollout hardening
- GO: OpenClaw-scoped internal pilot
- NOT GO: broader external rollout

## Scope lock
- Reference runtime: OpenClaw
- Autonomous pack types: skill, personality
- Manual-only: gateway/native-plugin installs
- Excluded from autonomous GA: payment/charge, autonomous social posting, sensitive inference from raw shell/browser text

## Freeze (except bug fixes)
- New catalog expansion
- New team features
- New ranking work
- New runtime expansion

## Mission milestone
"staging-grade signed control plane with OpenClaw adapter execution, soak evidence, and external-rollout gate packet."

## Block execution order
1) Managed staging rollout
2) Signed manifest endpoint + OpenClaw execution path
3) Provenance unification
4) 48h staging soak + external canary packet
5) Governance automation

## Required outputs
- staging-deploy-report.json
- staging-smoke-report.json
- backup-restore-drill.json
- seed-restore-report.json
- manifest-endpoint-spec-v1.md
- manifest-contract-conformance.json
- openclaw-manifest-execution-report.json
- provenance-linkage-report.json
- promotion-trust-gate-report.json
- soak-48h-staging-report.json
- soak-48h-staging-report.md
- external-canary-packet.json
- external-rollout-go-no-go.json
- weekly-governance-report-template.json
- governance-automation-readme.md

## Non-negotiable invariants
1. Never weaken digest pinning.
2. Never bypass pre-execution authorization.
3. Never disable quarantine-on-observed-scope-mismatch.
4. Never widen scope.
5. Never allow unsigned mutable metadata to drive install-time execution.
6. Never make rollback depend on manual DB edits.
