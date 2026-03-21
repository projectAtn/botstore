# OpenClaw Phase-1 Launch Readiness Packet

## Objective
Determine whether the OpenClaw reference runtime path is ready to exit phase-1 hardening and enter controlled pilot expansion.

## Required evidence bundle
1. Single-run conformance artifacts
   - `research/openclaw-conformance-result.json`
   - `research/openclaw-conformance-report.md`
   - `/tmp/openclaw_phase1_exit_check.json`
2. Burn-in artifacts
   - `research/qa-loop/openclaw-burnin/*.json`
   - `research/qa-loop/openclaw-burnin/summary.json`
   - `research/qa-loop/openclaw-burnin/summary.md`
3. Policy/trust artifacts
   - `docs/openclaw-tenant-policy-matrix-v1.md`
   - `research/openclaw-phase1-risk-register.md`

## Run sequence
```bash
cd /Users/claw/.openclaw/workspace/botstore
./scripts/openclaw_conformance.sh
RUNS=5 ./scripts/openclaw_conformance_burnin.sh
```

## GO decision baseline
- health and policy decision log checks pass across burn-in runs
- quarantine rate max within threshold in burn-in summary
- approval latency average within threshold in burn-in summary
- no unresolved phase-1 safety invariant violation

## NO_GO triggers
- any run fails health/policy decision log checks
- quarantine rate threshold breach
- approval latency threshold breach
- missing conformance artifacts

## Notes
This packet is phase-1 scoped. It does not imply phase-2 trust-chain completion (signature/attestation mandatory gates) or full GA readiness.
