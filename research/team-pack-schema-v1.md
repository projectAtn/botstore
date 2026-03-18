# Team Pack Schema v1

## Purpose
Define multi-agent compositions where each sub-agent has a role personality, assigned skills, handoff rules, and output contracts.

## Object

```json
{
  "slug": "startup-exec-team",
  "title": "Startup Exec Team",
  "version": "0.1.0",
  "purpose": "Weekly strategic operating rhythm for startup decisions",
  "team_type": "executive",
  "shared_skills": ["crm-sync-bidirectional", "calendar-ops-coordinator"],
  "roles": [
    {
      "role": "CEO",
      "personality_slug": "calm-chief-of-staff-persona",
      "owned_skills": ["product-strategy-pack"],
      "deliverables": ["weekly-priority-memo", "decision-log"],
      "kpis": ["decision-latency", "goal-clarity"]
    }
  ],
  "orchestration": {
    "trigger": "manual|scheduled",
    "cadence": "weekly",
    "handoff_order": ["CEO", "CFO", "CMO", "COO"],
    "conflict_policy": "CFO veto on budget risk > threshold; CEO final call",
    "approval_gates": ["policy", "budget", "security"]
  },
  "output_contract": {
    "format": "markdown",
    "sections": ["Summary", "Decisions", "Actions", "Risks", "Owners"]
  },
  "risk_level": "medium"
}
```

## QA dimensions
- Capability coverage (required vs available)
- Role coverage (required roles present)
- Artifact coverage (scenario-required outputs)
- Governance readiness (approval gates + conflict policy)
- Execution quality (scenario pass score)

## Score formula
`score = 0.5*capability_coverage + 0.3*role_coverage + 0.2*artifact_coverage`

Pass threshold: `>= 0.80`
