# Bot Discovery Pack (v1)

BotStore now exposes machine-discovery endpoints so autonomous agents can find and integrate quickly.

## Endpoints
- `GET /.well-known/botstore.json`
  - canonical service discovery metadata
- `GET /agent/capabilities-manifest`
  - capability vocabulary + alias map + risk notes
- `GET /llms.txt`
  - LLM/agent-friendly concise integration guide

## Why this matters
- Lets autonomous agents discover BotStore without human onboarding.
- Improves interoperability across runtimes and toolchains.
- Creates a stable protocol layer for SEO-for-bots / discoverability optimization.

## Recommended integration flow for agents
1. Read `/.well-known/botstore.json`
2. Read `/agent/capabilities-manifest`
3. Query `/agent/search` or `/agent/search-capabilities`
4. Install via `/agent/install-by-capability`
5. Evaluate policy with `/agent/policy-evaluate`
6. Report outcomes to `/agent/outcome`
