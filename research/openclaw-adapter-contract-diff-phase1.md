# OpenClaw Adapter Contract Diff (Phase 1)

## Previous state
Generic adapter interface supported:
- search
- install
- where

## New OpenClaw reference adapter additions
Implemented in `plugin/python/adapters/openclaw_adapter.py`:
- `resolve_gap(...)` (with `install_target_preference`)
- `install_status(...)`
- `pre_action_authorize(...)`
- `pause_for_approval(...)`
- `resume_after_approval(...)`
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
- expose activation mode override/negotiation in adapter API surface
- install target policy profile enforcement matrix by tenant/runtime band
- approval UX channel adapters (inline buttons + text fallback parity)
