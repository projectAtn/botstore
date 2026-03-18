# Reddit + X + GitHub Skill Demand Scan (2026-03-18)

## What was scanned
- Reddit (public JSON endpoints): r/LocalLLaMA, r/ChatGPT, r/ClaudeAI, r/OpenAI (query-based sampling for agent/automation/workflow/personality topics).
- GitHub (public API + curated repos): topic-based repository search (`ai-agent`, `workflow-automation`, `telegram-bot`) plus curated catalogs (`awesome-openclaw-agents`, `awesome-openclaw-usecases-zh`, `awesome-claude-skills`).
- X: attempted direct hashtag scraping (`#aiagents`, `#openclaw`, `#buildinpublic`) and public mirror access from this runtime; direct structured extraction was limited from this environment, so X signal was inferred via cross-posted GitHub/open-source ecosystem artifacts.

## Demand themes found (high-level)
- Community ops automation (Telegram/Discord/WhatsApp support triage, moderation, growth loops)
- GitHub-native workflows (issue radar, PR risk review, release watchers)
- Market intelligence from social chatter (painpoint mining, trend clustering, competitor deltas)
- Content production pipelines (transcript -> clips, SEO briefs, ad variants, short-form factory)
- Knowledge reliability (citation verification, RAG maintenance, source-grounded notes)
- Self-hosted reliability and security (incident triage, rollback guardians, secret rotation, health checks)
- Business automation (CRM sync, churn/renewal intelligence, proposal and contract support)

## Built output in this run
- Skills defined: **50**
- Personalities defined: **12**
- Merged candidate pack: `research/candidate-packs-v2.json`
- Intake verification: `research/v2-intake-summary.md` (quality PASS, runtime PASS)

## 50 skills to build (prioritized by category)

### Market Intelligence
- **Reddit Scout Pro** (`reddit-scout-pro`): Continuously discover user pain points and buying intent from selected subreddits without manual scrolling.
- **X Trend Harvester** (`x-trend-harvester`): Track fast-moving X hashtag conversations and convert noisy posts into actionable demand signals for builders.
- **GitHub Issue Radar** (`github-issue-radar`): Find high-signal unresolved issues in target repositories and surface recurring product pain themes.
- **Open-Source Repo Scout** (`opensource-repo-scout`): Identify fast-growing open-source agent ecosystems and extract integration opportunities for new skills.
- **Tool Release Watcher** (`tool-release-watcher`): Detect upstream API and SDK releases early so integrations stay compatible and useful.
- **Prompt Market Researcher** (`prompt-market-researcher`): Turn scattered prompt discussions into structured demand hypotheses for product decisions.
- **Competitor Feature Tracker** (`competitor-feature-tracker`): Monitor competitor launches and summarize strategic implications before they impact positioning.
- **User Painpoint Clusterer** (`user-painpoint-clusterer`): Cluster hundreds of user complaints into prioritized problem buckets that can be converted into build backlog.
- **Persona Signal Miner** (`persona-signal-miner`): Infer desired assistant personalities from community language patterns and workflow context.
- **Launch Feedback Summarizer** (`launch-feedback-summarizer`): Summarize multi-channel launch feedback quickly so teams can react during the critical first 48 hours.

### Growth & Community
- **Waitlist Converter** (`waitlist-converter`): Convert passive waitlist signups into active conversations and qualified prospects automatically.
- **Telegram Community Manager** (`telegram-community-manager`): Moderate and grow Telegram communities while preserving useful discussion quality.
- **Discord Community Manager** (`discord-community-manager`): Keep Discord servers healthy by triaging support posts, routing bugs, and maintaining response SLAs.
- **WhatsApp Support Copilot** (`whatsapp-support-copilot`): Handle repetitive support chats with consistent answers and smooth handoff for sensitive cases.
- **Email Outreach Sequencer** (`email-outreach-sequencer`): Run multi-step outreach campaigns with personalization while avoiding spammy repetitive messaging.
- **Lead Enrichment Finder** (`lead-enrichment-finder`): Enrich sparse lead records with public context so outreach is specific and relevant.
- **Sales Call Prep Kit** (`sales-call-prep-kit`): Generate concise pre-call briefs that improve close probability without manual research work.
- **Proposal Generator** (`proposal-generator`): Create client-ready proposals quickly with reusable structure and risk-conscious assumptions.

### Business Ops
- **Calendar Ops Coordinator** (`calendar-ops-coordinator`): Automatically coordinate meetings across time zones and reduce scheduling friction.
- **CRM Sync Bidirectional** (`crm-sync-bidirectional`): Prevent lead and customer data drift by syncing updates between communication channels and CRM state.
- **Contract Risk Highlighter** (`contract-risk-highlighter`): Spot risky legal clauses early so negotiations focus on real exposure, not guesswork.
- **Onboarding Journey Optimizer** (`onboarding-journey-optimizer`): Improve user activation by detecting friction points in onboarding flows and suggesting targeted fixes.
- **Churn Early Warning** (`churn-early-warning`): Detect likely churn signals before cancellation to trigger timely retention actions.
- **Renewal Expansion Coach** (`renewal-expansion-coach`): Prepare renewal and expansion opportunities using usage signals and stakeholder context.
- **Invoice Reconciliation** (`invoice-reconciliation`): Match invoices, receipts, and payments automatically to reduce bookkeeping errors.
- **Expense Policy Auditor** (`expense-policy-auditor`): Flag out-of-policy expenses with clear rationale and review-ready evidence trails.

