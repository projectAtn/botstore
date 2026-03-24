# Trust Chain Design v2 (Cryptographic Admission)

## Objective
Upgrade trust admission from local evidence checks to cryptographic verification receipts for production mode.

## Trust policy object
Source:
- `research/trust_policy_v1.json`

Fields:
- `mode` (`dev|test|production`)
- `trusted_issuers[]`
- `trusted_identities[]`
- `required_signature_annotations[]`
- `required_attestation_predicates[]`
- `require_sbom`
- `freshness_ttl_hours`

## Verification receipts
Model: `VerificationReceipt`
- `pack_version_id`
- `artifact_digest`
- `verifier_mode` (`local|cryptographic`)
- `ok`
- `checks_json`
- `error`
- `policy_hash`
- `created_at`

## Admission behavior
- `mode in {dev,test,local}`:
  - local verification may satisfy admission.
- `mode=production`:
  - only latest successful `cryptographic` receipt satisfies admission.
  - local-only receipts are insufficient.

## Verification endpoints
- `PUT /packs/{pack_id}/versions/{version_id}/trust`
- `POST /packs/{pack_id}/versions/{version_id}/trust/verify-local`
- `POST /packs/{pack_id}/versions/{version_id}/trust/verify-crypto`
- `GET /packs/{pack_id}/versions/{version_id}/trust/receipts`

## Cryptographic checks (verify-crypto)
- local trust evidence sanity (digest/uri/signature/sbom/attestation refs)
- `cosign verify` with issuer/identity pinning
- `cosign verify-attestation` for required predicates
- freshness TTL check

## Fail-closed policy
In production mode, if cryptographic verification fails/missing/stale, candidate is rejected for autonomous install and promotion gates.
