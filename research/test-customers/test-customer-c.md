# Test Customer C (Creator/Marketer) — BotStore Search Evaluation

**Date:** 2026-03-14  
**Persona need:** content repurposing, SEO optimization, campaign orchestration  
**API tested:** `http://127.0.0.1:8787`

## What I tested

1. `GET /health` → API reachable (`ok: true`, version `0.2.0`)
2. `GET /catalog` → 42 total packs
3. `POST /agent/search` with query only:
   - `"content repurposing SEO optimization campaign orchestration"`
4. `POST /agent/search` with query + capabilities:
   - missing capabilities: `writing`, `seo`, `social.post`, `workflow`, `analytics`
5. `POST /agent/search-capabilities` with same capability list

## Key findings

### 1) Search discoverability for this marketing use case is weak
- Query-only search returned top 10 with **score 0.0 across all results**.
- `why` field showed **query term overlap: 0** for all returned packs.
- This means a creator/marketer typing natural language does not get clearly relevant packs.

### 2) Capability-based results are only partially relevant
Top results included:
- `approval-policy-brain` (matched `social.post`, but this is governance-focused and high-risk)
- `research-citation-packager` (matched `writing`, research-oriented)
- `job-application-accelerator` (matched `writing`, but wrong domain)

Missing or weak coverage for:
- explicit `seo`
- explicit `campaign orchestration`
- explicit `content repurposing`
- explicit `analytics`

### 3) Actionability is low from the result list alone
- Several surfaced packs are adjacent but not “ready-fit” for the stated goal.
- Highest-ranked option requires approval (`social.post` scope, high risk), adding friction before value is shown.
- No clear “marketing starter bundle” appears in top results for this intent.

## Friction points (from customer perspective)

1. **Natural-language mismatch:** My exact terms (content repurposing/SEO/campaign orchestration) don’t map to relevant results.
2. **Sparse domain taxonomy:** Catalog lacks obvious marketing/creator tags or scoped capabilities (`seo`, `campaign`, `repurpose`, `analytics`).
3. **Result ambiguity:** Top hits are technically related but not goal-specific, so next step (install what?) is unclear.

## 3 fixes

1. **Add marketing capability schema + synonyms**
   - Add canonical capabilities/tags like: `marketing.seo`, `marketing.content_repurpose`, `marketing.campaign_orchestration`, `marketing.analytics`.
   - Expand `SEARCH_SYNONYMS` with mapping for `seo`, `campaign`, `repurpose`, `creator`, `content strategy`, etc.

2. **Create and feature at least one Creator/Marketer pack bundle**
   - Example: **"Creator Growth Ops Bundle"** combining writing + scheduling + analytics + social publishing workflows.
   - Mark as featured so `/store` and search can quickly route this persona to a direct-fit option.

3. **Improve ranking transparency + intent-fit scoring**
   - Add an `intent_fit` or `% match` score based on domain tags and capability coverage.
   - Penalize off-domain matches (e.g., job application tools for marketing query) even if one generic capability overlaps.
   - Return “missing capabilities not covered” so user sees gaps immediately.

## Bottom line
For a creator/marketer, relevant packs are **not currently easy to find** via natural-language search, and top suggestions are only **partially actionable**. Catalog/tagging and ranking need marketing-specific improvements to make this journey high-conversion.