# Runtime Simulation Verification Report

Candidates: 18
Final verified (tier+risk gate): 16

| slug | type | risk | score | tier | risk_gate | final_verified |
|---|---|---|---:|---|---|---|
| `model-switchboard` | skill | low | 100 | gold | ✅ | ✅ |
| `workflow-version-pinning` | skill | low | 100 | gold | ✅ | ✅ |
| `fact-source-verifier` | skill | low | 75 | bronze | ✅ | ✅ |
| `synthetic-media-checker` | skill | low | 100 | gold | ✅ | ✅ |
| `policy-compliance-guard` | skill | high | 100 | gold | ✅ | ✅ |
| `cost-governor` | skill | low | 75 | bronze | ✅ | ✅ |
| `autonomous-retry-recovery` | skill | low | 100 | gold | ✅ | ✅ |
| `human-escalation-router` | skill | medium | 100 | gold | ✅ | ✅ |
| `tool-health-monitor` | skill | low | 75 | bronze | ✅ | ✅ |
| `private-local-execution` | skill | medium | 100 | gold | ✅ | ✅ |
| `web-action-proof-logger` | skill | low | 100 | gold | ✅ | ✅ |
| `task-contract-engine` | skill | low | 75 | bronze | ✅ | ✅ |
| `ops-chief-persona` | personality | low | 75 | bronze | ✅ | ✅ |
| `safety-analyst-persona` | personality | low | 100 | gold | ✅ | ✅ |
| `research-scholar-persona` | personality | low | 75 | bronze | ✅ | ✅ |
| `cfo-assistant-persona` | personality | low | 75 | bronze | ✅ | ✅ |
| `autonomous-worker-persona` | personality | medium | 75 | bronze | ❌ | ❌ |
| `enterprise-assistant-persona` | personality | medium | 75 | bronze | ❌ | ❌ |

## Detailed test results

### Model Switchboard (`model-switchboard`) — tier: gold, required: 75, score: 100
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Workflow Version Pinning (`workflow-version-pinning`) — tier: gold, required: 75, score: 100
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Fact & Source Verifier (`fact-source-verifier`) — tier: bronze, required: 75, score: 75
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Synthetic Media Checker (`synthetic-media-checker`) — tier: gold, required: 75, score: 100
- ✅ **declares_scopes** — scope_count=1
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Policy & Compliance Guard (`policy-compliance-guard`) — tier: gold, required: 95, score: 100
- ✅ **declares_scopes** — scope_count=4
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=True, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Cost Governor (`cost-governor`) — tier: bronze, required: 75, score: 75
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Autonomous Retry & Recovery (`autonomous-retry-recovery`) — tier: gold, required: 75, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Human Escalation Router (`human-escalation-router`) — tier: gold, required: 85, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=True, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Tool Health Monitor (`tool-health-monitor`) — tier: bronze, required: 75, score: 75
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Private Local Execution (`private-local-execution`) — tier: gold, required: 85, score: 100
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Web Action Proof Logger (`web-action-proof-logger`) — tier: gold, required: 75, score: 100
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Task Contract Engine (`task-contract-engine`) — tier: bronze, required: 75, score: 75
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### No-BS Ops Chief (`ops-chief-persona`) — tier: bronze, required: 75, score: 75
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Safety-First Analyst (`safety-analyst-persona`) — tier: gold, required: 75, score: 100
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Research Scholar (`research-scholar-persona`) — tier: bronze, required: 75, score: 75
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Cost-Conscious CFO Assistant (`cfo-assistant-persona`) — tier: bronze, required: 75, score: 75
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Autonomous Worker (`autonomous-worker-persona`) — tier: bronze, required: 85, score: 75
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=True, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Audit-Ready Enterprise Assistant (`enterprise-assistant-persona`) — tier: bronze, required: 85, score: 75
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3
