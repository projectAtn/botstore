# BotStore Demand Scan v3 — 2026-03-14

## Scope & signal sources
- **Reddit:** r/ChatGPT, r/LocalLLaMA, r/artificial (top + search JSON threads, year window)
- **Hacker News:** AI/agent newest feed (`hnrss.org/newest?q=AI+agent`)
- **Product Hunt:** public feed (`producthunt.com/feed`)
- **Trend pages:** There’s An AI For That (new/trending tools), Exploding Topics AI trend brief

## Readout (what demand is clustering around)
1. **Agentic automation is shifting from "chat" to "do-work"** (coding, ops, research, inbox, monitoring).
2. **Trust/safety primitives are now first-order demand** (approval gates, idempotency, sandboxing, audit trails).
3. **Memory and personalization are becoming table stakes** for sticky assistants.
4. **Local/private deployment remains a durable pull** (esp. LocalLLaMA and self-hosted assistant threads).
5. **High-velocity launch channels (PH + HN) reward verticalized assistants** with clear ROI over general chatbots.

---

## Top 30 requested bot capabilities (ranked)

Confidence scale: **High / Medium / Low** based on cross-source recurrence + explicit request language.

| # | Capability | Why demand exists now | Confidence |
|---|---|---|---|
| 1 | **Autonomous coding task execution (repo-scale)** | Repeated demand in r/LocalLLaMA, r/artificial AMAs, HN Show HN for “delegate full tasks, not line edits.” | High |
| 2 | **Codebase understanding / repo wiki generation** | Strong pull for onboarding speed and architecture visibility in coding-agent launches. | High |
| 3 | **Multi-step workflow orchestration** | Users want chained actions across tools (research→write→publish; alert→diagnose→ticket). | High |
| 4 | **Long-term user memory with conflict resolution** | HN + Reddit discuss memory drift/contradiction; demand for durable, updateable memory lifecycle. | High |
| 5 | **Approval checkpoints for risky actions** | Safety concern spikes around autonomous side effects; desire for “human-in-the-loop” controls. | High |
| 6 | **Agent action audit trail / explainability logs** | Enterprise + builders want post-hoc “why did it do that?” traceability. | High |
| 7 | **Tool-use reliability / exactly-once execution** | Explicit demand from retry/duplicate side-effect pain (payments, emails, tickets). | High |
| 8 | **Secure command execution sandbox** | Strong concern around prompt injection and command abuse in self-hosted agent threads. | High |
| 9 | **Cross-app integrations (Slack/Notion/Jira/Email/Calendar)** | Persistent request pattern: assistant value rises when embedded in existing workflows. | High |
| 10 | **Inbox/news summarization with personalization** | PH + TAAFT show dense clustering in summary/news assistant products. | High |
| 11 | **Research copilot (web + source-cited synthesis)** | Frequent “find/summarize/compare” requests; users expect citations and concise briefs. | High |
| 12 | **Local-first / self-hosted assistant mode** | Strong demand in LocalLLaMA and security-conscious communities for private control. | High |
| 13 | **Model/provider routing for cost/latency/quality** | Users increasingly optimize spend/perf and want automatic model selection. | Medium |
| 14 | **Custom persona/tone modes (strict critic, coach, etc.)** | r/ChatGPT requests for calibration beyond default “friendly praise.” | High |
| 15 | **Voice input/output + meeting intelligence** | Cross-channel demand for hands-free interaction, transcription, action-item extraction. | Medium |
| 16 | **Agent-to-agent coordination primitives** | HN experimentation around leader/worker patterns and shared queues/state. | Medium |
| 17 | **RAG over personal/team knowledge bases** | Still a foundational ask: “use my docs/files, not generic web answers.” | High |
| 18 | **Browser automation with anti-fragile fallbacks** | Interest in real-world task completion despite brittle UIs and changing pages. | Medium |
| 19 | **Task planning + weekly execution (personal ops)** | Repeated requests for scheduling, reminders, and follow-through loops. | Medium |
| 20 | **Real-time monitoring + anomaly triage bots** | HN shows infra/network diagnostic agent launches; ops teams seek first-response automation. | Medium |
| 21 | **Payment/commerce-capable agents (guardrailed)** | Emerging but explicit ask: spend money safely on user’s behalf. | Medium |
| 22 | **Compliance/privacy policy enforcement layer** | Enterprise demand for policy checks before tool execution. | Medium |
| 23 | **Prompt-injection defense & data exfil prevention** | Security threads make this a blocking adoption criterion for agent deployment. | High |
| 24 | **Document AI (PDF/contracts/forms extraction + drafting)** | Ongoing practical demand in legal/commercial workflows. | Medium |
| 25 | **Content production bots (SEO/social/blog) with workflow hooks** | PH/TAAFT launches keep showing sustained creator/marketing demand. | Medium |
| 26 | **Customer support copilot + auto-resolution playbooks** | Strong ROI narrative in launch channels and SMB tooling. | Medium |
| 27 | **Sales prospecting + CRM update automation** | Persistent GTM productivity pull in AI tool launches. | Medium |
| 28 | **Multimodal generation/editing (image/video variants)** | Creator market still large; many trending tools are style and media generators. | Medium |
| 29 | **Evaluation/benchmark harness for agents** | Builder demand for measurable quality before production use. | Medium |
| 30 | **Deployment portability (cloud + edge + desktop)** | Users want same bot to run where data/compliance requires. | Low-Medium |

