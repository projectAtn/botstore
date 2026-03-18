# Custom Team Builder v1

## Goal
Allow users to build a custom multi-agent team by choosing roles, personalities, and skills, then validate before publish.

## UX Flow
1. Pick objective (e.g., Launch, Incident, Hiring, Research).
2. Pick 2-8 roles from role-agent catalog.
3. Auto-suggest personality + starter skills per role.
4. Add shared skills used by multiple roles.
5. Run validation (capability gaps, role gaps, risk mismatch, redundancy).
6. Simulate on selected QA scenario(s).
7. Publish team pack draft or save private template.

## API Draft
- `POST /teams/custom/compose`
- `POST /teams/custom/validate`
- `POST /teams/custom/simulate`
- `POST /teams/custom/publish`

## Guardrails
- Require at least one orchestration role (Chief of Staff/COO equivalent).
- Require governance role for medium/high risk teams.
- Block publish on validation errors.
- Warn on duplicate-problem role composition and skill redundancy.

## Success Metrics
- Build completion rate
- Validation pass rate
- Scenario pass rate
- Time-to-first-usable-team
