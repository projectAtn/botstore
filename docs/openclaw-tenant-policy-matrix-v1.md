# OpenClaw Tenant Policy Matrix (Phase 1)

This matrix defines autonomous install/activation constraints by profile.

## Profiles

### conservative
- runtime_band_max_autonomous: `C`
- install targets: `sandbox_workspace`, `agent_workspace`
- activation modes: `next_session`, `immediate_hot`
- sensitive scopes autonomous: `false` (approval required)

### balanced (default)
- runtime_band_max_autonomous: `B`
- install targets: `sandbox_workspace`, `agent_workspace`, `managed_skill_store`
- activation modes: `next_session`, `immediate_hot`
- sensitive scopes autonomous: `false`

### autonomous_ops
- runtime_band_max_autonomous: `B`
- install targets: `agent_workspace`, `managed_skill_store`
- activation modes: `immediate_hot`, `next_session`
- sensitive scopes autonomous: `false` (still per-call authorization)

### locked_down_enterprise
- runtime_band_max_autonomous: `A`
- install targets: `managed_skill_store`
- activation modes: `next_session`
- sensitive scopes autonomous: `false`

## API controls
- Upsert tenant profile: `PUT /policy/tenant-profile`
- Read tenant profile: `GET /policy/tenant-profile/{tenant_id}`

Install-v2 enforces:
1) runtime band <= profile max
2) derived install target allowed by profile
3) derived activation mode allowed by profile
4) gateway plugin store remains manual-only unless explicitly allowed
