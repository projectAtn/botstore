# Test Customer B (Security Lead) — Retest Round 2

**Need re-tested:** `compliance guard, audit logs, policy enforcement for risky actions`  
**API:** `http://127.0.0.1:8787` (`POST /agent/search`, `GET /catalog`)  
**Run date:** 2026-03-14

## Round 2 rerun (same need)
Request used:
- `query`: `compliance guard, audit logs, policy enforcement for risky actions`
- `missing_capabilities`: `audit.log.read`, `audit.log.write`, `policy.enforce`, `risk.evaluate`
- `limit`: `10`
- plus required API fields: `user_id`, `runtime`

Top 5 returned (stable across 5/5 identical runs):
1. `policy-compliance-guard` (id 19, score 0.8473, **high risk**, approval required)
2. `multi-agent-orchestrator` (id 13, 0.5448, medium risk, approval required)
3. `service-ops-verticals` (id 14, 0.4914, medium risk, approval required)
4. `human-escalation-router` (id 22, 0.4914, medium risk, approval required)
5. `approval-policy-brain` (id 9, 0.4621, **high risk**, approval required)

Notable: compliance/policy-oriented packs are now dominating the top, versus generic/non-governance utilities in round 1.

## Before vs After summary

### What changed positively
- **Relevance improved materially at the top**: previously top slots included weak matches (e.g., synthetic media checker / model switchboard). Now top-1 is the most directly aligned pack (`policy-compliance-guard`), and policy/approval semantics are strongly represented.
- **Trust posture appears stronger in surfaced candidates**: top results are mostly verified creator (`Ops Foundry`, trust 0.89), and risky-action packs are consistently `requires_approval=true`.
- **Determinism remains strong**: repeated identical payload returned identical top-10 ordering across all 5 runs.

### Remaining gaps
- Requested canonical capabilities (`audit.log.read`, `audit.log.write`, `policy.enforce`, `risk.evaluate`) still are not clearly expressed as first-class catalog scopes in many returned packs; relevance likely still mixes semantic/text signals with broader policy terms.
- Some top-ranked items are governance-adjacent rather than audit-log-specific.

## Scorecard (out of 5)

| Metric | Before (Round 1) | After (Round 2) | Delta |
|---|---:|---:|---:|
| **Trust** | 3.2/5 | **4.2/5** | +1.0 |
| **Determinism** | 4.5/5 | **5.0/5** | +0.5 |
| **Relevance** | 2.6/5 | **4.1/5** | +1.5 |

## Bottom line
For this Security Lead use case, round 2 is a clear improvement: ranking now prioritizes policy/compliance-oriented packs with appropriate approval gating, while keeping deterministic behavior. It is not yet perfect for strict audit-log capability matching, but it is much closer to procurement-grade discovery than round 1.