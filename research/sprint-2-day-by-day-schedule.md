# Sprint 2 Day-by-Day Execution Schedule (10 Workdays)

Date: 2026-03-18
Sprint Goal: Ranking moat + bundle workflows + personality runtime mode
Scope baseline: `BS-RANK-001`, `BS-BND-001`, `BS-PER-001`, `BS-QA-002`, `BS-CRT-001`

---

## Team lanes

- **Backend/Ranking:** ranking v2 and scoring controls
- **Backend/API:** bundle validation + personality attachment runtime path
- **Frontend:** bundle composer + creator trust views + personality selector
- **QA:** ranking eval harness and regression checks
- **PM/Docs:** threshold definitions + release notes

---

## Day 1
- Confirm baseline ranking metrics from current prod snapshot.
- Freeze ranking v2 scoring weights and guardrails (intent, capability, trust, anti-generic penalties).
- Define golden query set (Ops/Security/Marketing/Research/Finance).

## Day 2
- Implement ranking v2 scoring module behind feature flag.
- Add score explainability payload for debugging (`why` details).

## Day 3
- Add offline ranking evaluation script against golden queries.
- Compare v1 vs v2 top-3 relevance deltas.

## Day 4
- Implement bundle composer validation API:
  - duplicate problem target warnings
  - capability conflict checks
  - risk-level aggregate checks

## Day 5
- Frontend bundle composer UX:
  - child pack search/select
  - validation errors/warnings surfaced before save

## Day 6
- Implement personality runtime attachment flow (optional persona per install/use request).
- Ensure fallback-to-neutral behavior if persona unavailable.

## Day 7
- Frontend personality selector integration in install workflow.
- Add creator trust card fields in catalog result cards.

## Day 8
- QA harness (`BS-QA-002`) finalization:
  - top-3/top-5 reporting
  - drift alerts (intent-specific regressions)
- Run full suite against feature flag ON.

## Day 9
- Fixes + hardening:
  - ranking edge cases
  - bundle validation false positives
  - personality attach regressions

## Day 10
- Sprint demo + rollout decision:
  - ranking v2 results
  - bundle composer flow
  - personality runtime mode
- Handoff notes for Sprint 3 launch controls.

---

## Exit criteria
1. Ranking v2 improves top-3 relevance to >=80% on golden suite.
2. Bundle composer blocks invalid combos and explains why.
3. Personality runtime attach works without breaking installs.
4. Creator trust indicators visible in catalog.
5. QA report generated and archived for release decision.
