# BotStore Operator Runbook v1

## Scope
Operational runbook for the current launch lock:
- Reference runtime: OpenClaw
- Autonomous packs: skill + personality
- Manual-only: gateway/native-plugin installs

## Daily checks
1. Run conformance:
```bash
cd /Users/claw/.openclaw/workspace/botstore
BOTSTORE_API=http://127.0.0.1:8787 ./scripts/openclaw_conformance.sh
```
2. Run trust checks:
```bash
BOTSTORE_API=http://127.0.0.1:8787 python3 ./scripts/trust_chain_smoke.py
BOTSTORE_API=http://127.0.0.1:8787 python3 ./scripts/trust_chain_negative_matrix.py
```
3. Run policy + runtime2 checks:
```bash
BOTSTORE_API=http://127.0.0.1:8787 python3 ./scripts/policy_fixture_runner.py
BOTSTORE_API=http://127.0.0.1:8787 python3 ./scripts/runtime2_certify_python_hostbot.py
```
4. Generate launch scorecard:
```bash
python3 ./scripts/launch_scorecard.py
```

## Incident response
- Scope mismatch incident: quarantine + rollback
  - check `TrustIncident`
  - run `/agent/rollback` receipt for affected attempt
- Policy regression:
  - run replay diff
  - rollback policy bundle in one command
- Approval latency spike:
  - inspect `/status/control-plane` latency section
  - inspect approval checkpoint backlog

## SLO watchlist
- quarantine_rate spike
- approval_latency_minutes_avg spike
- activation failures
- outcome ingestion failures
