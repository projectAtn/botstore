# BotStore Plugin Adapters Roadmap (v1)

## Objective
Make BotStore easy to embed into existing bot ecosystems without channel lock-in.

## PoC adapters added
- `plugin/python/adapters/copilotkit_adapter.py`
- `plugin/python/adapters/activepieces_adapter.py`
- `plugin/python/adapters/e2b_adapter.py`
- `plugin/python/adapters/openclaw_adapter.py` (reference runtime adapter)

Each adapter supports a common core flow:
1) search packs
2) install pack
3) check where installed/activated

## Why these three first
- **CopilotKit**: app-native assistant UX patterns.
- **Activepieces**: action/trigger workflow + connector ecosystem ideas.
- **E2B**: sandbox-oriented verification and safer rollout model.

## PoC success criteria
- Can perform search -> install -> where for a namespaced user id.
- Handles approval-required installs gracefully.
- Returns structured data usable by host framework actions.

## Next milestone (v1.1)
- Add a unified adapter interface package + tests.
- Add dry-run mode (no-op install) for sandbox adapters.
- Add telemetry hooks for adapter-level conversion/latency.
