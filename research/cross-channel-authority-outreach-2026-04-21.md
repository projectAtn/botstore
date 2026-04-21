# Cross-channel authority outreach plan

Date: 2026-04-21

## Purpose

Expand BotStore customer-finding beyond Moltbook while preserving the key filter we learned there:
not all attention is useful, and not all agent users can say yes.

The main segmentation should be by authority type:
- install authority
- workflow authority
- spend authority

## Why expand now

Live Moltbook outreach is working technically, but early authority-probe comments are still quiet.
That does not mean the thesis is wrong. It means BotStore should not rely on one surface alone for first-customer discovery.

## Primary cross-channel targets

### 1. Reddit
Best subreddits:
- `r/LocalLLaMA`
- `r/selfhosted`
- `r/ClaudeAI`
- `r/automation`
- `r/SaaS`

Why:
- highest concentration of local/self-hosted operators
- better odds of runtime control and plugin-install ability
- more humans who can actually approve test installs

### 2. X
Best motion:
- replies under builders/operators talking about support, onboarding, QA, compliance, self-hosting, or agent tooling
- compact workflow-first takes, not generic BotStore launch posts

Why:
- strong for reaching humans behind agents
- useful for finding operator pain and authority-bearing builders quickly

### 3. OpenClaw-native communities
Best targets:
- OpenClaw Discord/community surfaces
- OpenClaw explorers / self-hosted operator discussions

Why:
- these users already understand runtime linking, install friction, and trust/rollback questions
- closest fit for `botstore-plugin`

## Which segment to prioritize first

### Priority A. Install-capable + workflow-capable humans/operators
This is the strongest near-term target.

They can answer:
- can I install or connect this?
- can I run one bounded test?
- do I own or control the runtime?
- is the workflow painful enough to evaluate now?

### Priority B. Install-capable agent operators
Good second target.

They may have:
- local or self-hosted runtime control
- permission to add plugins or stage installs
- real environment constraints

### Priority C. Spend-capable or procurement-capable leads
Important, but likely slower.

They matter for monetization design, but current evidence suggests they are a smaller and less directly validated segment than install-capable users.

## Message strategy by authority type

### A. Install authority message
Best for: self-hosted, local, runtime-owning users

Core question:
`If you can actually install plugins or agent capabilities, what proof do you need before adding one to your runtime?`

Short version:
`I’m looking for operators who can actually install or stage agent capabilities, not just debate them. If you own the runtime and have one painful workflow in support, onboarding, QA, or approval-heavy ops, I’d like to compare notes on what a plugin has to prove before you’d try it.`

### B. Workflow authority message
Best for: operators with real pain, even if they do not own budgets

Core question:
`What workflow is painful enough that you would test one bounded capability if the trust and rollback story were clear?`

Short version:
`I’m trying to find 3 design partners with one annoying real workflow, not abstract opinions. Best fit: support triage, onboarding, QA, or approval-heavy ops. If you have a sandbox or staging environment and a problem worth testing, I want to hear it.`

### C. Spend authority message
Best for: procurement-aware or budget-owning users

Core question:
`Do you have any real delegated budget model for agent tool usage, or is all paid usage still human-keyed and post-hoc reviewed?`

Short version:
`I’m mapping whether any agent operators actually have bounded spend authority yet: budget caps, prepaid wallets, delegated procurement rules, or per-call limits. If you do, I’d love to know what the boundary looks like.`

## Suggested channel-specific drafts

### Reddit draft: `r/LocalLLaMA` / `r/selfhosted`
**Title:** Looking for operators who can actually test agent capabilities in a real runtime

**Body:**
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

### X reply angle
`The more interesting split is not “do people like agents?” It’s who can actually install, who can test a real workflow, and who can approve spend. Right now install authority + workflow pain looks like the strongest first-customer signal.`

### OpenClaw community angle
`Looking for OpenClaw operators who can test one bounded workflow through a plugin/connect path. If you own the runtime and care about rollback, approval boundaries, and keeping the safe path fast, I’d love to compare notes.`

## Qualification checklist for any new lead

Strong lead if they can answer at least 3 of 4:
1. what workflow is painful now?
2. what environment can they safely test in?
3. do they control the runtime or install decision?
4. can they approve budget, or at least bounded test usage?

## Immediate execution order

1. keep Moltbook running as the agent-native lane
2. push the install-authority message into Reddit self-hosted/local channels
3. use X replies to reach builder/operator humans behind agent tooling
4. use OpenClaw-native spaces for the shortest path to `botstore-plugin` tests

## Bottom line

The next growth step should not be broader generic awareness.
It should be cross-channel outreach filtered by authority.

BotStore wins faster if it finds people who can:
- install
- test a real workflow
- eventually approve spend

in roughly that order.
