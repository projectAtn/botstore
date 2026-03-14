# Test Customer A (Ops Manager): BotStore evaluation

**Need tested:** `triage inbox + schedule meetings + send followups`

## What I tested
- `POST /agent/search` with query text + required capabilities (`email.read`, `email.send`, `calendar.read`, `calendar.write`), risk constraint `<= medium`
- `POST /agent/search-capabilities` with same capabilities
- Cross-checked candidate details via `GET /packs`

## Top results returned
1. **Inbox & Calendar Operator** (`inbox-calendar-ops`) — exact capability match, medium risk, approval required
2. **Service Ops Vertical Starter** (`service-ops-verticals`) — exact match + extra file scopes, medium risk, approval required
3. **Founder Command Bundle** (`founder-command-bundle`) — exact match + web scopes, medium risk, approval required
4. **Universal Connector Auth** — partial match only (missing `email.send` + `calendar.write`)

## Evaluation
- **Discoverability: Good (4/5)**
  - Search surfaced strong matches at the top for both semantic and capability queries.
  - Query parsing found relevant terms (`inbox`, `triage`, `schedule`, `meeting`).

- **Relevance: Good with some noise (3.5/5)**
  - Top 3 are genuinely relevant.
  - Lower-ranked items include weakly related packs (e.g., generic calendar/inbox packs with non-standard capability labels), which adds noise.

- **Risk fit: Reasonable but frictiony (3.5/5)**
  - Correctly keeps high-risk packs out when `risk_max=medium` is set.
  - Best matches are medium-risk and require approval, which is appropriate for email send/calendar write but may slow common ops workflows.

- **Ease: Fair (3/5)**
  - API is straightforward for developer use.
  - For an ops manager persona, there is no single obvious “one-click workflow pack” label for this exact job; requires comparing similar candidates.

## 3 improvement suggestions
1. **Normalize capability taxonomy and enforce canonical scopes**
   - Reduce noise from packs using broad tags like `email`/`calendar` instead of actionable scopes like `email.send`.
2. **Add intent presets (Ops templates) in search**
   - Example preset: “Inbox triage + meeting scheduling + follow-ups” that pre-fills capabilities and ranks by workflow completeness.
3. **Show decision-critical metadata in results by default**
   - Include approval requirement, scope delta (exact vs extra permissions), and estimated setup effort to make faster, safer install choices.

## Bottom line
BotStore can find good packs for this ops need, but selection quality and speed would improve with stricter capability normalization and clearer workflow-oriented ranking/presentation.