---

## Top 15 persona archetypes to prioritize

| # | Persona archetype | Jobs-to-be-done / rationale | Confidence |
|---|---|---|---|
| 1 | **Indie Developer / Solo Builder** | Wants autonomous coding, debugging, release help, and repo understanding. | High |
| 2 | **Startup CTO / Eng Lead** | Needs safe delegation, auditability, and team-wide AI workflow standardization. | High |
| 3 | **Security Engineer / AppSec Lead** | Demands sandboxing, policy gates, and injection-resistant agents. | High |
| 4 | **DevOps / SRE Operator** | Wants anomaly triage, runbook execution, and incident summarization. | Medium-High |
| 5 | **Knowledge Worker “Inbox Zero” Operator** | Needs email/news/calendar summarization and actionable daily briefs. | High |
| 6 | **Founder-Operator (non-technical)** | Wants one assistant for research, planning, and execution without heavy setup. | High |
| 7 | **Product Manager** | Needs synthesis across docs/feedback, spec drafting, and decision support. | Medium-High |
| 8 | **Marketing Generalist** | Requests campaign drafts, SEO outputs, and cross-channel content workflows. | Medium |
| 9 | **Sales Rep / RevOps** | Wants prospect research, personalized outreach drafts, and CRM automation. | Medium |
| 10 | **Customer Support Manager** | Needs ticket summarization, response drafting, and auto-triage confidence controls. | Medium |
| 11 | **Research Analyst** | Demands citation-grounded web synthesis and recurring topic monitoring. | High |
| 12 | **Privacy-Conscious Power User** | Strong preference for local/self-hosted assistants with explicit data boundaries. | High |
| 13 | **Student / Lifelong Learner** | Uses tutors, explainers, and study-plan agents; values adaptive tone + memory. | Medium |
| 14 | **Creator / Media Producer** | Seeks multimodal ideation, script generation, and rapid creative variants. | Medium |
| 15 | **Operations/EA-style Coordinator** | Needs scheduling, task follow-up, reminders, and stakeholder brief generation. | Medium |

---

## Strategic implications for BotStore

1. **Lead with “trusted autonomy,” not generic chat.**
   - Winning bot listings should show: approvals, logs, rollback/fallback, and safety posture.
2. **Package vertical bots with concrete workflows.**
   - “Coding finisher,” “Inbox/News analyst,” “Security guardrail bot,” etc.
3. **Support persona + tone calibration as a core primitive.**
   - Demand is explicit for customizable critique/coaching modes.
4. **Prioritize integrations + memory quality early.**
   - These are the strongest retention multipliers across channels.
5. **Create a trust badge rubric for marketplace quality.**
   - Example fields: sandboxed execution, idempotency, audit logs, data policy, local mode.

## Confidence notes & caveats
- Signals are strong on **directionality** (what people want), weaker on exact market sizing.
- Reddit source mix includes hype/noise; high-confidence items were promoted only when repeated across at least 2 source families (e.g., Reddit + HN, or PH + trend pages).
- Trend pages skew toward launch-heavy categories (news/content/media), which can overrepresent creator use cases vs enterprise ops.
