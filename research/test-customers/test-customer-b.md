# Test Customer B (Security Lead) — BotStore Search Evaluation

**Need tested:** `compliance guard, audit logs, policy enforcement for risky actions`  
**API:** `http://127.0.0.1:8787` (`POST /agent/search`, `GET /catalog`)  
**Run date:** 2026-03-14

## 1) Top search results observed
Using:
- `query`: compliance guard, audit logs, policy enforcement for risky actions
- `missing_capabilities`: `audit.log.read`, `audit.log.write`, `policy.enforce`, `risk.evaluate`
- `limit`: 10

Top 5 returned:
1. `policy-sop-generator` (score 0.1745, medium risk, no approval)
2. `synthetic-media-checker` (0.1318, low risk)
3. `web-action-proof-logger` (0.1318, low risk)
4. `policy-compliance-guard` (0.0955, high risk, approval required)
5. `model-switchboard` (0.0909, low risk)

## 2) Trustworthiness assessment
### What looks good
- Top results are mostly from **verified creator** `Ops Foundry` with trust score **0.89**.
- High-risk pack (`policy-compliance-guard`) is correctly marked `requires_approval=true`, which is good for governance-sensitive installs.

### Concerns (for a Security Lead)
- **Capability mismatch:** none of the requested capabilities (`audit.log.read`, `audit.log.write`, `policy.enforce`, `risk.evaluate`) exist in current catalog scope taxonomy, so ranking relies mostly on text overlap and generic risk/type biases.
- **Potential false positives:** packs like `synthetic-media-checker` and `model-switchboard` rank highly without strong compliance/audit capability evidence.
- **Trust signal underused in ranking:** creator verification/trust appears in catalog metadata but does not materially shape ranking score.

## 3) Determinism assessment
- Re-ran identical `/agent/search` payload **5 times**.
- Top-5 order was identical in all runs.
- **Conclusion:** deterministic for current dataset and execution path.
- **Caveat:** equal-score ties (e.g., many 0.05 results) could become unstable without a secondary sort key.

## 4) Feedback
For this security use case, results are **partially trustworthy operationally** (verified source, approval flags) but **not semantically precise** (requested governance capabilities are missing from taxonomy and scoring). Current ranking is deterministic but not sufficiently intent-faithful for compliance-critical discovery.

## 5) Three ranking improvements
1. **Capability ontology + alias mapping for governance terms**
   - Add canonical capabilities such as `audit.log.read`, `audit.log.write`, `policy.enforce`, `risk.evaluate`, `approval.workflow`.
   - Map query aliases (`audit logs`, `policy guard`, `risky actions`) to these canonical capabilities.
   - Strongly prioritize exact/alias capability matches over text overlap.

2. **Trust-aware scoring with security floor rules**
   - Incorporate creator trust/verification directly into ranking (e.g., multiplier/bonus).
   - For compliance intents, apply floor rules: penalize or filter unverified/low-trust creators unless no alternatives.
   - Surface provenance explainers in `why` (e.g., `verified creator`, `trust=0.89`).

3. **Deterministic multi-key sort and security intent reranker**
   - After score, use stable tie-breakers: `requires_approval (true first for risky-action intents)`, `creator_verification`, `creator_trust_score`, then `pack_id`.
   - Add an intent-specific reranker for security/compliance queries that boosts packs with governance/action-control semantics and de-emphasizes unrelated low-risk utilities.

## Quick verdict
- **Deterministic?** Yes (in repeated test).
- **Trustworthy for security procurement?** Moderate at best today; metadata is promising, but relevance/ontology needs strengthening for compliance-grade discovery.
