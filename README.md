# BotStore (MVP)

App store for bot personalities + skills.

## Scope (v0)
- Publish/list packs (`personality`, `skill`, `bundle`)
- Creator profiles with verification + trust score
- Permission scopes per pack
- Risk-aware install flow with approval queue
- Roll back installed packs
- Catalog filtering by type

## Quick start (API)
```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8787
```

Then open: `http://localhost:8787/docs`

## Standards + SDK (new)
- `standards/botpack.schema.json` — portable BotPack manifest schema
- `standards/compatibility-matrix.schema.json` — cross-runtime test result schema
- `standards/conformance-spec.md` — required validation and policy tests
- `sdk/python/botpack_adapter.py` — Python adapter contract example
- `sdk/typescript/adapter.ts` — TypeScript adapter contract example
- `research/top-demand-skills-personalities-2026-03.md` — demand-oriented pack ranking

## Bot-environment endpoints
- `GET /bot/store?user_id=<id>` — list store catalog for bot surfaces
- `POST /bot/install` with `{ user_id, pack_slug }`
- `POST /bot/install-bundle` with `{ user_id, bundle_slug }`
- `GET /bot/installs?user_id=<id>`
- `GET /bot/approvals?user_id=<id>&pending_only=true`
- `POST /targets/bind` to link user -> runtime/agent install target
- `GET /targets?user_id=<id>` list linked targets
- `GET /where?user_id=<id>` shows install + activation location/status
- `GET /bot/open-store-link?user_id=<id>` → returns `/?user_id=<id>` URL for direct webview opening
- `POST /bot/command` with `{ user_id, text }` for `/store`, `/install`, `/bundle`, `/approvals`, `/approve`, `/reject`, `/installs`, `/link`, `/where`, and conversational text search
- `POST /bot/callback` with `{ user_id, callback_data }` for button callbacks (`install:slug`, `bundle:slug`, `approve:id`, `reject:id`, `open:url`)
- Optional endpoint auth: set `BOTSTORE_BOT_KEY` env var and send `X-Botstore-Key` header on `/bot/*`
- See `docs/bot-commands.md` for Telegram-ready mapping details
- Run `integrations/telegram_bridge.py` (or `integrations/run_telegram_bridge.sh`) for direct Telegram chat integration (see `docs/telegram-bridge.md`)
- Integrate into existing bots with plugin adapter: `plugin/python/botstore_plugin.py` (see `docs/botstore-plugin.md`)
- Adapter PoC roadmap (CopilotKit/Activepieces/E2B): `docs/plugin-adapters-roadmap-v1.md`
- GitHub integration scoring shortlist: `research/github-integration-matrix-v1.md`

## Agent-native endpoints (autonomous mode)
- `POST /agent/search-capabilities`
- `POST /agent/search`
- `POST /agent/install-by-capability` (legacy)
- `POST /agent/install-by-capability-v2` (attempt transaction + digest pinning + install target/activation mode)
- `POST /agent/action-authorize` (action-time authorization)
- `POST /agent/approval-checkpoint/pause` + `POST /agent/approval-checkpoint/resume`
- `POST /agent/rollback` (deterministic rollback receipt)
- `POST /agent/policy-evaluate`
- `POST /policy/bps/evaluate` (BotStore Policy Spec DSL evaluation)
- `POST /policy/bundles` + `GET /policy/bundles` (versioned policy bundle registry)
- `GET /policy/decision-log` (explainable decision export)
- `POST /agent/outcome` (legacy)
- `POST /agent/outcome-v2` (attempt-bound outcomes + trust incidents/quarantine)
- `GET /agent/compatibility/{pack_id}?runtime=<name>&version=<opt>`
- `GET /status/control-plane` (north-star/safety/latency/exploration KPI snapshot)
- `GET /analytics/shadow-ranker-eval` (shadow reranker hook metrics)
- `GET /analytics/replay-dataset` (candidate-level logged replay rows for offline evaluation)
- `POST /packs/{pack_id}/versions` + `GET /packs/{pack_id}/versions` (capability/scope/action separated manifests)
- Discovery endpoints: `GET /.well-known/botstore.json`, `GET /agent/capabilities-manifest`, `GET /llms.txt`
- Bot discovery pack notes: `docs/bot-discovery-pack.md`
- Autonomous-agent vision + architecture: `docs/botstore-v1-autonomous-agents.md`
- Pack spec draft: `docs/pack-spec-v1.md`
- Adapter contract draft: `docs/adapter-contract-v1.md`
- OpenClaw reference architecture: `docs/openclaw-reference-architecture-v1.md`
- OpenClaw tool/scope/action mapping: `docs/openclaw-tool-scope-action-mapping-v1.md`
- Content system starter: `docs/content-strategy-v1.md`
- Candidate pack quality gate: `research/candidate-packs-v1.json` + `scripts/quality_check_candidates.py` + `research/candidate-packs-quality-report.md`
- Runtime simulation + tier gate: `scripts/runtime_simulation_verify.py` + `research/runtime-simulation-report.md` + `research/runtime-simulation-result.json`
- Auto delist enforcement: `scripts/enforce_delist.py`
- Hazard-based reverify scheduling: `scripts/reverify_scheduler.py`
- End-to-end control-plane smoke test: `scripts/control_plane_smoke.sh`
- OpenClaw adapter smoke test: `scripts/openclaw_adapter_smoke.sh`
- Verification policy: `docs/verification-tiers.md`
- Pack test runner: `scripts/pack_test_runner.py` + `research/pack-test-report.md` + `research/pack-test-result.json`
- Statement-based contract runner: `research/pack-performance-contracts.json` + `scripts/contract_task_runner.py` + `research/contract-task-report.md` + `research/contract-task-result.json`
- Reddit/X demand scan notes: `research/reddit-x-skill-demand-2026-03-14.md`
- Bot leadership operating model: `docs/bot-ceo-operating-system.md`
- 90-day GTM execution scorecard: `docs/gtm-90-day-operator-scorecard.md`
- Community launch kit (Reddit + X): `docs/community-launch-kit.md`
- Control-plane migration report: `research/control-plane-migration-report-2026-03-20.md`
- OpenClaw adapter contract diff (phase 1): `research/openclaw-adapter-contract-diff-phase1.md`
- OpenClaw phase-1 risk register: `research/openclaw-phase1-risk-register.md`

## Next milestones
1. Add auth + publisher namespaces
2. Ratings/ranking with anti-fraud signals
3. Billing + revenue split
4. Signed pack artifacts + verification in install flow
5. Conformance runner CLI producing compatibility matrix JSON