### Knowledge & Content
- **Knowledge Base Curator** (`knowledge-base-curator`): Keep internal knowledge bases current by pruning stale pages and promoting high-value updates.
- **RAG Index Maintainer** (`rag-index-maintainer`): Maintain retrieval quality by continuously refreshing indexes and removing noisy documents.
- **Citation Verifier** (`citation-verifier`): Prevent unsupported claims by checking references before final output is published.
- **Paper to Notes** (`paper-to-notes`): Convert research papers into concise decision-ready notes with preserved methodological context.
- **Transcript to Action Items** (`transcript-to-action-items`): Transform raw meeting transcripts into accountable tasks, deadlines, and owners.
- **Podcast to Clips** (`podcast-to-clips`): Identify clip-worthy moments in long audio and package them for social distribution.
- **Shortform Content Factory** (`shortform-content-factory`): Repurpose long-form material into platform-specific short posts at high throughput.
- **Thumbnail Brief Generator** (`thumbnail-brief-generator`): Generate high-converting thumbnail concepts with hooks, contrast plans, and text overlays.
- **SEO Brief Builder** (`seo-brief-builder`): Create SEO briefs that align search intent, structure, and conversion goals in one pass.
- **Keyword Cluster Mapper** (`keyword-cluster-mapper`): Cluster large keyword lists into content hubs that can be directly assigned to production.
- **Ad Creative Variant Lab** (`ad-creative-variant-lab`): Generate and score ad copy variants quickly so teams can test ideas weekly, not quarterly.
- **Landing Page A/B Orchestrator** (`landing-page-ab-orchestrator`): Coordinate A/B tests end-to-end and keep result interpretation consistent across stakeholders.

### E-commerce & Revenue
- **E-commerce Listing Optimizer** (`ecommerce-listing-optimizer`): Optimize product titles, bullets, and descriptions for conversion across multiple marketplaces.
- **Price Change Sentinel** (`price-change-sentinel`): Track competitor price moves and trigger response playbooks before margin erosion compounds.
- **Inventory Demand Forecaster** (`inventory-demand-forecaster`): Forecast short-term demand to reduce stockouts and overstock risk during promotions.

### DevOps & Security
- **Incident Triage Commander** (`incident-triage-commander`): Cut incident response time by classifying alerts and routing the right owner immediately.
- **Deploy Rollback Guardian** (`deploy-rollback-guardian`): Protect release quality by monitoring deployments and triggering rollback playbooks when needed.
- **Log Anomaly Sleuth** (`log-anomaly-sleuth`): Find high-impact anomalies in noisy logs before they become production incidents.
- **Cloud Cost Analyzer** (`cloud-cost-analyzer`): Continuously surface wasteful cloud spend with practical optimization actions and confidence levels.
- **Security Alert Triager** (`security-alert-triager`): Prioritize security findings by exploitability and business impact so teams fix what matters first.
- **Secret Rotation Reminder** (`secret-rotation-reminder`): Prevent credential drift by tracking secret age and enforcing rotation reminders before expiry.
- **Backup Drill Coordinator** (`backup-drill-coordinator`): Run repeatable backup-restore drills so teams can trust recovery claims during real incidents.
- **Self-Host Healthcheck** (`self-host-healthcheck`): Monitor self-hosted services for reliability, security posture, and maintenance debt.

## Personality pack (12)
- **Conversion Closer** (`conversion-closer-persona`): Teams need persuasive but ethical conversion-focused communication that still respects user trust and consent boundaries.
- **Empathetic Support Ally** (`empathetic-support-ally-persona`): Support channels need warm, patient communication that resolves issues quickly without sounding robotic or dismissive.
- **Grumpy but Accurate SRE** (`grumpy-sre-persona`): Incident communication should be brutally clear on risk and action items, even under pressure and uncertainty.
- **Forensic Analyst** (`forensic-analyst-persona`): Security and failure analysis require evidence-driven communication that avoids speculation and preserves chain-of-custody logic.
- **Growth Hacker Operator** (`growth-hacker-persona`): Early-stage teams need rapid experiment-first thinking that still documents what worked and what failed.
- **Calm Chief of Staff** (`calm-chief-of-staff-persona`): Leadership communication needs organized, low-drama synthesis that aligns teams on priorities and dependencies.
- **Playful Creator** (`playful-creator-persona`): Creative workflows benefit from energetic brainstorming while still delivering concrete outputs and deadlines.
- **Strict Compliance Officer** (`strict-compliance-officer-persona`): Regulated teams need formal, policy-aligned language that blocks risky shortcuts and records approvals clearly.
- **Local-First Privacy Guardian** (`local-first-privacy-guardian-persona`): Privacy-sensitive workflows require strong bias toward local processing and minimal data sharing by default.
- **Product Strategist** (`product-strategist-persona`): Product teams need strategic framing that connects user pain, market context, and roadmap tradeoffs coherently.
- **Community Hype Manager** (`community-hype-manager-persona`): Community growth requires high-energy communication that drives engagement without becoming spammy or manipulative.
- **Research Librarian** (`research-librarian-persona`): Knowledge-heavy tasks need methodical citation behavior and careful uncertainty statements for trustable outputs.

## Notes
- Candidate definitions include scopes, risk level, and quality tests for automated intake checks.
- Medium-risk candidates include audit/escalation language so they pass runtime risk gating with current simulation rules.
- Next build step: scaffold executable SKILL.md directories for top 10 and ship in batches of 5-10 with live user testing.
