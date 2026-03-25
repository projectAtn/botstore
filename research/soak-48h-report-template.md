# 48h Unattended Soak Report (Template)

## Run Metadata
- Run ID:
- Window (UTC):
- Mode: `live` / `dry-run`
- Seed:
- Scheduler cadence: 20 minutes fixed
- Planned cycles:
- Executed cycles:

## Scenario Mix (Required vs Observed)
| Scenario | Required | Observed | Match |
|---|---:|---:|---|
| steady_state |  |  |  |
| policy_pressure |  |  |  |
| trust_path |  |  |  |
| monitoring_probe |  |  |  |
| rollback_drill |  |  |  |

## SLO Time-Series Summary
- Source JSONL:
- Source summary JSON:
- Key metrics (latest):
  - policy.quarantine_rate:
  - policy.approval_latency_minutes_avg:
  - policy.activation_failure_rate_proxy:
  - alert.pass_ratio:
  - phase_gate.pass_ratio:
  - launch.pass_ratio:

## Pass/Fail Rubric
- [ ] All planned cycles executed
- [ ] Scenario mix exactly matched required deterministic mix
- [ ] No unresolved critical command failures
- [ ] Alert envelope remained available (`alert.all_pass = true` for all checks)
- [ ] Phase gate remained green (`phase_gate.all_pass = true`)
- [ ] Launch scorecard remained GO

## Failure Analysis
- Failure artifact path:
- Distinct failure signatures:
- First failure timestamp:
- Last failure timestamp:
- Recovery behavior notes:

## Operator Notes
- Known environment constraints:
- Deviations from plan:
- Follow-up actions:
