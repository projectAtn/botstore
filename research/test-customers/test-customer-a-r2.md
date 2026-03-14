# Test Customer A (Ops Manager) — Retest Round 2

**Need re-tested:** `triage inbox + schedule meetings + send followups`

## Round 2 check (after search/ranking updates + featured promotions)
- Re-ran:
  - `POST /agent/search` with `missing_capabilities=[email.read,email.send,calendar.read,calendar.write]` and `constraints.risk_max=medium`
  - `POST /agent/search-capabilities` with same required capabilities
  - `GET /packs` for pack metadata / featured flags
- Top matches remain strong and now consistently grouped at the top:
  1. `service-ops-verticals`
  2. `inbox-calendar-ops` *(featured)*
  3. `founder-command-bundle` *(featured)*
  4. `universal-connector-auth` (partial)

## Before vs After (concise)
- **Discoverability:** **Improved slightly** — exact-match packs are still top-tier, and ranking feels more stable across both endpoints.
- **Relevance:** **Slightly improved at the top, long-tail noise remains** — top 3 are excellent fits; lower ranks still include weakly related packs.
- **Risk fit:** **About the same (good)** — `risk_max=medium` behavior is correct; top options are medium-risk with approval for write/send scopes.
- **Ease:** **Improved slightly** — featured promotions make likely picks (`inbox-calendar-ops`, `founder-command-bundle`) easier to notice faster, but user still needs to compare similar candidates.

## Round 2 score (out of 5)
- **Discoverability:** 4.5/5  *(was 4.0)*
- **Relevance:** 4.0/5  *(was 3.5)*
- **Risk fit:** 3.5/5  *(was 3.5)*
- **Ease:** 3.5/5  *(was 3.0)*

## Bottom line
Updates moved this use case in the right direction: stronger top-of-list confidence and better visual/promotional guidance to likely installs. Main remaining gap is lower-rank relevance noise from non-canonical or weakly related capability labels.