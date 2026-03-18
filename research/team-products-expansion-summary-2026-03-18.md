# Team Products Expansion Summary (2026-03-18)

## What was added

### 1) More teams (expanded team catalog)
- New file: `team-packs-v3.json`
- Team count: **15**
- Includes executive, finance, GTM, community, support, revenue, security, devops, product, research, ecommerce, hiring, governance, and content teams.

### 2) Singular sub-agent offerings
- New file: `singular-role-agent-offerings-v1.json`
- Agent role offerings: **29**
- Each role is available as a standalone offering with:
  - role name
  - personality mapping
  - starter skills
  - suggested shared skills
  - source teams

### 3) Build custom team option (productized)
- Product spec: `custom-team-builder-v1.md`
- Working prototype script: `scripts/custom_team_builder.py`
- Example output: `custom-team-built-sample.json`

## QA scenarios and validation

- Scenario set: `team-pack-qa-scenarios-v2.json` (**20 scenarios**)
- QA runner: `scripts/team_pack_qa_flexible.py`
- Outputs:
  - `team-pack-qa-result-v2.json`
  - `team-pack-qa-report-v2.md`
  - `team-packs-v3-patched.json`

### Results
- Initial pass: **20/20**
- Patched pass: **20/20**
- Average score: **0.97**

## Notes
- Team QA validates capability/role/artifact coverage per scenario.
- Autofix path is available and generated a patched team set even though all scenarios already passed.

## API implementation (custom team builder endpoints)
Implemented in `api/app/main.py`:
- `POST /teams/custom/compose`
- `POST /teams/custom/validate`
- `POST /teams/custom/simulate`
- `POST /teams/custom/publish`

### Live smoke test
- Compose: success (`Custom Revenue Tiger Team`)
- Validate: pass (`score=0.8`)
- Simulate: ran 2 scenarios (`pass=1`, `avg_score=0.725`)
- Publish: created bundle pack `custom-revenue-tiger-team` (`pack_id=126`)
