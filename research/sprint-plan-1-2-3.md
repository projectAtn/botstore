# BotStore 90-Day Delivery Plan — Sprint 1/2/3

Date: 2026-03-18
Owner: BotStore Core
Scope: Coexist-with-OpenClaw strategy (not replace), marketplace moat execution

---

## Planning assumptions

- Sprint length: 2 weeks
- Team capacity assumption: ~36 story points/sprint (small cross-functional team)
- Story point scale: Fibonacci (1, 2, 3, 5, 8, 13)
- Critical path focus:
  1) Import/Export interoperability
  2) Promotion QA gate
  3) Ranking v2 baseline
  4) Creator/trust + private visibility

---

## Sprint 1 — Foundation + Interop Core

Goal: Make BotStore interoperable with OpenClaw skill ecosystem and enforce quality gate before promotion.

### Backlog (Sprint 1)

| ID | Story | SP | Owner | Dependencies |
|---|---|---:|---|---|
| BS-INT-001 | Import OpenClaw skill folder (`SKILL.md` + metadata) into BotStore draft pack | 8 | Backend | None |
| BS-INT-002 | Export BotStore skill to OpenClaw-compatible package | 5 | Backend | BS-INT-001 (shared parser model) |
| BS-QA-001 | Promotion gate: block featured/promoted unless QA suite passes | 8 | Backend + QA | Existing QA scripts |
| BS-UI-001 | Catalog segmentation tabs (Skills / Personalities / Bundles / Verified) | 5 | Frontend | None |
| BS-OPS-001 | Artifact/report endpoint for latest QA run per pack | 3 | Backend | BS-QA-001 |
| BS-REL-001 | Regression smoke tests for install/search/promotion paths | 5 | QA | None |
| BS-PM-001 | Docs/update: positioning + operator runbook | 2 | PM/Docs | None |

**Sprint 1 total: 36 SP**

### Sprint 1 Definition of Done

- Import/export works on at least 10 real skills.
- Promotion gate enforces pass/fail at API layer.
- UI segmentation live in catalog.
- QA report attached to candidate/published items.

---

## Sprint 2 — Ranking + Bundles + Personality Runtime

Goal: Improve recommendation quality and package outcomes through bundles + personality attachment.

### Backlog (Sprint 2)

| ID | Story | SP | Owner | Dependencies |
|---|---|---:|---|---|
| BS-RANK-001 | Ranking v2 (intent + capability + trust + anti-generic penalty) | 13 | Backend/Ranking | BS-QA-001 |
| BS-BND-001 | Bundle composer UI + API validation (child conflict checks) | 8 | Backend + Frontend | BS-UI-001 |
| BS-PER-001 | Personality runtime mode (attach optional persona to workflow/install) | 8 | Backend + Frontend | Existing personality catalog |
| BS-QA-002 | Ranking eval harness: top-3/top-5 relevance reports by intent suite | 5 | QA | BS-RANK-001 |
| BS-CRT-001 | Creator trust card in catalog (verification + QA pass rate + trust score) | 5 | Frontend | BS-OPS-001 |

**Sprint 2 total: 39 SP**

### Sprint 2 Definition of Done

- Ranking v2 beats baseline on test-agent suites (target: top-3 relevance >80%).
- Bundles creatable/editable with validation.
- Personality mode selectable and stable.
- Creator trust indicators visible in UI.

---

## Sprint 3 — Marketplace Controls + Monetization + Multi-runtime Deploy

Goal: Move from strong internal marketplace to launch-ready platform controls.

### Backlog (Sprint 3)

| ID | Story | SP | Owner | Dependencies |
|---|---|---:|---|---|
| BS-ENT-001 | Visibility model (public/team/private packs) + ACL enforcement | 8 | Backend/Auth | BS-INT-001 |
| BS-MON-001 | Paid pack entitlement checks (install-time) | 13 | Backend/Billing | BS-ENT-001 |
| BS-COMP-001 | Audit export (install/approval/action logs JSON+CSV) | 5 | Backend | BS-QA-001 |
| BS-DEP-001 | Multi-runtime one-click deploy orchestration + per-target status | 8 | Backend/Runtime | Existing target binding flow |
| BS-QA-003 | Launch readiness test matrix (security + rollback + permission leakage) | 8 | QA/Sec | BS-ENT-001, BS-MON-001 |

**Sprint 3 total: 42 SP**

### Sprint 3 Definition of Done

- Private/team visibility enforced server-side.
- Paid pack entitlements block unauthorized installs.
- Audit export usable for compliance checks.
- Multi-runtime deploy supports success/failure visibility and rollback-safe behavior.

---

## Dependency graph (high-level)

1. **BS-INT-001** → enables robust import/export object model
2. **BS-QA-001** → prerequisite for trustworthy promotion and ranking validation
3. **BS-RANK-001** → depends on QA signal + normalized metadata
4. **BS-ENT-001** → prerequisite for monetization controls
5. **BS-MON-001** + **BS-ENT-001** → prerequisite for launch-grade paid/private marketplace

Critical path:
`BS-INT-001 -> BS-QA-001 -> BS-RANK-001 -> BS-ENT-001 -> BS-MON-001 -> BS-QA-003`

---

## Milestone checkpoints

- End Sprint 1: Interop + quality gate baseline complete
- End Sprint 2: Recommendation moat (ranking + bundles + personality runtime) complete
- End Sprint 3: Launch controls (private/paid/deploy/audit) complete

---

## Risks and mitigations

1. **Risk:** Ranking noise from overlapping scope signatures
   - Mitigation: include intent lexical weighting + anti-generic penalty + test-agent eval gates.

2. **Risk:** Promotion bypass via manual DB edits
   - Mitigation: enforce promotion state transitions in API, add audit logs for state changes.

3. **Risk:** Bundle overfitting / duplicate problem targets
   - Mitigation: add “problem uniqueness check” in bundle composer and QA warnings.

4. **Risk:** Monetization complexity delays core value
   - Mitigation: keep paid model minimal in Sprint 3 (entitlement check first, advanced billing later).

---

## KPI targets by end of Sprint 3

- Top-3 recommendation relevance: **>= 80%** on core suites
- Promotion QA pass-before-publish: **>= 90%**
- Install success rate: **>= 95%**
- Post-install rollback rate: **<= 5%**
- Creator weekly retention trend: positive for 4 consecutive weeks
