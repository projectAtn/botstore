# OpenClaw Reference Runtime Architecture (Phase 1)

## Scope lock
Autonomous GA scope is intentionally narrow:
- Runtime: OpenClaw reference adapter only
- Verticals: Ops / DevOps / SecOps
- Autonomous install scope:
  - skill packs
  - personality packs
- Excluded from autonomous GA:
  - gateway/native plugin code installs
  - social posting packs
  - payment/charge actions

## Control-plane split
- **BotStore control plane** owns:
  - retrieval + ranking
  - policy + approval grants
  - trust incidents + quarantine
  - promotion/delist
  - replay/shadow analytics
- **OpenClaw adapter** owns:
  - compatibility probe
  - install/activate/rollback execution
  - pre-action authorization enforcement
  - observed scope capture
  - outcome emission

## Install targets
1. `sandbox_workspace` (ephemeral)
2. `agent_workspace` (durable per-agent)
3. `managed_skill_store` (shared, policy-approved)
4. `gateway_plugin_store` (manual only in phase 1)

## Activation modes
- `immediate_hot`: skill-folder style packs only
- `next_session`: personality overlays (SOUL/AGENTS/IDENTITY effects)
- `gateway_restart`: excluded from autonomous GA

## End-to-end flow
1. OpenClaw tool `botstore_resolve_gap` called when blocked
2. Adapter calls `/agent/install-by-capability-v2`
3. BotStore returns selected digest-pinned pack version + policy decision
4. Adapter installs to approved target + activates with allowed mode
5. Before sensitive execution, adapter calls `/agent/action-authorize`
6. If approval is needed, adapter pauses lane via `/agent/approval-checkpoint/pause` and resumes via `/agent/approval-checkpoint/resume`
7. Adapter reports observed scopes + outcome to `/agent/outcome-v2`
8. On failure/quarantine, adapter emits `/agent/rollback` receipt
9. BotStore updates trust/learning state, including quarantine if needed

## Correlation keys
- `attempt_id` (primary join key)
- `task_id`
- `policy_decision_id`
- `grant_id`
- OpenClaw run/session IDs mapped into metadata for diagnostics joins

## Safety invariant
Sensitive actions must route through typed tool metadata and per-call authorization. Raw shell/browser paths are never trusted for sensitive scopes.
