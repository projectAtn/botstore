# BotStore (MVP)

App store for bot personalities + skills.

## Scope (v0)
- Publish/list packs (`personality`, `skill`, `bundle`)
- Install packs to a user
- Roll back installed packs
- Basic catalog filtering by type

## Quick start (API)
```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8787
```

Then open: `http://localhost:8787/docs`

## Next milestones
1. Permission manifests + approval engine
2. Verified creators and trust score
3. Ratings + ranking
4. Billing + revenue split
5. Web UI
