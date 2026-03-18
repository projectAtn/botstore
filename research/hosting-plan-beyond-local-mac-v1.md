# Hosting Plan Beyond Local Mac (v1)

Date: 2026-03-18
Status: Practical migration plan

## Problem
Current setup can run on local Mac, but production reliability needs cloud hosting with managed storage, CI/CD, and secure runtime isolation.

---

## Target architecture

## Core services
1. **API service (BotStore API)**
   - Run in container platform (Fly.io/Render/Railway/Kubernetes).
2. **Database**
   - Move from local SQLite to managed Postgres.
3. **Object storage**
   - Store artifacts/reports/manifests in S3-compatible bucket.
4. **Worker service**
   - Async jobs: QA runs, adapter installs, telemetry processing.
5. **Gateway/ingress**
   - TLS termination, auth, rate limits.
6. **Observability**
   - Logs + metrics + alerting (Grafana/Datadog/Cloudwatch).

## Optional edge
- CDN for static marketplace web UI.

---

## Environment split

- **dev**: low-cost single region
- **staging**: production-like with synthetic traffic
- **prod**: HA setup, backup and failover policy

---

## Migration phases

## Phase 1 (1-2 weeks): "Cloud baseline"
- Containerize API + workers.
- Provision managed Postgres.
- Add migration path from SQLite snapshot.
- Deploy staging + prod skeleton.

## Phase 2 (2-3 weeks): "Reliability"
- Move artifacts to object storage.
- Add queue-backed workers for QA and publishing jobs.
- Add health checks, autoscaling, and alerts.

## Phase 3 (2-4 weeks): "Security + enterprise readiness"
- Secrets manager integration.
- SSO/RBAC for publisher/admin roles.
- Audit log exports and retention policy.

---

## Minimal production stack recommendation

If speed is priority:
- API/worker: Render or Fly.io
- DB: Neon or Supabase Postgres
- Storage: Cloudflare R2 or AWS S3
- CI/CD: GitHub Actions
- Monitoring: Grafana Cloud + uptime checks

If scale/enterprise is priority:
- Kubernetes (EKS/GKE)
- Managed Postgres (RDS/CloudSQL)
- S3
- Managed queue (SQS/PubSub)
- Datadog/New Relic

---

## Operational requirements

- Daily DB backup + point-in-time recovery
- Artifact retention policy
- Blue/green deploy or canary rollout
- Rollback command under 5 minutes
- Incident runbook + on-call rotation

---

## Security baseline

- TLS everywhere
- API key + service auth for adapters
- Least-privilege DB roles
- Signed manifest support (next step)
- Dependency scanning + image scanning in CI

---

## Cost model (starter)

Expected starter monthly range:
- API/worker hosting: $40–$200
- Managed Postgres: $25–$150
- Storage + egress: $5–$60
- Monitoring: $0–$100

Total starter range: **~$70–$510/month** depending on traffic and redundancy.

---

## Immediate next actions (this week)

1. Add Postgres support to BotStore API config.
2. Introduce DB migration tool (Alembic).
3. Write Dockerfile + compose for API + worker + db local parity.
4. Stand up staging deployment.
5. Move CI gate run-all into hosted CI pipeline with artifact upload.
