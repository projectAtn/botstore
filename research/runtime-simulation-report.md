# Runtime Simulation Verification Report

Candidates: 18
Verified (>=75): 18

| slug | type | score | verified |
|---|---|---:|---|
| `model-switchboard` | skill | 100 | ✅ |
| `workflow-version-pinning` | skill | 100 | ✅ |
| `fact-source-verifier` | skill | 75 | ✅ |
| `synthetic-media-checker` | skill | 100 | ✅ |
| `policy-compliance-guard` | skill | 100 | ✅ |
| `cost-governor` | skill | 75 | ✅ |
| `autonomous-retry-recovery` | skill | 100 | ✅ |
| `human-escalation-router` | skill | 100 | ✅ |
| `tool-health-monitor` | skill | 75 | ✅ |
| `private-local-execution` | skill | 100 | ✅ |
| `web-action-proof-logger` | skill | 100 | ✅ |
| `task-contract-engine` | skill | 75 | ✅ |
| `ops-chief-persona` | personality | 75 | ✅ |
| `safety-analyst-persona` | personality | 100 | ✅ |
| `research-scholar-persona` | personality | 75 | ✅ |
| `cfo-assistant-persona` | personality | 75 | ✅ |
| `autonomous-worker-persona` | personality | 75 | ✅ |
| `enterprise-assistant-persona` | personality | 75 | ✅ |

## Detailed test results

### Model Switchboard (`model-switchboard`)
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Workflow Version Pinning (`workflow-version-pinning`)
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Fact & Source Verifier (`fact-source-verifier`)
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Synthetic Media Checker (`synthetic-media-checker`)
- ✅ **declares_scopes** — scope_count=1
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Policy & Compliance Guard (`policy-compliance-guard`)
- ✅ **declares_scopes** — scope_count=4
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=True, risk=high
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Cost Governor (`cost-governor`)
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Autonomous Retry & Recovery (`autonomous-retry-recovery`)
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Human Escalation Router (`human-escalation-router`)
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=True, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Tool Health Monitor (`tool-health-monitor`)
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Private Local Execution (`private-local-execution`)
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Web Action Proof Logger (`web-action-proof-logger`)
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Task Contract Engine (`task-contract-engine`)
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### No-BS Ops Chief (`ops-chief-persona`)
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Safety-First Analyst (`safety-analyst-persona`)
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ✅ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Research Scholar (`research-scholar-persona`)
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Cost-Conscious CFO Assistant (`cfo-assistant-persona`)
- ✅ **declares_scopes** — scope_count=2
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=low
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Autonomous Worker (`autonomous-worker-persona`)
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=True, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3

### Audit-Ready Enterprise Assistant (`enterprise-assistant-persona`)
- ✅ **declares_scopes** — scope_count=3
- ✅ **risk_matches_scope_sensitivity** — has_sensitive=False, risk=medium
- ❌ **has_recoverability_or_audit_signal** — includes fallback/retry/audit/log/escalation/rollback
- ✅ **has_min_quality_tests** — quality_tests=3
