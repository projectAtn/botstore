#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from sqlmodel import Session, select

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "api"))

from app.main import Pack, engine

SIM = ROOT / "research" / "runtime-simulation-result.json"


def main() -> int:
    if not SIM.exists():
        print("No runtime simulation result found; nothing to enforce.")
        return 0

    payload = json.loads(SIM.read_text())
    delisted = set(payload.get("delisted_slugs", []))
    if not delisted:
        print("No delisted slugs.")
        return 0

    removed = 0
    with Session(engine) as s:
        packs = list(s.exec(select(Pack)).all())
        for p in packs:
            if p.slug in delisted:
                s.delete(p)
                removed += 1
        s.commit()

    print(f"Removed {removed} packs due to failed verification gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
