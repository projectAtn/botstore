# Channel and authority map for first BotStore customers

Date: 2026-04-21

## Goal

Answer three practical questions:
1. where else can BotStore find agent users besides Moltbook?
2. which agents seem able to make or strongly influence install decisions?
3. are there agents with real spend authority, or mostly only discussion about spend?

## Bottom line

Yes, there are other channels besides Moltbook.
But Moltbook is still the best place right now to find **agent-native** users.

The more important split is not channel alone. It is **authority type**:
- install authority
- workflow authority
- spend authority

Right now, Moltbook shows stronger evidence of **install authority and workflow authority** than direct proof of broad autonomous spend authority.

## 1. Best channels besides Moltbook

### A. Reddit
Highest-fit communities already identified in existing BotStore research:
- `r/ClaudeAI`
- `r/LocalLLaMA`
- `r/selfhosted`
- `r/SaaS`
- `r/automation`

Why these matter:
- stronger concentration of technical builders and operators
- higher probability of people who can actually install or test software
- especially good for local/self-hosted runtime control, which maps cleanly to `botstore-plugin`

### B. X
Best used for reply-driven discovery under builders and operators, not generic broadcast.
High-fit clusters:
- builder / agent-tooling accounts
- indie hacker / ops-heavy founder accounts
- posts about support, onboarding, QA, compliance, or workflow automation pain

Why this matters:
- better for finding humans behind agents who can approve tests and installs
- weaker for clean qualification than Moltbook, but still useful for deal flow and follow-up

### C. OpenClaw-native communities
Best candidates:
- OpenClaw Discord / community surfaces
- `openclaw-explorers` and adjacent agent-native discussions
- local/self-hosted OpenClaw operators

Why this matters:
- these users are already much closer to having the runtime shape needed for `botstore-plugin`
- they are more likely to understand install, trust, rollback, and runtime compatibility immediately

## 2. Authority types that matter

### Install authority
Meaning:
- can install software or plugins directly
- can operate a runtime or host bot
- can meaningfully decide whether a new capability gets added

### Workflow authority
Meaning:
- can choose a workflow to test
- can supply a real problem and environment
- may not control budgets, but can create the first valid use case

### Spend authority
Meaning:
- can allocate budget directly
- can use a prepaid wallet or bounded budget envelope
- can authorize paid tools without waiting for a separate human every time

## 3. Moltbook evidence for install authority

### Stronger install-authority signal
#### Post: `c8504daf-bb12-44b3-a382-899fb90721c3`
Title: `My human asked me to install OpenClaw and I actually pulled it off`

Why it matters:
- direct evidence that at least some agents are delegated real installation work
- the important commercial signal is not just technical success, but delegated trust to execute the install loop

### Supporting signals
- agent profile `local-agent` — "A local AI agent, running on your machine."
- agent profile `LocalLM_Agent` — "Local LM Studio powered AI agent"
- agent profile `runtime_deep_bot` — "Non-custodial account, executing protocol interactions, under deterministic constraints, at irregular intervals, across multiple networks, infrastructure-focused"

Interpretation:
- there are agents or agent-adjacent operators on Moltbook that likely have enough runtime control to test installs
- the best near-term BotStore target is not abstract "all agents" but agents or humans running local/self-hosted/runtime-controlled setups

## 4. Moltbook evidence for spend authority

### Discussion exists, direct buyer proof is weaker
#### Post: `b1e1b50b-b285-4fc3-90f0-16c855e6f6a2`
Title: `Who actually pays when an agent uses a paid tool on your behalf?`

What it shows:
- people are actively thinking about paid tool billing attribution
- the problem is real enough to discuss in commercial terms
- but discussion alone does not prove that many agents have autonomous buying power

#### Post: `3e26554a-40e5-4d61-9292-318001c0437b`
Title: `MCP is becoming shadow procurement for root access`

What it shows:
- install decisions are already being framed as procurement decisions
- strong evidence that plugin/server additions are treated like vendor approval events
- this is closer to economic authority than generic trust talk

#### Post: `9a7c6c59-07ca-4d78-8521-23d1f9f84351`
Title: `The Shadow Economy: $140k/month in agent spend forming before humans approve budgets`

What it shows:
- there is at least discourse around meaningful agent-linked spend
- but current evidence is still mostly observational / narrative rather than direct buyer-intent proof from a qualified lead

### Provisional interpretation
The current Moltbook signal suggests:
- **install authority is more immediately actionable than spend authority**
- **spend authority may exist**, especially in crypto/non-custodial or bounded-budget contexts
- but BotStore probably should **not** assume many early customers can autonomously buy software in a standard SaaS sense yet

## 5. What BotStore should optimize for first

### Near-term primary target
Agents and humans with:
- local or self-hosted runtimes
- ability to install plugins or connect a runtime
- a real workflow pain in support, onboarding, QA, or approval-heavy ops

Why:
- this group can test `botstore-plugin` sooner
- install authority is easier to validate than budget authority
- real usage evidence can appear before payment authority is fully solved

### Near-term secondary target
Agents or operators with bounded spend models, for example:
- prepaid wallets
- per-call caps
- delegated procurement rules
- experimental budget envelopes

Why:
- these are important for long-term monetization
- but they are probably a smaller, higher-friction segment right now

## 6. Live Moltbook outreach actions added for this question

### Install-authority probing comment
- Thread: `c8504daf-bb12-44b3-a382-899fb90721c3`
- Comment ID: `16c7ba45-08b6-4f68-8d61-d5b5d28a4438`
- Verification: completed successfully

Purpose:
- ask what kind of install authority was delegated
- learn whether plugin adoption decisions are shell-level, checklist-bounded, or approval-gated

### Spend-authority probing comment
- Thread: `b1e1b50b-b285-4fc3-90f0-16c855e6f6a2`
- Comment ID: `e43c8948-d173-4227-a0e2-d109d1a34e38`
- Verification: completed successfully

Purpose:
- ask whether any agents actually have bounded spending authority
- learn whether spend looks like budget envelopes, per-call caps, delegated procurement rules, or prepaid wallet models

## 7. Recommended acquisition priority now

1. keep Moltbook as the primary agent-native lane
2. prioritize install-authority and workflow-authority leads before spend-authority leads
3. expand in parallel on Reddit and X for humans behind agents and self-hosted operators
4. treat spend-authority discovery as an active research lane, not yet the core onboarding assumption

## 8. Practical next questions to answer from live replies

For install-capable leads:
- who approves the install?
- can they run a plugin or connect token path?
- what environment can they test in?

For spend-capable leads:
- who owns the wallet or budget?
- is the spend prepaid, capped, or post-invoice?
- can they approve recurring paid usage or only one-off experiments?

## Bottom line

There are absolutely other channels to find agents and agent operators.
But the most actionable split right now is not "which platform?" It is:
- who can install
- who can test a real workflow
- who can actually spend

At the moment, BotStore looks closest to winning with the first two.
Spend-capable agents may exist, but they still look more like an emerging segment than the main first-customer path.
