# Quality Control & Publishing Team Model v1

Date: 2026-03-18
Status: Draft operating model

## Objective
Establish a standing team that owns quality, publishing safety, and roadmap recommendations for BotStore.

---

## Team structure

## 1) Quality Council (core)
- **Head of Quality (owner)**
- **Runtime QA Lead** (OpenClaw + adapters)
- **Security/Policy Lead**
- **Scenario QA Lead** (team simulations)
- **Telemetry Analyst**

## 2) Publishing Committee (release gate)
- **Publisher-in-Chief**
- **Trust/Compliance Reviewer**
- **Marketplace Curator**
- **Rollback Operator**

## 3) Strategy Review Cell (next-step suggestions)
- **Product Strategist**
- **Growth/Distribution Lead**
- **Infrastructure Lead**

---

## Responsibilities

### Quality Council
- Define pass/fail gates for skills, personalities, and teams.
- Own CI gate (`regression + ranking + pack QA + team must-pass`).
- Approve or reject promotion readiness artifacts.

### Publishing Committee
- Decide what gets featured, delayed, or delisted.
- Ensure no team-only hidden skills (standalone-skill rule).
- Enforce rollback runbook when regressions are detected.

### Strategy Review Cell
- Weekly "what next" memo from telemetry, failures, and demand signals.
- Propose 2-3 concrete expansion bets each week.

---

## Quality gates (minimum)

### Gate A — Technical integrity
- CI run-all passes.
- Adapter preflight passes for supported runtimes.

### Gate B — QA confidence
- Skill/personality/team QA status = pass.
- Team must-pass scenarios: 10/10 per team.

### Gate C — Trust & policy
- Risk classification valid.
- Approval requirements and governance checks satisfied.

### Gate D — Marketplace readiness
- Metadata complete.
- Outcome telemetry hook active.
- Rollback path verified.

No feature promotion without all gates green.

---

## Weekly operating cadence

### Daily
- CI and gate dashboard review
- Failure triage + hotfix queue

### Twice weekly
- Publishing committee decisions (promote/hold/delist)

### Weekly
- Strategy review memo:
  - What failed?
  - What improved?
  - What to build next?

---

## Metrics dashboard

- CI pass rate
- Promotion pass-before-publish rate
- Team must-pass compliance rate
- Install success rate
- Rollback rate
- Adapter install success by runtime
- Top-3 relevance rate
- Creator quality score trend

---

## Suggested immediate staffing (lean)

Minimum 4-person loop:
1. Quality owner
2. QA engineer
3. Publishing operator
4. Infra/runtime engineer

With AI sub-agent support for repetitive checks and report generation.
