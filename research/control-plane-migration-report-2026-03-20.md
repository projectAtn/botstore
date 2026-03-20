# BotStore Control-Plane Migration Report — 2026-03-20

## Summary
BotStore has been shifted from a catalog/install-only model to an install-transaction control plane centered on `InstallAttempt` and digest-pinned `PackVersion`.

## New Core Objects
- `PackVersion`
- `InstallAttempt`
- `PolicyDecision`
- `ApprovalGrant`
- `CandidateImpression`
- `ActionAuthorization`
- `OutcomeReport`
- `TrustIncident`
- `PolicyBundle`

## New/Updated API Endpoints
### Install/Policy/Authorization
- `POST /agent/install-by-capability-v2`
- `POST /agent/action-authorize`
- `POST /agent/outcome-v2`
- `POST /policy/bps/evaluate`
- `POST /policy/bundles`
- `GET /policy/bundles`
- `GET /policy/decision-log`

### Analytics/Status
- `GET /analytics/replay-dataset`
- `GET /analytics/shadow-ranker-eval`
- `GET /status/control-plane`

### Versioning
- `POST /packs/{pack_id}/versions`
- `GET /packs/{pack_id}/versions`

## Policy/Trust Changes
- Runtime bands A/B/C/D introduced.
- Structured policy explanation output standardized:
  - `reason_codes`
  - `blocking_conditions`
  - `required_approvals`
  - `minimum_verification_tier`
  - `runtime_requirements`
  - `policy_hash`
- Sensitive action flow supports signed grant token output.
- Quarantine enforcement on observed scope mismatch:
  - if `observed_scopes` is not subset of allowed scopes, trust incident is raised and attempt is quarantined.

## Ranking/Learning Changes
- Candidate-set logging now captures full decision context (not only winner).
- Propensity and exploration bucket are recorded on impressions.
- Safe exploration path constrained to policy-equivalent, non-risk-escalating candidates.
- Replay and shadow evaluation endpoints added for offline policy/ranker iteration.

## Promotion Gate Hardening
`PUT /packs/{pack_id}/promote?featured=true` now additionally checks:
- current version exists
- verification tier >= tier1_signed
- >= 5 matured outcomes
- Wilson lower-confidence success bound threshold
- tenant diversity threshold
- no quarantined trust incidents

## Reverify Operations
- Added `scripts/reverify_scheduler.py` hazard-based cadence:
  - high risk: 7d
  - medium risk: 30d
  - low risk: 60d
- Immediate due on recent trust incidents.

## Draft Spec Assets Added
- `docs/pack-spec-v1.md`
- `docs/adapter-contract-v1.md`

## Operational Note
Current implementation remains a modular monolith (FastAPI + DB-backed models), consistent with near-term plan.
