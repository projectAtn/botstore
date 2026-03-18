# Hosting Phase 1 Execution (2026-03-18)

## Objective
Start migration away from local-Mac-only runtime by enabling containerized API + managed-DB-ready config + worker process.

## Implemented

1) **DB config externalization**
- Updated API engine bootstrap to use `DATABASE_URL` env var.
- Default remains SQLite (`sqlite:///./botstore.db`) for local fallback.
- SQLite path now sets `check_same_thread=False`; Postgres path supported via SQLAlchemy URL.

2) **Postgres driver support**
- Added `psycopg[binary]` to `api/requirements.txt`.

3) **Container image**
- Added `botstore/Dockerfile`:
  - installs API deps
  - copies api/scripts/research/web
  - runs `uvicorn app.main:app` on port 8787

4) **Compose stack**
- Added `botstore/docker-compose.yml` with:
  - `db` (Postgres 16)
  - `api` (BotStore API, uses `DATABASE_URL`)
  - `worker` (periodic QA/CI scheduler)

5) **Worker service loop**
- Added `scripts/worker_loop.py`:
  - mode `qa_scheduler` runs `ci_gate_run_all.py` on interval
  - interval configurable (`WORKER_INTERVAL_SECONDS`)

## How to run

From `botstore/`:

```bash
docker compose up --build
```

API: `http://localhost:8787`

## Next steps (Phase 1 remaining)

- Add `alembic` migration scaffolding for Postgres schema management.
- Add startup DB migration task in deployment pipeline.
- Add staging environment variables and secrets template.
- Add hosted artifact storage (S3/R2) for reports/manifests.

## Phase 1.5 progress (DB migration safety)

6) **Alembic scaffolding added**
- `api/alembic.ini`
- `api/alembic/env.py`
- `api/alembic/script.py.mako`
- `api/alembic/versions/20260318_000001_baseline.py`

7) **Migration runner scripts**
- `scripts/db_migrate.py` (runs `alembic upgrade head`)
- `scripts/start_api.sh` (runs migration step before API start)

8) **Container startup updated**
- Dockerfile now starts API via `scripts/start_api.sh` to include migration step.

9) **Environment template**
- Added `.env.example` for container/host configuration.
