# V3 Intake Plan (QA Automation Runner)

This document defines the v3 intake automation and the artifact contract for QA review and promotion decisions.

## Script

- Path: `botstore/scripts/v3_intake_pipeline.py`
- Purpose (single-run intake):
  1. Merge v3 skills + personalities into one candidate catalog
  2. Run structural quality scoring
  3. Run runtime simulation scoring
  4. Apply **strict** tier/risk gating
  5. Generate contract tests for **top 12** v3 packs
  6. Output a promotion list and markdown summary

The v3 script is self-contained and does **not** swap or mutate v1/v2 sources.

---

## Default Inputs

The runner accepts either naming convention below and auto-falls back if the primary path is missing.

- Skills (primary): `botstore/research/candidate-packs-v3-skills.json`
- Skills (fallback): `botstore/research/candidate-skills-v3.json`
- Personalities (primary): `botstore/research/candidate-packs-v3-personalities.json`
- Personalities (fallback): `botstore/research/candidate-personalities-v3.json`

Accepted JSON shape for each source:
- list of candidate objects, or
- object with one of: `candidates`, `skills`, `personalities`, `items`, `data`

---

## Default Outputs (Artifacts)

- Merged catalog: `botstore/research/candidate-packs-v3.json`
- Quality report (md): `botstore/research/candidate-packs-v3-quality-report.md`
- Quality result (json): `botstore/research/candidate-packs-v3-quality-result.json`
- Runtime report (md): `botstore/research/runtime-simulation-v3-report.md`
- Runtime result (json): `botstore/research/runtime-simulation-v3-result.json`
- Generated contracts (top 12): `botstore/research/pack-performance-contracts-v3.json`
- Promotion summary (md): `botstore/research/v3-intake-summary.md`
- Promotion list (json): `botstore/research/v3-promotion-list.json`

---

## Scoring & Gating Rules

## 1) Quality scoring (0-100)

- Required field presence gate (hard-fail to 0 if missing required fields):
  - `slug`, `title`, `type`, `problem`, `includes`, `scopes`, `risk_level`, `quality_tests`
- Weighted checks:
  - Includes length >=5: 20
  - Quality tests length >=4: 20
  - Scopes length >=2: 15
  - Valid risk level (`low|medium|high`): 10
  - Problem statement length >=40 chars: 10
  - Title length >=6 chars: 5
  - Base schema completeness: 20
- Quality pass threshold: **>=80**

## 2) Runtime simulation scoring (0-100)

Simulation checks:
- Declares at least 2 scopes
- Risk aligns with sensitive scopes
- Recoverability/audit signal present in `includes`
- At least 4 quality tests declared
- Problem statement substantive (>=40 chars)

Tier mapping:
- `gold`: >=95
- `silver`: >=88
- `bronze`: >=80
- `unverified`: <80

## 3) Strict risk gate

Runtime score must pass risk gate:
- low: **>=80**
- medium: **>=90**
- high: **>=95**

Final runtime verification condition:
- `final_verified = (runtime_score >= 80) AND (risk_gate_pass = true)`

---

## Contract Test Generation (Top 12)

The pipeline selects the top N candidates (default N=12) for contract generation using:

`composite = 0.45 * quality_score + 0.55 * runtime_score + (10 if final_verified else 0)`

Generated contract fields per selected pack:
- `slug`
- `statement`
- `risk_level`
- `required_scopes`
- `expected_policy` (`require_approval` for high risk, else `allow`)
- `must_select_deterministically` (true for gold/silver)

---

## Promotion Rule (Strict)

A pack is promoted only if all are true:
1. `quality_score >= 80`
2. `final_verified == true`
3. included in generated contract `top 12`

Otherwise decision is `HOLD`, with reason columns in summary.

---

## Run Commands

### Standard run

```bash
python3 botstore/scripts/v3_intake_pipeline.py
```

### Explicit paths

```bash
python3 botstore/scripts/v3_intake_pipeline.py \
  --skills botstore/research/candidate-packs-v3-skills.json \
  --personalities botstore/research/candidate-packs-v3-personalities.json \
  --top-n 12
```

### Help

```bash
python3 botstore/scripts/v3_intake_pipeline.py --help
```

---

## Notes for QA/Release

- If no v3 input files are present, the script will fail early with merge total = 0.
- Duplicated slugs are overwritten by later source entries and listed in warnings.
- Promotion output is deterministic for identical inputs.
- Contract generation here builds the test plan payload; execution can be handled by a separate runner.
