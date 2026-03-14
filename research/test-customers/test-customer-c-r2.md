# Test Customer C (Creator/Marketer) — Retest Round 2

**Date:** 2026-03-14  
**Persona need:** content repurposing, SEO optimization, campaign orchestration  
**API tested:** `http://127.0.0.1:8787`  
**Change context:** after marketing/security featured promotions + synonym upgrades

## Retest payloads (same intent)

1. `GET /health` → `ok: true`, version `0.2.0`
2. `GET /catalog` → **49 packs** (was 42)
3. `POST /agent/search`
   - `query`: `"content repurposing SEO optimization campaign orchestration"`
4. `POST /agent/search`
   - same query + `missing_capabilities`: `writing`, `seo`, `social.post`, `workflow`, `analytics`
5. `POST /agent/search-capabilities`
   - same missing capabilities

---

## Before vs After (key outcomes)

| Area | Round 1 (Before) | Round 2 (After) | Delta |
|---|---|---|---|
| Catalog size | 42 packs | 49 packs | **+7 packs** |
| Query-only top-10 scores | all **0.0** | non-zero, top score **0.1862** | **Improved retrieval** |
| Query-only term overlap | all **0** | top result overlap **2** (`ad-creative-feedback-loop`) | **Synonym/text matching improved** |
| Marketing-flavored result in #1 | No | Yes (`ad-creative-feedback-loop`) | **Improved intent relevance** |
| Query+capabilities top result | Governance/security-heavy | Still governance/security-heavy (`policy-drift-detector`, `approval-policy-brain`) | **No meaningful change** |
| Explicit `seo` coverage in top capability matches | Missing | Still missing | **Unresolved** |
| Explicit `content repurposing` capability | Missing | Still missing | **Unresolved** |
| Explicit `campaign orchestration` capability | Missing | Still missing (closest: `growth-experiment-orchestrator`, weak coverage) | **Mostly unresolved** |

---

## What improved

1. **Natural language discoverability is no longer dead-on-arrival**
   - Previously: all 0.0 scores and 0 overlap.
   - Now: query-only search surfaces at least one clearly marketing-adjacent pack first:
     - `ad-creative-feedback-loop` (score `0.1862`, overlap `2`)

2. **Featured promotions appear to have taken effect in catalog composition**
   - Featured list now includes marketing/security items such as:
     - `growth-experiment-orchestrator`
     - `ad-creative-feedback-loop`
     - `policy-drift-detector`
     - `secret-leak-preventer`

## What still hurts conversion for Creator/Marketer

1. **Capability matching still over-prioritizes governance/security for this need**
   - Query+capabilities top results remain:
     - `policy-drift-detector` (high risk, approval)
     - `approval-policy-brain` (high risk, approval)
   - These are not first-best tools for creator growth workflows.

2. **Taxonomy gap remains for core marketing capabilities**
   - No direct capability hits for `seo`, `content repurposing`, `campaign orchestration`.
   - Generic `writing` matches still drag in off-domain results (`job-application-accelerator`).

3. **Actionability remains mixed**
   - Highest-ranked capability matches still include approval friction and domain mismatch.
   - User still has to infer which packs to combine to achieve end-to-end campaign workflow.

---

## Scorecard (Bot C perspective)

Scale: **1 (poor) → 10 (excellent)**

| Dimension | Before | After | Notes |
|---|---:|---:|---|
| Natural-language relevance | 2/10 | **5/10** | Improved from zero-match to some intent capture |
| Capability-fit to creator/marketer goal | 3/10 | **4/10** | Slight bump, still missing core marketing capabilities |
| First-result actionability | 3/10 | **5/10** | Better in query-only path; weak in query+capability path |
| Approval/risk friction | 4/10 | **4/10** | No clear improvement |
| Overall conversion likelihood | 3/10 | **5/10** | Better discoverability, still not “install with confidence” |

**Overall:** meaningful improvement in top-of-funnel discovery, but mid-funnel decision friction remains high due to capability taxonomy/ranking gaps.

---

## Remaining friction (priority order)

1. **Add canonical marketing capabilities + synonyms**
   - `marketing.seo`
   - `marketing.content_repurpose`
   - `marketing.campaign_orchestration`
   - `marketing.analytics`

2. **Reweight ranking when intent is marketing/creator**
   - Penalize governance/security packs unless explicitly requested.
   - Boost packs with marketing domain tags and campaign outcomes.

3. **Ship a direct-fit featured bundle for this persona**
   - Example: **Creator Growth Ops Bundle** (repurpose + SEO + scheduling + social publish + analytics).
   - Ensure it appears in top 3 for this exact query family.

4. **Expose gap clarity in response**
   - Return `covered_capabilities` + `missing_capabilities` per result so users can decide faster.

## Bottom line

Round 2 is **better than Round 1** for discoverability (zero-match issue improved), but the system is still not consistently routing creator/marketer users to a clear, low-friction, goal-complete solution.