# Policy Ops Runbook v1 (Phase 2B)

## Lifecycle states
- draft
- tested
- shadow
- canary
- active
- retired

## APIs
- Create bundle: `POST /policy/bundles`
- List bundles: `GET /policy/bundles?bundle_id=<id>`
- Transition state: `POST /policy/bundles/{bundle_row_id}/transition`
- Replay diff: `POST /policy/replay-diff`
- Rollback active bundle: `POST /policy/bundles/{bundle_id}/rollback`

## Activation checklist
1. Candidate bundle transitions to `tested`
2. Run fixture suite (`scripts/policy_fixture_runner.py`)
3. Transition to `shadow`
4. Run replay diff against active baseline (`/policy/replay-diff`)
5. Transition to `canary`
6. If healthy, transition to `active` (`activate=true`)

## Rollback
One command:
```bash
BOTSTORE_API=http://127.0.0.1:8787 ./scripts/policy_bundle_rollback.sh <bundle_id>
```

## Demo artifacts
- `research/policy-ops-demo-result.json`
- `research/policy-ops-demo-report.md`
- `research/policy-fixture-report.json`
- `research/policy-fixture-report.md`
