#!/usr/bin/env python3
"""Apply canonical capability taxonomy updates to key packs.

Usage:
  cd botstore/api
  source .venv/bin/activate
  python ../scripts/apply_capability_taxonomy_v1.py
"""

import sys
from pathlib import Path

from sqlmodel import Session, select

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "api"))

from app.main import Pack, engine  # noqa: E402

UPDATES = {
    "policy-compliance-guard": ["policy.enforce", "risk.evaluate", "audit.log.write", "audit.log.read"],
    "approval-policy-brain": ["policy.enforce", "risk.evaluate"],
    "policy-drift-detector": ["policy.enforce", "risk.evaluate", "audit.log.read"],
    "secret-leak-preventer": ["risk.evaluate", "audit.log.write"],
    "pii-redaction-firewall": ["risk.evaluate", "audit.log.write"],
    "social-listening-response-drafter": [
        "marketing.content_repurpose",
        "marketing.campaign_orchestration",
        "marketing.analytics",
    ],
    "growth-experiment-orchestrator": ["marketing.campaign_orchestration", "marketing.analytics"],
    "ad-creative-feedback-loop": ["marketing.content_repurpose", "marketing.seo", "marketing.analytics"],
    "crm-followup-autopilot": ["marketing.campaign_orchestration", "marketing.analytics"],
}


def main() -> int:
    with Session(engine) as s:
        updated = 0
        for slug, extras in UPDATES.items():
            p = s.exec(select(Pack).where(Pack.slug == slug)).first()
            if not p:
                continue
            scopes = [x.strip() for x in (p.scopes_csv or "").split(",") if x.strip()]
            merged = []
            seen = set()
            for x in scopes + extras:
                if x not in seen:
                    seen.add(x)
                    merged.append(x)
            p.scopes_csv = ",".join(merged)
            s.add(p)
            updated += 1
        s.commit()
    print(f"Updated packs: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
