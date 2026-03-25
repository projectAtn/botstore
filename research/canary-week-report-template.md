# Canary Week Report Template (7-Day External Rollout)

Use this template to produce the final canary evidence packet.

## Metadata

- Window start (UTC):
- Window end (UTC):
- Days observed:
- Owner:
- Environment:

## Rollout Scope

- Cohort / tenant set:
- Traffic share:
- Runtime(s):
- Policy bundle hash/version:

## Daily Health Summary

| Day | Date (UTC) | Availability | Errors | Trust verify failures | Alert state | Notes |
|---|---|---:|---:|---:|---|---|
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |

## Gate Evidence Links

- Launch scorecard JSON:
- Conformance JSON:
- Trust smoke report JSON:
- Trust negative matrix JSON:
- Alert test JSON:
- Phase gate summary JSON:
- Heartbeat JSON:

## Incident Review

- Open incidents:
- Closed incidents:
- Sev-1/Sev-2 count:
- Rollbacks triggered:
- Root-cause notes:

## Decision

- GO/NO_GO:
- Decision rationale:
- Follow-up actions (if any):

---

## Optional Machine-Readable Companion (`research/canary-week-report.json`)

```json
{
  "generated_at": "2026-03-25T00:00:00Z",
  "window_start": "2026-03-18T00:00:00Z",
  "window_end": "2026-03-25T00:00:00Z",
  "days_observed": 7,
  "go_nogo": "GO",
  "open_incidents": 0,
  "notes": [
    "All required gate signals remained green for 7 days"
  ]
}
```
