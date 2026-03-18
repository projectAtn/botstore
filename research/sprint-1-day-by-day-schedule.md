# Sprint 1 Day-by-Day Execution Schedule (10 Workdays)

Date: 2026-03-18
Sprint Goal: Interop foundation + QA promotion gate + catalog segmentation baseline
Scope baseline: `BS-INT-001`, `BS-INT-002`, `BS-QA-001`, `BS-UI-001`, `BS-OPS-001`, `BS-REL-001`, `BS-PM-001`

---

## Team lanes

- **Backend A:** Interop parser/import/export
- **Backend B:** Promotion gate + QA artifacts
- **Frontend:** Catalog segmentation + trust/QA surfacing hooks
- **QA:** Regression + gate validation suite
- **PM/Docs:** Positioning + runbook + acceptance tracking

---

## Day 1 (Kickoff + architecture lock)

- Align acceptance criteria for all Sprint 1 tickets.
- Freeze import/export data model (`slug/title/problem/scopes/risk/type/version`).
- Define promotion state machine (`draft -> qa_passed -> promoted`).
- Create test data set: 10 representative skill folders.

**Deliverables:**
- ADR note for interop model
- Sprint board with owners and blockers

---

## Day 2 (Importer skeleton)

- Implement folder scanner + `SKILL.md` parser (happy path).
- Add draft pack creation endpoint for imported skills.
- Add parse warnings for missing fields.

**Deliverables:**
- `BS-INT-001` v0 endpoint
- Initial importer unit tests

---

## Day 3 (Exporter skeleton)

- Implement BotStore pack -> OpenClaw-compatible export package.
- Include metadata + version + changelog stub.
- Validate on 3 packs roundtrip (import -> export).

**Deliverables:**
- `BS-INT-002` v0
- Roundtrip smoke script

---

## Day 4 (Promotion gate core)

- Add API enforcement: promotion requires QA status = pass.
- Persist QA result object (status, suite, timestamp, reason).
- Reject manual promote calls when missing/failed QA.

**Deliverables:**
- `BS-QA-001` backend gate
- API error contract for blocked promotion

---

## Day 5 (QA artifact endpoint + regression harness)

- Build endpoint to fetch latest QA report per pack.
- Add regression tests for install/search/promotion invariants.
- CI job: run regression + gate tests.

**Deliverables:**
- `BS-OPS-001`
- `BS-REL-001` initial CI coverage

---

## Day 6 (Frontend catalog segmentation)

- Implement segmented catalog views: Skills / Personalities / Bundles / Verified.
- Preserve selected filter state in session.
- Add visual marker for approval-required packs.

**Deliverables:**
- `BS-UI-001` v1 in web UI

---

## Day 7 (Frontend QA/trust surfacing)

- Add QA badge placeholder in cards.
- Show pass/fail + last run timestamp from artifact endpoint.
- Add creator trust badge slot (data-ready, UI visible).

**Deliverables:**
- UI integration with QA artifact data

---

## Day 8 (Integration day)

- End-to-end flow test:
  1) import skill
  2) run QA
  3) promote (pass only)
  4) export promoted skill
- Fix integration bugs + schema mismatches.

**Deliverables:**
- E2E green path demo script

---

## Day 9 (Hardening + failure paths)

- Negative-path tests:
  - malformed skill folders
  - missing scopes/risk
  - promotion without QA
  - failed QA promotion attempts
- Improve error messages for operator clarity.

**Deliverables:**
- Failure-path test report
- Updated operator runbook draft

---

## Day 10 (Sprint close)

- Final regression run + release candidate tag.
- Demo to stakeholder:
  - interop import/export
  - QA gate enforcement
  - segmented catalog UX
- Retrospective + Sprint 2 handoff notes.

**Deliverables:**
- Sprint 1 review packet
- Sprint 2 ready backlog (ranking/bundles/personality runtime)

---

## Daily checkpoint template (use each day)

- Yesterday done:
- Today planned:
- Blockers:
- Risk level (low/med/high):
- KPI drift notes:

---

## Exit criteria (Sprint 1 complete)

1. 10-skill import test set parses with deterministic draft creation.
2. Exported pack validates for OpenClaw-compatible structure.
3. Promotion API blocks all non-QA-passed promotions.
4. Catalog segmentation is live and usable in UI.
5. Regression and gate tests pass in CI.
