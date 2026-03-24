# Policy Ops Runbook v2 (Automatic Rollback)

## Controller
- Script: `scripts/policy_slo_controller.py`

## Inputs
- `/status/control-plane`
- `/policy/decision-log`
- policy bundle id

## Trigger classes
- quarantine spike
- deny-rate spike
- approval-latency spike
- activation-failure proxy spike
- forced trigger (demo/testing)

## Action
When any trigger fires (and not dry-run), controller executes:
- `POST /policy/bundles/{bundle_id}/rollback`

## Artifacts
- `research/policy-slo-controller-report.json`
- `research/policy-slo-controller-report.md`
- `research/canary-rollback-demo-result.json`
- `research/canary-rollback-demo-report.md`

## Demo
```bash
cd /Users/claw/.openclaw/workspace/botstore
BOTSTORE_API=http://127.0.0.1:8787 python3 ./scripts/policy_canary_rollback_demo.py
```

## Operational notes
- Keep conservative thresholds in pilot mode.
- Never skip replay diff + fixture checks for policy activation.
- Rollback path must remain one command/API call with no manual DB edits.
