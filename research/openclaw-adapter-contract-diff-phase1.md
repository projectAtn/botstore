# OpenClaw Adapter Contract Diff (Phase 1)

## Previous state
Generic adapter interface supported:
- search
- install
- where

## New OpenClaw reference adapter additions
Implemented in `plugin/python/adapters/openclaw_adapter.py`:
- `resolve_gap(...)`
- `install_status(...)`
- `pre_action_authorize(...)`
- `report_outcome(...)`
- `action_scope_map(...)`

## Why this matters
These methods align runtime execution to the control-plane lifecycle:
- capability resolution uses InstallAttempt v2
- sensitive actions are authorized per-call
- outcomes are attempt-bound and trust-enforced

## Runtime metadata additions
- runtime_id
- runtime_version
- runtime_band
- optional runtime attestation hash

## Safety behavior added
- typed action/scope mapping for side-effecting actions
- no sensitive inference from raw shell text
- outcome pathway supports scope-mismatch quarantine handling from control plane

## Remaining contract work
- install target selection as explicit enum in adapter API
- activation mode as explicit enum in adapter API
- rollback receipt and deterministic rollback status handling
- explicit approval pause/resume checkpoint API
