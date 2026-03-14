# V2 Intake Pipeline Summary

Generated: 2026-03-14T12:00:31.900943+00:00

## 1) Merge
- Merged output: `/Users/claw/.openclaw/workspace/botstore/research/candidate-packs-v2.json`
- Total merged candidates: **37**
- Source counts (pre-dedup): skills=25, personalities=12
- Duplicate slugs overwritten: none

## 2) Existing checks
- `quality_check_candidates.py`: PASS
- `runtime_simulation_verify.py`: PASS

## 3) Runtime simulation outcome
- Verified slugs: **12**
- Delist recommendations: **25**

| slug | risk | score | required | final_verified | recommendation |
|---|---|---:|---:|---|---|
| `inbox-triage-ops` | medium | 75 | 85 | ❌ | **DELIST** |
| `calendar-negotiator` | medium | 100 | 85 | ✅ | **KEEP** |
| `sales-crm-autopilot` | medium | 75 | 85 | ❌ | **DELIST** |
| `customer-support-copilot` | high | 100 | 95 | ✅ | **KEEP** |
| `finance-expense-audit` | high | 100 | 95 | ✅ | **KEEP** |
| `contract-lifecycle-assistant` | high | 75 | 95 | ❌ | **DELIST** |
| `recruiting-pipeline-manager` | high | 75 | 95 | ❌ | **DELIST** |
| `onboarding-automation-suite` | medium | 75 | 85 | ❌ | **DELIST** |
| `knowledge-base-steward` | low | 100 | 75 | ✅ | **KEEP** |
| `meeting-intelligence-pack` | medium | 75 | 85 | ❌ | **DELIST** |
| `incident-response-commander` | high | 75 | 95 | ❌ | **DELIST** |
| `cloud-cost-optimizer` | medium | 75 | 85 | ❌ | **DELIST** |
| `security-posture-guardian` | high | 75 | 95 | ❌ | **DELIST** |
| `compliance-evidence-collector` | high | 100 | 95 | ✅ | **KEEP** |
| `marketing-campaign-orchestrator` | medium | 75 | 85 | ❌ | **DELIST** |
| `seo-content-factory` | medium | 75 | 85 | ❌ | **DELIST** |
| `ecommerce-ops-agent` | medium | 75 | 85 | ❌ | **DELIST** |
| `procurement-sourcing-copilot` | high | 75 | 95 | ❌ | **DELIST** |
| `social-listening-response` | high | 100 | 95 | ✅ | **KEEP** |
| `research-synthesizer-pro` | medium | 75 | 85 | ❌ | **DELIST** |
| `data-pipeline-guardian` | high | 75 | 95 | ❌ | **DELIST** |
| `qa-regression-automator` | medium | 75 | 85 | ❌ | **DELIST** |
| `dev-docs-auto-maintainer` | low | 100 | 75 | ✅ | **KEEP** |
| `real-estate-deal-assistant` | high | 75 | 95 | ❌ | **DELIST** |
| `healthcare-intake-navigator` | high | 75 | 95 | ❌ | **DELIST** |
| `ops-sre-incident-commander` | medium | 100 | 85 | ✅ | **KEEP** |
| `compliance-policy-auditor` | high | 75 | 95 | ❌ | **DELIST** |
| `finops-cloud-cost-steward` | medium | 75 | 85 | ❌ | **DELIST** |
| `vendor-procurement-negotiator` | medium | 75 | 85 | ❌ | **DELIST** |
| `revops-pipeline-coach` | medium | 75 | 85 | ❌ | **DELIST** |
| `customer-support-deescalation-specialist` | low | 100 | 75 | ✅ | **KEEP** |
| `security-soc-triage-analyst` | high | 100 | 95 | ✅ | **KEEP** |
| `hr-people-ops-coach` | high | 75 | 95 | ❌ | **DELIST** |
| `data-governance-steward` | medium | 75 | 85 | ❌ | **DELIST** |
| `portfolio-program-execution-director` | medium | 75 | 85 | ❌ | **DELIST** |
| `ai-product-red-teamer` | high | 100 | 95 | ✅ | **KEEP** |
| `autonomous-ops-orchestrator` | high | 100 | 95 | ✅ | **KEEP** |

## 4) Execution logs (trimmed)

### quality_check_candidates.py
```text
Wrote /Users/claw/.openclaw/workspace/botstore/research/candidate-packs-quality-report.md
Pass: 37/37
```

### runtime_simulation_verify.py
```text
Wrote /Users/claw/.openclaw/workspace/botstore/research/runtime-simulation-report.md
Verified: 12/37
Wrote /Users/claw/.openclaw/workspace/botstore/research/runtime-simulation-result.json
```

## 5) Output artifacts
- `/Users/claw/.openclaw/workspace/botstore/research/candidate-packs-quality-report.md`
- `/Users/claw/.openclaw/workspace/botstore/research/runtime-simulation-report.md`
- `/Users/claw/.openclaw/workspace/botstore/research/runtime-simulation-result.json`
