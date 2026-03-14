# V3 Intake Summary

Generated: 2026-03-14T12:31:52.178146+00:00

## 1) Merge
- Merged output: `/Users/claw/.openclaw/workspace/botstore/research/candidate-packs-v3.json`
- Total merged candidates: **45**
- Source counts (pre-dedup): skills=30, personalities=15
- Duplicate slugs overwritten: none

## 2) Quality check
- Threshold: **>=80**
- Pass: **45 / 45**
- Output: `/Users/claw/.openclaw/workspace/botstore/research/candidate-packs-v3-quality-report.md` and `/Users/claw/.openclaw/workspace/botstore/research/candidate-packs-v3-quality-result.json`

## 3) Runtime simulation + strict tier/risk gate
- Risk gates: low=80, medium=90, high=95
- Final verified: **45 / 45**
- Output: `/Users/claw/.openclaw/workspace/botstore/research/runtime-simulation-v3-report.md` and `/Users/claw/.openclaw/workspace/botstore/research/runtime-simulation-v3-result.json`

## 4) Contract test generation (top 12)
- Contracts generated: **12**
- Output: `/Users/claw/.openclaw/workspace/botstore/research/pack-performance-contracts-v3.json`

## 5) Promotion list
- Promoted: **12**
- Hold: **33**

### Promoted
| slug | type | risk | quality | runtime | tier |
|---|---|---|---:|---:|---|
| `inbox-triage-pro` | skill | medium | 100 | 100 | gold |
| `calendar-conflict-resolver` | skill | medium | 100 | 100 | gold |
| `meeting-brief-builder` | skill | low | 100 | 100 | gold |
| `research-citation-packager` | skill | medium | 100 | 100 | gold |
| `expense-receipt-organizer` | skill | medium | 100 | 100 | gold |
| `travel-itinerary-concierge` | skill | medium | 100 | 100 | gold |
| `job-application-accelerator` | skill | low | 100 | 100 | gold |
| `codebase-onboarding-guide` | skill | low | 100 | 100 | gold |
| `pr-review-summarizer` | skill | medium | 100 | 100 | gold |
| `incident-postmortem-writer` | skill | medium | 100 | 100 | gold |
| `contract-redline-assistant` | skill | high | 100 | 100 | gold |
| `policy-sop-generator` | skill | medium | 100 | 100 | gold |

### Hold
| slug | type | risk | quality | runtime | tier | reason |
|---|---|---|---:|---:|---|---|
| `social-content-repurposer` | skill | low | 100 | 100 | gold | not in top12 contracts |
| `ad-copy-ab-tester` | skill | medium | 100 | 100 | gold | not in top12 contracts |
| `seo-content-optimizer` | skill | low | 100 | 100 | gold | not in top12 contracts |
| `customer-feedback-clusterer` | skill | medium | 100 | 100 | gold | not in top12 contracts |
| `support-ticket-autoprioritizer` | skill | high | 100 | 100 | gold | not in top12 contracts |
| `oncall-handoff-assistant` | skill | medium | 100 | 100 | gold | not in top12 contracts |
| `database-migration-guard` | skill | high | 100 | 100 | gold | not in top12 contracts |
| `api-change-impact-analyzer` | skill | medium | 100 | 100 | gold | not in top12 contracts |
| `docs-to-faq-converter` | skill | low | 100 | 100 | gold | not in top12 contracts |
| `learning-path-designer` | skill | low | 100 | 100 | gold | not in top12 contracts |
| `fitness-plan-adapter` | skill | medium | 100 | 100 | gold | not in top12 contracts |
| `meal-prep-planner` | skill | low | 100 | 100 | gold | not in top12 contracts |
| `budget-guardrails-coach` | skill | medium | 100 | 100 | gold | not in top12 contracts |
| `subscription-leak-finder` | skill | medium | 100 | 100 | gold | not in top12 contracts |
| `home-maintenance-scheduler` | skill | low | 100 | 100 | gold | not in top12 contracts |
| `event-runbook-orchestrator` | skill | medium | 100 | 100 | gold | not in top12 contracts |
| `podcast-show-notes-generator` | skill | low | 100 | 100 | gold | not in top12 contracts |
| `community-moderation-coach` | skill | high | 100 | 100 | gold | not in top12 contracts |
| `operator-chief` | personality | low | 100 | 100 | gold | not in top12 contracts |
| `warm-coach` | personality | low | 100 | 100 | gold | not in top12 contracts |
| `skeptical-analyst` | personality | medium | 100 | 100 | gold | not in top12 contracts |
| `founder-copilot` | personality | medium | 100 | 100 | gold | not in top12 contracts |
| `professor-socratic` | personality | low | 100 | 100 | gold | not in top12 contracts |
| `no-fluff-editor` | personality | low | 100 | 100 | gold | not in top12 contracts |
| `empathetic-support-agent` | personality | medium | 100 | 100 | gold | not in top12 contracts |
| `security-paranoid` | personality | high | 100 | 100 | gold | not in top12 contracts |
| `creative-spark` | personality | low | 100 | 100 | gold | not in top12 contracts |
| `data-journalist` | personality | medium | 100 | 100 | gold | not in top12 contracts |
| `negotiation-strategist` | personality | medium | 100 | 100 | gold | not in top12 contracts |
| `incident-commander` | personality | high | 100 | 100 | gold | not in top12 contracts |
| `patient-therapist-lite` | personality | high | 100 | 100 | gold | not in top12 contracts |
| `sales-closer` | personality | medium | 100 | 100 | gold | not in top12 contracts |
| `family-organizer` | personality | low | 100 | 100 | gold | not in top12 contracts |

## 6) Artifacts
- `/Users/claw/.openclaw/workspace/botstore/research/candidate-packs-v3.json`
- `/Users/claw/.openclaw/workspace/botstore/research/candidate-packs-v3-quality-report.md`
- `/Users/claw/.openclaw/workspace/botstore/research/candidate-packs-v3-quality-result.json`
- `/Users/claw/.openclaw/workspace/botstore/research/runtime-simulation-v3-report.md`
- `/Users/claw/.openclaw/workspace/botstore/research/runtime-simulation-v3-result.json`
- `/Users/claw/.openclaw/workspace/botstore/research/pack-performance-contracts-v3.json`
- `/Users/claw/.openclaw/workspace/botstore/research/v3-promotion-list.json`
