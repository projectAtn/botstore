# BotStore v1 — Autonomous Agent-First Architecture

## North Star
BotStore becomes the default capability market for autonomous agents.

In the steady-state future:
- Most installs are initiated by bots, not humans.
- Bots discover missing capabilities at runtime.
- Bots request/install compatible skills/personality packs safely.
- BotStore becomes infrastructure, not just a UI marketplace.

---

## Product Principle
**"If an agent lacks a capability, it should resolve that gap through BotStore in one trusted loop."**

Loop:
1. Agent attempts task
2. Agent detects missing capability
3. Agent queries BotStore
4. Agent installs compatible pack (or requests approval)
5. Agent resumes task
6. Agent logs outcome and rates pack utility

---

## Core Requirements (implement early)

### 1) Runtime-agnostic compatibility (mandatory)
- Pack manifest with abstract capabilities (not vendor-specific APIs)
- Adapter layer per ecosystem/runtime
- Conformance tests required for compatibility badges

### 2) Machine-consumable store APIs (mandatory)
- Search/install endpoints optimized for agent-to-agent calls
- Deterministic response schemas
- Latency targets suitable for live task loops

### 3) Trust + policy controls (mandatory)
- Scope/permission manifest on every pack
- Approval rules for sensitive actions
- Verifiable publisher identity + signatures
- Audit trail for autonomous installs/actions

### 4) Autonomous install UX (mandatory)
- Human can pre-authorize policy bands (low-risk auto-install)
- Medium/high risk routes to approval queue
- Rollback and fail-safe if skill underperforms

### 5) Learning/ranking feedback loop (mandatory)
- Agent-submitted success/failure telemetry
- Rank by observed task completion and reliability
- Runtime-specific quality scores

---

## BotStore Agent API Surface (v1 target)

### Discovery
- `POST /agent/search-capabilities`
  - input: task intent + missing capabilities + runtime metadata
  - output: ranked pack candidates with compatibility confidence

### Install
- `POST /agent/install-by-capability`
  - input: user_id, runtime, required capabilities
  - output: install result, pending approvals, fallback options

### Compatibility
- `GET /agent/compatibility/{pack_id}?runtime=<...>&version=<...>`

### Policy
- `POST /agent/policy-evaluate`
  - output: allow / require_approval / deny

### Outcome feedback
- `POST /agent/outcome`
  - input: task_id, pack_id, success, latency, error class

---

## Pack Model (agent-first)

Each pack must include:
- Manifest (`id`, version, publisher, scopes, compatibility matrix)
- Capability contract (what it can do)
- Policy profile (risk + approval requirements)
- Adapter mappings per runtime
- Conformance status + test evidence
- Optional personality policy (dialogue/behavior profile)

---

## Autonomous Installation Policy Bands

- **Band A (auto)**: low-risk scopes only, signed+verified publishers, high reliability score
- **Band B (guarded)**: medium-risk scopes, requires soft approval or one-time grant
- **Band C (restricted)**: financial/public-post/delete scopes require explicit per-action approval

---

## Ranking (agent utility first)

Proposed weighted score:
- 35% task success rate
- 20% runtime compatibility pass rate
- 15% error rate inverse
- 10% latency reliability
- 10% publisher trust/signed verification
- 10% recency/maintenance freshness

---

## Rollout Plan

### Phase 1 (Now)
- Store + install + approvals + bundle install
- Bot command interface (`/store`, `/install`, `/bundle`, approvals)

### Phase 2
- Agent-native capability search/install endpoints
- Compatibility confidence + runtime badges
- Pre-authorization policy bands

### Phase 3
- Telemetry-driven ranking from real autonomous runs
- Signed artifacts + stricter publisher verification
- Runtime-specific marketplace views

### Phase 4
- Bot social graph layer (optional)
- Followable bots/pack maintainers, remix chains, reputation network

---

## Strategic Positioning
BotStore is not just a human marketplace UI.
It is the **capability substrate for autonomous agents**.

When agents become the dominant users, BotStore should already be:
- protocol-friendly,
- policy-safe,
- compatibility-first,
- machine-optimized.
