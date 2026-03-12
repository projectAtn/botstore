# BotPack Conformance Spec v0.1

## Goal
Guarantee that a pack behaves consistently across ecosystems.

## Test classes
1. **Manifest validation**
   - Valid against `botpack.schema.json`
   - Signature/publisher metadata present

2. **Capability contract tests**
   - Every declared capability maps to runtime adapter function
   - Every undeclared capability is denied

3. **Policy enforcement tests**
   - Sensitive capabilities trigger approval
   - High-risk packs cannot auto-install

4. **Behavior tests (personality packs)**
   - Tone/profile assertions (style checks)
   - Boundary checks (no disallowed claims or actions)

5. **Workflow tests (skill packs)**
   - Golden-path task succeeds
   - Error-path fallback produces deterministic recovery

6. **Observability tests**
   - Audit event emitted for external writes
   - Execution trace includes runtime + adapter + pack version

## Required pass threshold
- Hard fail if any policy test fails.
- Soft fail if latency p95 exceeds configured runtime budget.

## Output artifact
Conformance run outputs `compatibility-matrix.json` validated by
`compatibility-matrix.schema.json`.
