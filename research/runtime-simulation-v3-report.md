# Runtime Simulation V3 Report

Generated: 2026-03-14T12:31:52.177355+00:00
Candidates: 45
Final verified (strict tier+risk gate): 45

| slug | type | risk | score | tier | required | risk_gate | final_verified |
|---|---|---|---:|---|---:|---|---|
| `inbox-triage-pro` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `calendar-conflict-resolver` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `meeting-brief-builder` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `research-citation-packager` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `expense-receipt-organizer` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `travel-itinerary-concierge` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `job-application-accelerator` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `codebase-onboarding-guide` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `pr-review-summarizer` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `incident-postmortem-writer` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `contract-redline-assistant` | skill | high | 100 | gold | 95 | ✅ | ✅ |
| `policy-sop-generator` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `social-content-repurposer` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `ad-copy-ab-tester` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `seo-content-optimizer` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `customer-feedback-clusterer` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `support-ticket-autoprioritizer` | skill | high | 100 | gold | 95 | ✅ | ✅ |
| `oncall-handoff-assistant` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `database-migration-guard` | skill | high | 100 | gold | 95 | ✅ | ✅ |
| `api-change-impact-analyzer` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `docs-to-faq-converter` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `learning-path-designer` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `fitness-plan-adapter` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `meal-prep-planner` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `budget-guardrails-coach` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `subscription-leak-finder` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `home-maintenance-scheduler` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `event-runbook-orchestrator` | skill | medium | 100 | gold | 90 | ✅ | ✅ |
| `podcast-show-notes-generator` | skill | low | 100 | gold | 80 | ✅ | ✅ |
| `community-moderation-coach` | skill | high | 100 | gold | 95 | ✅ | ✅ |
| `operator-chief` | personality | low | 100 | gold | 80 | ✅ | ✅ |
| `warm-coach` | personality | low | 100 | gold | 80 | ✅ | ✅ |
| `skeptical-analyst` | personality | medium | 100 | gold | 90 | ✅ | ✅ |
| `founder-copilot` | personality | medium | 100 | gold | 90 | ✅ | ✅ |
| `professor-socratic` | personality | low | 100 | gold | 80 | ✅ | ✅ |
| `no-fluff-editor` | personality | low | 100 | gold | 80 | ✅ | ✅ |
| `empathetic-support-agent` | personality | medium | 100 | gold | 90 | ✅ | ✅ |
| `security-paranoid` | personality | high | 100 | gold | 95 | ✅ | ✅ |
| `creative-spark` | personality | low | 100 | gold | 80 | ✅ | ✅ |
| `data-journalist` | personality | medium | 100 | gold | 90 | ✅ | ✅ |
| `negotiation-strategist` | personality | medium | 100 | gold | 90 | ✅ | ✅ |
| `incident-commander` | personality | high | 100 | gold | 95 | ✅ | ✅ |
| `patient-therapist-lite` | personality | high | 100 | gold | 95 | ✅ | ✅ |
| `sales-closer` | personality | medium | 100 | gold | 90 | ✅ | ✅ |
| `family-organizer` | personality | low | 100 | gold | 80 | ✅ | ✅ |

## Detailed test results

### Inbox Triage Pro (`inbox-triage-pro`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Calendar Conflict Resolver (`calendar-conflict-resolver`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Meeting Brief Builder (`meeting-brief-builder`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Research Citation Packager (`research-citation-packager`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Expense Receipt Organizer (`expense-receipt-organizer`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Travel Itinerary Concierge (`travel-itinerary-concierge`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Job Application Accelerator (`job-application-accelerator`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Codebase Onboarding Guide (`codebase-onboarding-guide`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### PR Review Summarizer (`pr-review-summarizer`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Incident Postmortem Writer (`incident-postmortem-writer`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Contract Redline Assistant (`contract-redline-assistant`) — tier: gold, required: 95, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Policy & SOP Generator (`policy-sop-generator`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Social Content Repurposer (`social-content-repurposer`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Ad Copy A/B Tester (`ad-copy-ab-tester`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### SEO Content Optimizer (`seo-content-optimizer`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Customer Feedback Clusterer (`customer-feedback-clusterer`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Support Ticket Autoprioritizer (`support-ticket-autoprioritizer`) — tier: gold, required: 95, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### On-call Handoff Assistant (`oncall-handoff-assistant`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Database Migration Guard (`database-migration-guard`) — tier: gold, required: 95, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### API Change Impact Analyzer (`api-change-impact-analyzer`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Docs-to-FAQ Converter (`docs-to-faq-converter`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Learning Path Designer (`learning-path-designer`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Fitness Plan Adapter (`fitness-plan-adapter`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Meal Prep Planner (`meal-prep-planner`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Budget Guardrails Coach (`budget-guardrails-coach`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Subscription Leak Finder (`subscription-leak-finder`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Home Maintenance Scheduler (`home-maintenance-scheduler`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Event Runbook Orchestrator (`event-runbook-orchestrator`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Podcast Show Notes Generator (`podcast-show-notes-generator`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Community Moderation Coach (`community-moderation-coach`) — tier: gold, required: 95, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Operator Chief (`operator-chief`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Warm Coach (`warm-coach`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Skeptical Analyst (`skeptical-analyst`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Founder Copilot (`founder-copilot`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Professor Socratic (`professor-socratic`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### No-Fluff Editor (`no-fluff-editor`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Empathetic Support Agent (`empathetic-support-agent`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Security Paranoid (`security-paranoid`) — tier: gold, required: 95, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Creative Spark (`creative-spark`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Data Journalist (`data-journalist`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Negotiation Strategist (`negotiation-strategist`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Incident Commander (`incident-commander`) — tier: gold, required: 95, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Patient Therapist Lite (`patient-therapist-lite`) — tier: gold, required: 95, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Sales Closer (`sales-closer`) — tier: gold, required: 90, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars

### Family Organizer (`family-organizer`) — tier: gold, required: 80, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback/guardrail
- ✅ **has_min_quality_tests** — quality_tests=4
- ✅ **problem_statement_substantive** — problem length >= 40 chars
