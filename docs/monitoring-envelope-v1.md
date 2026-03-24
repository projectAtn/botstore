# Monitoring Envelope v1

## Objective
Ensure launch-blocking failures become visible within minutes and no silent trust/auth/quarantine path remains.

## Required signals
1. Trust verify failures
2. Install admission denials
3. Action-authorize latency
4. Approval wait time
5. Activation failures
6. Quarantine events
7. Outcome-v2 completeness
8. Auth-bypass sentinel
9. Typed-map completeness

## Correlation IDs required in reports/logs
- `attempt_id`
- `decision_id`
- `grant_id`
- `checkpoint_id`
- `run_id`
- `session_key`
- `session_id`

## Alert thresholds (initial)
- trust verify failure count > 0 in last 15m => CRITICAL
- install admission denial rate > 0.40 in last 30m => WARN/CRITICAL (context dependent)
- action-authorize p95 > 0.2s => WARN
- approval latency avg > 10m => WARN
- quarantine_rate > 0.30 => CRITICAL
- outcome-v2 completeness < 0.95 => CRITICAL
- auth-bypass sentinel fail => CRITICAL
- typed-map completeness fail => CRITICAL
