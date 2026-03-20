# BotStore Pack Spec v1 (Draft)

Status: draft

## Purpose
Canonical package metadata for capability retrieval, policy evaluation, compatibility checks, and digest-pinned installation.

## Identity
- `pack_id` (stable logical id)
- `pack_version_id` (immutable install unit)
- `slug`
- `semver`
- `manifest_version`
- `artifact_digest` (sha256:...)

## Capability / Permission / Action separation
- `capabilities_declared[]`: retrieval and ranking surface
- `scopes_requested[]`: permissions required
- `actions_supported[]`: concrete runtime operations
- `capabilities_verified[]` (optional evidence)
- `scopes_observed[]` (runtime evidence)

## Runtime compatibility
- `compatible_runtimes[]`
- `runtime_requirements` (e.g. `{ runtime_band_max: "C" }`)

## Trust + verification
- `verification_tier`
- `sbom_ref` (optional)
- `signature_ref` (optional)
- `attestation_refs[]` (optional)

## Policy hints
- `policy_requirements` (declarative hints only)
- final allow/deny semantics must come from policy engine decision output

## Conformance hooks
- `fixtures_ref` (optional)
- `expected_outputs_ref` (optional)
- `expected_scope_usage_ref` (optional)

## Recommended minimal JSON shape
```json
{
  "pack_id": 12,
  "pack_version_id": 48,
  "slug": "deploy-rollback-guardian",
  "semver": "1.2.0",
  "manifest_version": "v2",
  "artifact_digest": "sha256:...",
  "capabilities_declared": ["deploy.rollback", "incident.triage"],
  "scopes_requested": ["log.read", "message.send"],
  "actions_supported": ["deploy.rollback", "message.send"],
  "compatible_runtimes": ["openclaw"],
  "runtime_requirements": {"runtime_band_max": "B"},
  "verification_tier": "tier2_verified"
}
```
