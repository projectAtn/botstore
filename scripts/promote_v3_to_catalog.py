#!/usr/bin/env python3
import json
from pathlib import Path

from sqlmodel import Session, select

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "api"))
from app.main import Pack, PackType, Creator, engine  # noqa

RESEARCH = ROOT / "research"
PROMO = RESEARCH / "v3-promotion-list.json"
CANDIDATES = RESEARCH / "candidate-packs-v3.json"


def main() -> int:
    if not PROMO.exists() or not CANDIDATES.exists():
        print("Missing v3 promotion/candidate files")
        return 1

    promo = json.loads(PROMO.read_text())
    promoted = set(promo.get("promoted_slugs", []))
    if not promoted and isinstance(promo.get("promoted"), list):
        promoted = {p.get("slug") for p in promo.get("promoted", []) if isinstance(p, dict) and p.get("slug")}
    data = json.loads(CANDIDATES.read_text())
    candidates = {c["slug"]: c for c in data.get("candidates", [])}

    if not promoted:
        print("No promoted slugs found")
        return 0

    with Session(engine) as s:
        creators = {c.name: c for c in s.exec(select(Creator)).all()}
        default_skill_creator = creators.get("Ops Foundry")
        default_persona_creator = creators.get("Epic Labs")

        inserted = 0
        updated = 0
        for slug in sorted(promoted):
            c = candidates.get(slug)
            if not c:
                continue

            ptype = PackType(c.get("type", "skill"))
            creator = default_skill_creator if ptype == PackType.skill else default_persona_creator
            scopes_csv = ",".join(c.get("scopes", []))

            existing = s.exec(select(Pack).where(Pack.slug == slug)).first()
            if existing:
                existing.title = c.get("title", existing.title)
                existing.description = c.get("problem", existing.description)
                existing.risk_level = c.get("risk_level", existing.risk_level)
                existing.scopes_csv = scopes_csv or existing.scopes_csv
                existing.is_featured = True
                if creator:
                    existing.creator_id = creator.id
                s.add(existing)
                updated += 1
            else:
                pack = Pack(
                    slug=slug,
                    title=c.get("title", slug),
                    type=ptype,
                    description=c.get("problem", ""),
                    risk_level=c.get("risk_level", "low"),
                    scopes_csv=scopes_csv,
                    is_featured=True,
                    creator_id=(creator.id if creator else None),
                )
                s.add(pack)
                inserted += 1

        s.commit()

    print(f"Promotion complete: inserted={inserted}, updated={updated}, total_promoted={len(promoted)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
