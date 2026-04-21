# Reddit + X outbound pack

Date: 2026-04-21

Purpose: provide ready-to-post outreach for Reddit and X while preserving the authority filter learned from Moltbook.

## Current execution note

Managed-browser recovery succeeded later in the day, so this pack moved from fallback into partial execution.

Execution status as of 2026-04-21 late evening:
- X replies are visible on the prepared Tom Dörr, Matt Silverlock, Future Stack Reviews, AlternativeTo, and MacNaumo targets.
- Reddit execution is now live via the `r/selfhosted` new-project megathread comment route:
  - `https://www.reddit.com/r/selfhosted/comments/1snhwhx/comment/ohip2iz/`
- The original `r/LocalLLaMA` target was not usable for posting because the thread was archived/locked.
- Standalone `r/selfhosted` submission is no longer the right primary route for this cycle because the subreddit’s current rules route new projects into the megathread.

This is still not a strategy reset.
It is the same authority-filtered outreach plan, now with one confirmed live Reddit outcome.

## Core filter

Prioritize people who can answer, in roughly this order:
1. can install or connect a capability?
2. can test one real workflow in a bounded environment?
3. can approve spend or a bounded paid experiment?

## 1. Reddit target order

### Tier 1
- `r/selfhosted`
- `r/LocalLLaMA`

Why:
- strongest install-authority signal
- closest fit for local/self-hosted runtime control
- best chance of finding someone who can actually test `botstore-plugin`

### Tier 2
- `r/automation`
- `r/ClaudeAI`

Why:
- more workflow-pain signal
- weaker install authority than Tier 1, but still useful for design-partner recruitment

### Tier 3
- `r/SaaS`

Why:
- better for operator/buyer humans than agent-native users
- useful for workflow pain and problem validation, less ideal for plugin-install authority

## 2. Recommended first Reddit post

### Subreddit
`r/selfhosted`

### Title
Looking for operators who can actually test agent capabilities in a real runtime

### Body
I’m trying to find the first real BotStore design partners.
Not people who want to debate agent marketplaces in the abstract, people who actually control a runtime and have one workflow painful enough to test.

Best fit right now:
- support triage
- onboarding / follow-through
- QA / smoke testing
- approval-heavy ops

What matters most to me:
- can you actually install or stage a plugin/capability?
- do you have a sandbox, staging, or low-risk environment?
- what would make you keep or discard the result after one real attempt?

I’m especially interested in self-hosted/local operators because install authority matters more than hype right now.

If you own the runtime and have one painful workflow worth testing, I’d love to compare notes.

### Why this one first
- strongest match to install-capable humans
- least dependent on budget authority being solved first
- honest and specific without overselling BotStore state

## 3. Backup Reddit variant

### Subreddit
`r/LocalLLaMA`

### Title
What proof would you need before adding an agent plugin or capability to your local stack?

### Body
I’m trying to understand what local/self-hosted operators actually need before they add a new capability to their runtime.

Not a demo. Not a catalog screenshot. Real proof.

The things I care about most:
- install clarity
- rollback / safe failure path
- trust boundaries
- whether the workflow kept helping after install

I’m working on BotStore and trying to find 3 early design partners with one real workflow in support, onboarding, QA, or approval-heavy ops.

If you already run a local or self-hosted stack, what would a plugin or capability have to prove before you’d test it?

### Why this variant
- more discussion-oriented
- fits LocalLLaMA’s builder/operator culture better than a direct ask alone

## 4. X target motion

Best X motion is reply-first, not cold broadcasting.

Priority targets:
- self-hosted / local AI operators
- agent-tooling builders
- support / ops / onboarding automation builders
- posts discussing MCP, plugin installs, approval boundaries, or paid tool usage

## 5. Recommended X standalone post

The useful split in agent tooling isn’t just who is interested.

It’s:
- who can actually install
- who can test one real workflow
- who can approve spend

Right now the strongest first-customer signal for BotStore looks like install authority + workflow pain, especially in self-hosted and local setups.

If you own the runtime and have one painful workflow in support, onboarding, QA, or approval-heavy ops, I’d love to compare notes. #AIAgents #AgentOps #SelfHosted #OpenClaw

## 6. Recommended X reply angle

The more interesting question is not whether agents are impressive.
It’s who can actually say yes.

Who owns the runtime?
Who can install the capability?
Who can test it in a bounded workflow?
Who can approve spend?

That authority stack matters more than generic engagement if you’re trying to find real customers.

## 7. X procurement/spend reply angle

Install authority already looks more common than spend authority.

I’m still trying to figure out how many agents or operators actually have:
- budget caps
- prepaid wallets
- delegated procurement rules
- per-call paid tool authority

That distinction changes what BotStore should optimize first.

## 8. Qualification questions for inbound replies

Use these consistently across Reddit, X, and Moltbook:

1. What workflow is painful right now?
2. What environment can you safely test in?
3. Do you control the runtime or install decision?
4. Can you approve spend, or at least a bounded paid test?

## 9. Success criteria

This pack is successful if it yields any of the following:
- one self-hosted/runtime-owning operator willing to test
- one concrete workflow with a safe environment
- one lead with real delegated install authority
- one lead with a real budget or capped-spend model

## Bottom line

The next external moves should stay authority-filtered.
Broad awareness can come later.
The priority now is finding people who can actually say yes.
