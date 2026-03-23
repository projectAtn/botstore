# Trust Chain Design v1 (Phase 2A)

## Goal
Fail closed on autonomous install paths unless mandatory trust evidence is present and verified.

## PackVersion trust fields
- `artifact_uri`
- `signature_refs_json`
- `sbom_ref`
- `attestation_refs_json`
- `verification_state` (`unverified|verified|failed`)
- `verification_error`
- `verification_checked_at`
- `verification_verified_at`

## Verification gate (current)
Install path (`/agent/install-by-capability-v2`) only considers pack versions where:
1. trust evidence is present
2. local trust verification passes
3. `verification_state == verified`

Promotion path also requires trust verification success.

## Trust APIs
- `PUT /packs/{pack_id}/versions/{version_id}/trust`
- `POST /packs/{pack_id}/versions/{version_id}/trust/verify-local`

## Tooling
- `scripts/trust_chain_smoke.py`
- `scripts/trust_cosign_sign.sh`
- `scripts/trust_cosign_verify.sh`
- `scripts/trust_generate_spdx.sh`

## Next hardening step
Replace local trust verifier with mandatory cosign + attestation predicate checks in the install gate.
