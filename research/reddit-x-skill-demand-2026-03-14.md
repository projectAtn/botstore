# Reddit/X-driven Skill Demand Scan (2026-03-14)

## Scope
User requested trend scan from Reddit + X for new useful BotStore skills/personas.

## Data reality
- Reddit JSON/top feeds were accessible.
- X public search is heavily login-gated from this runtime, so X signal is partial.
- We used visible Reddit demand patterns + broader public agent trend context.

## Practical demand patterns observed
Even with noisy social feeds, recurring demand themes are clear:

1. **Reliability under autonomy**
   - Bots that recover from errors, retries, and connector breakage.
2. **Safety/governance**
   - Approval gates, compliance checks, auditable actions.
3. **Cost control**
   - Budget-aware model/runtime routing.
4. **Trust and verification**
   - Source-backed outputs and media authenticity checks.
5. **Task execution maturity**
   - Better planning, decomposition, and completion validation.

## Candidate packs designed
- 12 skills + 6 personalities were specified in:
  - `research/candidate-packs-v1.json`

## Quality test process
We created and ran a quality gate:
- Script: `scripts/quality_check_candidates.py`
- Report: `research/candidate-packs-quality-report.md`
- Result: **18/18 PASS** (score >= 75)

## Marketplace action completed
All vetted candidates were added as separate catalog products via seed import flow.
Current catalog count after reseed: **32** packs.

## Notes
- We intentionally kept these as separate products (no new bundles), per user request.
- Next upgrade should introduce behavioral test harnesses (runtime simulation) beyond static rubric checks.
