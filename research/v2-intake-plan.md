# V2 Intake Plan (Skills + Personalities)

This note documents the intake pipeline script and the expected report format for QA review.

## Script

- Path: `botstore/scripts/v2_intake_pipeline.py`
- Purpose:
  1. Merge v2 skill + personality candidate files
  2. Run existing quality gates:
     - `scripts/quality_check_candidates.py`
     - `scripts/runtime_simulation_verify.py`
  3. Emit pass/fail and delist recommendations in a summary report

## Default Inputs/Outputs

- Default input (skills): `botstore/research/candidate-skills-v2.json`
- Default input (personalities): `botstore/research/candidate-personalities-v2.json`
- Merged output: `botstore/research/candidate-packs-v2.json`
- Summary report: `botstore/research/v2-intake-summary.md`

The pipeline temporarily swaps `candidate-packs-v1.json` while running existing scripts, then restores it (unless `--in-place` is provided).

## Run Commands

### Standard (safe restore)

```bash
python3 botstore/scripts/v2_intake_pipeline.py
```

### Explicit paths

```bash
python3 botstore/scripts/v2_intake_pipeline.py \
  --skills botstore/research/candidate-skills-v2.json \
  --personalities botstore/research/candidate-personalities-v2.json \
  --merged-out botstore/research/candidate-packs-v2.json \
  --summary-out botstore/research/v2-intake-summary.md
```

### Keep merged file as active source for legacy scripts

```bash
python3 botstore/scripts/v2_intake_pipeline.py --in-place
```

## Input JSON Shape (accepted)

Each source can be either:

- a list of candidates, or
- an object containing one of: `candidates`, `skills`, `personalities`, `items`, `data`

Minimum expected candidate fields (aligned with existing quality checks):

- `slug`
- `title`
- `type` (`skill` or `personality`; auto-filled if missing)
- `problem`
- `includes` (list)
- `scopes` (list)
- `risk_level` (`low|medium|high`)
- `quality_tests` (list)

## Summary Report Template (produced)

`v2-intake-summary.md` sections:

1. **Merge**
   - merged file path
   - source counts
   - dedup/overwrite notes
   - warnings
2. **Existing checks**
   - quality script PASS/FAIL
   - runtime simulation PASS/FAIL
3. **Runtime simulation outcome**
   - verified count
   - delist recommendation count
   - table per candidate (`score`, `required_score`, `final_verified`, recommendation)
4. **Execution logs (trimmed)**
5. **Output artifacts**

## Delist Decision Rule

Delist recommendation is based on `runtime-simulation-result.json`:

- `final_verified = false` => **DELIST**
- `final_verified = true` => **KEEP**

This preserves existing risk gates (low/medium/high thresholds) from `runtime_simulation_verify.py`.
