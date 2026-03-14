# Contract Task Runner Report

Total contracts: 8
Pass: 8
Average score: 81.2

| slug | score | pass | latency_ms |
|---|---:|---|---:|
| `inbox-calendar-ops` | 100 | ✅ | 11.0 |
| `research-analyst` | 100 | ✅ | 5.7 |
| `fact-source-verifier` | 75 | ✅ | 5.5 |
| `policy-compliance-guard` | 75 | ✅ | 6.6 |
| `autonomous-retry-recovery` | 75 | ✅ | 5.4 |
| `human-escalation-router` | 75 | ✅ | 6.5 |
| `private-local-execution` | 75 | ✅ | 5.3 |
| `task-contract-engine` | 75 | ✅ | 5.8 |

## Details

### `inbox-calendar-ops` — Can support inbox triage and calendar scheduling workflows.
- ✅ **scope_coverage** — required=['calendar.read', 'calendar.write', 'email.read', 'email.send'], pack=['calendar.read', 'calendar.write', 'email.read', 'email.send']
- ✅ **policy_expectation** — expected=require_approval, got=require_approval
- ✅ **discoverable_by_required_capabilities** — top_results=['inbox-calendar-ops', 'service-ops-verticals', 'founder-command-bundle', 'universal-connector-auth', 'human-escalation-router']
- ✅ **install_by_capability_selects_pack** — installed=['inbox-calendar-ops']

### `research-analyst` — Can perform web-grounded research and summarization.
- ✅ **scope_coverage** — required=['web.fetch', 'web.search'], pack=['files.read', 'web.fetch', 'web.search']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['research-analyst', 'quality-eval-gate', 'fact-source-verifier', 'browser-operator-pro', 'research-scholar-persona']
- ✅ **install_by_capability_selects_pack** — installed=['research-analyst']

### `fact-source-verifier` — Can validate factual claims with sources.
- ✅ **scope_coverage** — required=['web.fetch', 'web.search'], pack=['files.read', 'web.fetch', 'web.search']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['research-analyst', 'quality-eval-gate', 'fact-source-verifier', 'browser-operator-pro', 'research-scholar-persona']
- ❌ **install_by_capability_selects_pack** — installed=['research-analyst']

### `policy-compliance-guard` — Can evaluate and gate risky actions before execution.
- ✅ **scope_coverage** — required=['email.send', 'message.send'], pack=['email.send', 'files.read', 'files.write', 'message.send']
- ✅ **policy_expectation** — expected=require_approval, got=require_approval
- ✅ **discoverable_by_required_capabilities** — top_results=['human-escalation-router', 'policy-compliance-guard', 'inbox-calendar-ops', 'multi-agent-orchestrator', 'service-ops-verticals']
- ❌ **install_by_capability_selects_pack** — installed=['human-escalation-router']

### `autonomous-retry-recovery` — Can recover from transient task failures and retry safely.
- ✅ **scope_coverage** — required=['memory.read', 'memory.write'], pack=['files.write', 'memory.read', 'memory.write']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['capability-discovery-engine', 'memory-architect', 'task-decomposer', 'model-switchboard', 'cost-governor']
- ❌ **install_by_capability_selects_pack** — installed=['capability-discovery-engine']

### `human-escalation-router` — Can escalate uncertain/high-risk actions to a human.
- ✅ **scope_coverage** — required=['message.send'], pack=['email.send', 'memory.read', 'message.send']
- ✅ **policy_expectation** — expected=require_approval, got=require_approval
- ✅ **discoverable_by_required_capabilities** — top_results=['multi-agent-orchestrator', 'human-escalation-router', 'approval-policy-brain', 'policy-compliance-guard', 'research-analyst']
- ❌ **install_by_capability_selects_pack** — installed=['multi-agent-orchestrator']

### `private-local-execution` — Can route sensitive tasks through private/local pathways.
- ✅ **scope_coverage** — required=['files.read', 'memory.read'], pack=['files.read', 'files.write', 'memory.read']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['memory-architect', 'private-local-execution', 'research-analyst', 'capability-discovery-engine', 'task-decomposer']
- ❌ **install_by_capability_selects_pack** — installed=['memory-architect']

### `task-contract-engine` — Can convert vague tasks into measurable acceptance criteria.
- ✅ **scope_coverage** — required=['memory.read', 'memory.write'], pack=['memory.read', 'memory.write']
- ✅ **policy_expectation** — expected=allow, got=allow
- ✅ **discoverable_by_required_capabilities** — top_results=['capability-discovery-engine', 'memory-architect', 'task-decomposer', 'model-switchboard', 'cost-governor']
- ❌ **install_by_capability_selects_pack** — installed=['capability-discovery-engine']

