# BotStore Demand Snapshot v4 — 2026-03-14

## Scope (fresh public signals)
Collected on 2026-03-14 from:
- **Hacker News (Algolia API):** `query=agent`, last ~45 days (100 stories sampled)
- **Reddit JSON search:** r/ChatGPT, r/LocalLLaMA, r/artificial (top/relevance, month+year windows)
- **GitHub Search API:** repos pushed in last 30 days for `agent`, `mcp server`, `self-hosted assistant`
- **TAAFT homepage snapshot:** visible tool headings (lightweight trend check)

Raw files:
- `/Users/claw/.openclaw/workspace/botstore/research/demand-scan-v4-raw.json`
- `/Users/claw/.openclaw/workspace/botstore/research/demand-scan-v4-targeted-reddit.json`
- `/Users/claw/.openclaw/workspace/botstore/research/demand-scan-v4-github.json`

---

## Executive readout
Demand is still concentrating around **agentic execution** (especially coding + workflows), but the “must-have” layer has shifted to **trust controls** (security, approval, exactly-once side effects), **tool interoperability** (MCP), and **local/self-hosted privacy**.

If BotStore wants high-conversion packs, the strongest angle is:
> **“Do real work safely with verifiable controls,”** not generic chat wrappers.

---

## Demand clusters → candidate pack concepts

Confidence score = 0–100, based on recurrence across source families + explicitness of user pain/request language.

| # | Demand cluster | Public signal snapshot | Candidate pack concept | Confidence |
|---|---|---|---|---:|
| 1 | **Coding agents that complete multi-step tasks** | HN + Reddit + GitHub all saturated with coding-agent posts/tools; strong engagement around “actual agent, not demo.” | **Code Finisher Pack**: repo planning, PR drafting, test-loop, rollback-aware execution | **92** |
| 2 | **Guardrails for unsafe agent actions** | Recurrent “prompt injection is terrifying,” shell/tool safety failures, whitelisting posts on HN. | **Agent Safety Guard Pack**: command allowlist, policy gates, risky-action approvals, side-effect journaling | **90** |
| 3 | **MCP/tool ecosystem integration demand** | GitHub: `awesome-mcp-servers`, `playwright-mcp`, `github-mcp-server` among top-starred active repos; HN posts on tool gateways. | **MCP Connector Pack**: plug-and-play connectors + schema validation + fallback routing | **89** |
| 4 | **Self-hosted / local-first assistants** | LocalLLaMA threads + GitHub self-hosted assistant repos (Tabby, etc.) show durable privacy/control pull. | **PrivateOps Pack**: local model profiles, offline mode, data-boundary presets, local RAG quickstart | **87** |
| 5 | **Memory users can control (not opaque memory)** | Targeted Reddit signal: feature requests for multiple memory spaces, memory visibility and toggles. | **Memory Vault Pack**: scoped memories (project/persona), inspect/edit/delete flows, memory diffing | **84** |
| 6 | **Reliable workflow automation (beyond “chat answers”)** | Repeated mentions of automation workflows + frustrations with brittle tool-calling. | **Workflow Autopilot Pack**: trigger→plan→act pipelines, retries with idempotency keys, human checkpoint nodes | **83** |
| 7 | **Observability + evaluation for agents in production** | HN/GitHub/Reddit show evaluation, harness, benchmark, and feedback-loop interest. | **Agent Telemetry Pack**: traces, run scoring, failure taxonomy, regression checks | **80** |
| 8 | **Research/reporting agents with citations** | Ongoing demand for research task performance and synthesis quality in community discussions. | **Research Analyst Pack**: source crawl, citation-first summaries, compare/contrast briefs | **77** |
| 9 | **Voice + multimodal interaction for practical workflows** | LocalLLaMA engagement on voice embeddings/TTS + HN multimodal/browser tool experiments. | **Multimodal Operator Pack**: voice input/output + browser/canvas task macros | **73** |
| 10 | **Agentic commerce and payment-safe execution** | HN posts around agent payments/commerce exist but volume smaller than coding/security demand. | **Commerce Agent Pack**: spend limits, merchant allowlists, pre-transaction approval + receipts | **68** |
| 11 | **Content/SEO automation with workflow hooks** | Still visible in launch channels but weaker signal intensity vs core infra/coding demand. | **Content Engine Pack**: brief→outline→draft→repurpose pipeline with review gates | **64** |
| 12 | **Multi-agent orchestration frameworks** | Frequent experimentation posts (“OS for agents”, multi-agent systems), but production demand less explicit. | **Swarm Orchestrator Pack**: planner/worker patterns, shared memory bus, arbitration rules | **62** |

---

## Evidence highlights (sampled)

### 1) Coding + execution
- HN: “Free Coding Agent”, “Intake API — inbox for AI coding agents”, “Kube-pilot — AI engineer in your cluster”
- Reddit (LocalLLaMA): high-engagement threads on agentic coding model comparisons and real-world runs
- GitHub: very high-star active repos around Langflow, Dify, LangChain, Opencode

### 2) Safety + trust
- Reddit (ChatGPT): high-engagement prompt-injection concern threads
- HN: “whitelisting AI agent terminal commands”, “exactly-once execution guard”, security frameworks for agents
- Pattern: users now ask “can it do work safely?” before “can it do work?”

### 3) MCP + integrations
- GitHub: explosive momentum in MCP server ecosystem (`awesome-mcp-servers`, `playwright-mcp`, `github-mcp-server`, `fastmcp`)
- HN: tool gateway/server access posts for agents
- Pattern: integration breadth is becoming a purchase criterion

### 4) Self-hosted/local
- LocalLLaMA continues to favor local/open deployments and practical local agent setups
- GitHub “self-hosted assistant” results show sustained active maintenance

### 5) Memory controls
- Targeted Reddit queries surfaced explicit asks for memory visibility and profile separation
- Pattern: memory is demanded, but only with user-governable boundaries

---

## Prioritization recommendation (next pack batch)

Ship in this order for best demand fit:
1. **Code Finisher Pack**
2. **Agent Safety Guard Pack**
3. **MCP Connector Pack**
4. **PrivateOps Pack**
5. **Memory Vault Pack**

Why: these five clusters combine the highest confidence and strongest cross-source recurrence, while also creating a coherent “trusted autonomy” product line.

---

## Caveats
- Social sources are noisy and can over-amplify hype; confidence scores reflect **directional demand**, not TAM.
- Product Hunt feed parsing returned no AI-specific items in this scrape window (likely feed-format variance), so PH signal is underweighted in v4.
- Reddit engagement weights can bias toward controversy; cluster confidence was adjusted by cross-source confirmation (HN + GitHub + Reddit where possible).