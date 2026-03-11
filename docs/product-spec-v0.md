# BotStore v0 Product Spec

## Vision
A marketplace where users install either:
- **Personality packs** (tone, behavior, style)
- **Skill packs** (capabilities and integrations)
- **Bundles** (curated combinations)

## Core entities
- Creator
- Pack
- Permission manifest
- Install
- Approval event
- Review and telemetry

## Guardrails
- Sandboxed execution by default
- Explicit approval for external write actions
- Audit trail for sensitive actions

## Discovery
- Type filters (personality/skill/bundle)
- Compatibility badges
- Basic trust indicator

## Monetization
- Free listings
- Paid one-time packs
- Subscription packs

## 30-day build plan
- Week 1: Registry + install/rollback
- Week 2: Permission manifest + approvals
- Week 3: Ratings/ranking + creator profiles
- Week 4: Billing + polish + launch docs
