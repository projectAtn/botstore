# Runtime Simulation V3 Report

Generated: 2026-03-14T12:30:59.329539+00:00
Candidates: 45
Final verified (strict tier+risk gate): 2

| slug | type | risk | score | tier | required | risk_gate | final_verified |
|---|---|---|---:|---|---:|---|---|
| `inbox-triage-pro` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `calendar-conflict-resolver` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `meeting-brief-builder` | skill | low | 60 | unverified | 80 | ❌ | ❌ |
| `research-citation-packager` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `expense-receipt-organizer` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `travel-itinerary-concierge` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `job-application-accelerator` | skill | low | 60 | unverified | 80 | ❌ | ❌ |
| `codebase-onboarding-guide` | skill | low | 60 | unverified | 80 | ❌ | ❌ |
| `pr-review-summarizer` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `incident-postmortem-writer` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `contract-redline-assistant` | skill | high | 80 | bronze | 95 | ❌ | ❌ |
| `policy-sop-generator` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `social-content-repurposer` | skill | low | 60 | unverified | 80 | ❌ | ❌ |
| `ad-copy-ab-tester` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `seo-content-optimizer` | skill | low | 60 | unverified | 80 | ❌ | ❌ |
| `customer-feedback-clusterer` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `support-ticket-autoprioritizer` | skill | high | 80 | bronze | 95 | ❌ | ❌ |
| `oncall-handoff-assistant` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `database-migration-guard` | skill | high | 80 | bronze | 95 | ❌ | ❌ |
| `api-change-impact-analyzer` | skill | medium | 80 | bronze | 90 | ❌ | ❌ |
| `docs-to-faq-converter` | skill | low | 60 | unverified | 80 | ❌ | ❌ |
| `learning-path-designer` | skill | low | 60 | unverified | 80 | ❌ | ❌ |
| `fitness-plan-adapter` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `meal-prep-planner` | skill | low | 60 | unverified | 80 | ❌ | ❌ |
| `budget-guardrails-coach` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `subscription-leak-finder` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `home-maintenance-scheduler` | skill | low | 80 | bronze | 80 | ✅ | ✅ |
| `event-runbook-orchestrator` | skill | medium | 60 | unverified | 90 | ❌ | ❌ |
| `podcast-show-notes-generator` | skill | low | 60 | unverified | 80 | ❌ | ❌ |
| `community-moderation-coach` | skill | high | 80 | bronze | 95 | ❌ | ❌ |
| `operator-chief` | personality | low | 60 | unverified | 80 | ❌ | ❌ |
| `warm-coach` | personality | low | 60 | unverified | 80 | ❌ | ❌ |
| `skeptical-analyst` | personality | medium | 60 | unverified | 90 | ❌ | ❌ |
| `founder-copilot` | personality | medium | 60 | unverified | 90 | ❌ | ❌ |
| `professor-socratic` | personality | low | 60 | unverified | 80 | ❌ | ❌ |
| `no-fluff-editor` | personality | low | 60 | unverified | 80 | ❌ | ❌ |
| `empathetic-support-agent` | personality | medium | 60 | unverified | 90 | ❌ | ❌ |
| `security-paranoid` | personality | high | 60 | unverified | 95 | ❌ | ❌ |
| `creative-spark` | personality | low | 80 | bronze | 80 | ✅ | ✅ |
| `data-journalist` | personality | medium | 60 | unverified | 90 | ❌ | ❌ |
| `negotiation-strategist` | personality | medium | 60 | unverified | 90 | ❌ | ❌ |
| `incident-commander` | personality | high | 80 | bronze | 95 | ❌ | ❌ |
| `patient-therapist-lite` | personality | high | 60 | unverified | 95 | ❌ | ❌ |
| `sales-closer` | personality | medium | 60 | unverified | 90 | ❌ | ❌ |
| `family-organizer` | personality | low | 60 | unverified | 80 | ❌ | ❌ |

## Detailed test results

### Inbox Triage Pro (`inbox-triage-pro`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Calendar Conflict Resolver (`calendar-conflict-resolver`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Meeting Brief Builder (`meeting-brief-builder`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Research Citation Packager (`research-citation-packager`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Expense Receipt Organizer (`expense-receipt-organizer`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Travel Itinerary Concierge (`travel-itinerary-concierge`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Job Application Accelerator (`job-application-accelerator`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Codebase Onboarding Guide (`codebase-onboarding-guide`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### PR Review Summarizer (`pr-review-summarizer`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Incident Postmortem Writer (`incident-postmortem-writer`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Contract Redline Assistant (`contract-redline-assistant`) — tier: bronze, required: 95, score: 80
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Policy & SOP Generator (`policy-sop-generator`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Social Content Repurposer (`social-content-repurposer`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Ad Copy A/B Tester (`ad-copy-ab-tester`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### SEO Content Optimizer (`seo-content-optimizer`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Customer Feedback Clusterer (`customer-feedback-clusterer`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Support Ticket Autoprioritizer (`support-ticket-autoprioritizer`) — tier: bronze, required: 95, score: 80
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### On-call Handoff Assistant (`oncall-handoff-assistant`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Database Migration Guard (`database-migration-guard`) — tier: bronze, required: 95, score: 80
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### API Change Impact Analyzer (`api-change-impact-analyzer`) — tier: bronze, required: 90, score: 80
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Docs-to-FAQ Converter (`docs-to-faq-converter`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Learning Path Designer (`learning-path-designer`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Fitness Plan Adapter (`fitness-plan-adapter`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Meal Prep Planner (`meal-prep-planner`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Budget Guardrails Coach (`budget-guardrails-coach`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Subscription Leak Finder (`subscription-leak-finder`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Home Maintenance Scheduler (`home-maintenance-scheduler`) — tier: bronze, required: 80, score: 80
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Event Runbook Orchestrator (`event-runbook-orchestrator`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Podcast Show Notes Generator (`podcast-show-notes-generator`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Community Moderation Coach (`community-moderation-coach`) — tier: bronze, required: 95, score: 80
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Operator Chief (`operator-chief`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Warm Coach (`warm-coach`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Skeptical Analyst (`skeptical-analyst`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Founder Copilot (`founder-copilot`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Professor Socratic (`professor-socratic`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### No-Fluff Editor (`no-fluff-editor`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Empathetic Support Agent (`empathetic-support-agent`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Security Paranoid (`security-paranoid`) — tier: unverified, required: 95, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Creative Spark (`creative-spark`) — tier: bronze, required: 80, score: 80
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Data Journalist (`data-journalist`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Negotiation Strategist (`negotiation-strategist`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Incident Commander (`incident-commander`) — tier: bronze, required: 95, score: 80
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Patient Therapist Lite (`patient-therapist-lite`) — tier: unverified, required: 95, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Sales Closer (`sales-closer`) — tier: unverified, required: 90, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Family Organizer (`family-organizer`) — tier: unverified, required: 80, score: 60
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ❌ **has_min_quality_tests** — quality_tests=3
- ✅ **problem_statement_substantive** — problem length >= 40 chars
