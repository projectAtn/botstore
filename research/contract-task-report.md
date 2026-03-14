# Contract Task Runner Report

Total contracts: 8
Pass: 8
Average score: 87.5

| slug | risk | min_score | score | pass | latency_ms |
|---|---|---:|---:|---|---:|
| `inbox-calendar-ops` | medium | 90 | 100 | ✅ | 12.2 |
| `research-analyst` | low | 75 | 100 | ✅ | 6.0 |
| `fact-source-verifier` | low | 75 | 80 | ✅ | 5.7 |
| `policy-compliance-guard` | high | 95 | 100 | ✅ | 7.1 |
| `autonomous-retry-recovery` | low | 75 | 80 | ✅ | 5.5 |
| `human-escalation-router` | low | 75 | 80 | ✅ | 6.5 |
| `private-local-execution` | low | 75 | 80 | ✅ | 5.5 |
| `task-contract-engine` | low | 75 | 80 | ✅ | 5.4 |

## Details

### `inbox-calendar-ops` — Can support inbox triage and calendar scheduling workflows.
- ✅ **scope_coverage** — required=['calendar.read', 'calendar.write', 'email.read', 'email.send'], pack=['calendar.read', 'calendar.write', 'email.read', 'email.send']
- ✅ **policy_expectation** — expected=require_approval, got=require_approval
- ✅ **discoverable_by_required_capabilities** — top_results=['inbox-calendar-ops', 'service-ops-verticals', 'founder-command-bundle', 'universal-connector-auth', 'policy-compliance-guard']
- ✅ **install_by_capability_selects_pack** — installed=['inbox-calendar-ops']
- ✅ **deterministic_primary_selection** — required=True, first_installed=inbox-calendar-ops

### `research-analyst` — Can perform web-grounded research and summarization.
- ✅ **scope_coverage** — required=['web.fetch', 'web.search'], pack=['files.read', 'web.fetch', 'web.search']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['research-analyst', 'quality-eval-gate', 'fact-source-verifier', 'browser-operator-pro', 'research-scholar-persona']
- ✅ **install_by_capability_selects_pack** — installed=['research-analyst']
- ✅ **deterministic_primary_selection** — required=False, first_installed=research-analyst

### `fact-source-verifier` — Can validate factual claims with sources.
- ✅ **scope_coverage** — required=['web.fetch', 'web.search'], pack=['files.read', 'web.fetch', 'web.search']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['research-analyst', 'quality-eval-gate', 'fact-source-verifier', 'browser-operator-pro', 'research-scholar-persona']
- ❌ **install_by_capability_selects_pack** — installed=['research-analyst']
- ✅ **deterministic_primary_selection** — required=False, first_installed=research-analyst

### `policy-compliance-guard` — Can evaluate and gate risky actions before execution.
- ✅ **scope_coverage** — required=['email.send', 'message.send'], pack=['email.send', 'files.read', 'files.write', 'message.send']
- ✅ **policy_expectation** — expected=require_approval, got=require_approval
- ✅ **discoverable_by_required_capabilities** — top_results=['policy-compliance-guard', 'human-escalation-router', 'approval-policy-brain', 'inbox-calendar-ops', 'multi-agent-orchestrator']
- ✅ **install_by_capability_selects_pack** — installed=['policy-compliance-guard']
- ✅ **deterministic_primary_selection** — required=True, first_installed=policy-compliance-guard

### `autonomous-retry-recovery` — Can recover from transient task failures and retry safely.
- ✅ **scope_coverage** — required=['memory.read', 'memory.write'], pack=['files.write', 'memory.read', 'memory.write']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['capability-discovery-engine', 'memory-architect', 'task-decomposer', 'model-switchboard', 'cost-governor']
- ❌ **install_by_capability_selects_pack** — installed=['capability-discovery-engine']
- ✅ **deterministic_primary_selection** — required=False, first_installed=capability-discovery-engine

### `human-escalation-router` — Can escalate uncertain/high-risk actions to a human.
- ✅ **scope_coverage** — required=['message.send'], pack=['email.send', 'memory.read', 'message.send']
- ✅ **policy_expectation** — expected=require_approval, got=require_approval
- ✅ **discoverable_by_required_capabilities** — top_results=['approval-policy-brain', 'policy-compliance-guard', 'multi-agent-orchestrator', 'human-escalation-router', 'inbox-calendar-ops']
- ❌ **install_by_capability_selects_pack** — installed=['approval-policy-brain']
- ✅ **deterministic_primary_selection** — required=False, first_installed=approval-policy-brain

### `private-local-execution` — Can route sensitive tasks through private/local pathways.
- ✅ **scope_coverage** — required=['files.read', 'memory.read'], pack=['files.read', 'files.write', 'memory.read']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['memory-architect', 'private-local-execution', 'research-analyst', 'capability-discovery-engine', 'task-decomposer']
- ❌ **install_by_capability_selects_pack** — installed=['memory-architect']
- ✅ **deterministic_primary_selection** — required=False, first_installed=memory-architect

### `task-contract-engine` — Can convert vague tasks into measurable acceptance criteria.
- ✅ **scope_coverage** — required=['memory.read', 'memory.write'], pack=['memory.read', 'memory.write']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['capability-discovery-engine', 'memory-architect', 'task-decomposer', 'model-switchboard', 'cost-governor']
- ❌ **install_by_capability_selects_pack** — installed=['capability-discovery-engine']
- ✅ **deterministic_primary_selection** — required=False, first_installed=capability-discovery-engine

