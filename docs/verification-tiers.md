# Verification Tiers & Risk Gates

BotStore now enforces tiered verification with risk-aware minimum scores.

## Tier bands
- **Gold**: score >= 95
- **Silver**: score >= 85
- **Bronze**: score >= 75
- **Unverified**: < 75

## Risk-aware minimum score
- **low risk** packs: minimum 75
- **medium risk** packs: minimum 85
- **high risk** packs: minimum 95

A pack must pass both:
1) base verification (>=75) and
2) risk gate minimum for its risk level.

## Tooling
- Runtime verifier: `scripts/runtime_simulation_verify.py`
- Result file: `research/runtime-simulation-result.json`
- Delisting enforcement: `scripts/enforce_delist.py`

## Current run summary
- Candidates evaluated: 18
- Final verified: 16
- Delisted: 2 (`autonomous-worker-persona`, `enterprise-assistant-persona`)
