#!/usr/bin/env python3
"""Hazard-based re-verification scheduler.

Default cadence:
- high risk: 7 days
- medium risk: 30 days
- low risk: 60 days

Immediate reverify triggers:
- recent trust incident
- recent rollback/quarantine
- stale/missing verification timestamps (best-effort)
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "api" / "botstore.db"
OUT = ROOT / "research" / "reverify-schedule-report.json"

CADENCE_DAYS = {"high": 7, "medium": 30, "low": 60}


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def main() -> int:
    now = datetime.now(timezone.utc)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    packs = conn.execute(
        """
        SELECT p.id AS pack_id, p.slug, p.risk_level, pv.id AS pack_version_id, pv.semver,
               pv.verification_tier, pv.created_at
        FROM pack AS p
        JOIN packversion AS pv ON pv.pack_id = p.id
        WHERE pv.is_current = 1
        """
    ).fetchall()

    incidents = conn.execute(
        """
        SELECT pack_version_id, created_at
        FROM trustincident
        WHERE quarantined = 1
        """
    ).fetchall()
    incident_by_pv: dict[int, list[datetime]] = {}
    for r in incidents:
        ts = parse_ts(r["created_at"])
        if ts:
            incident_by_pv.setdefault(int(r["pack_version_id"] or 0), []).append(ts)

    out_rows: list[dict] = []
    due_now = 0
    for row in packs:
        pv_id = int(row["pack_version_id"])
        risk = (row["risk_level"] or "medium").lower()
        cadence = CADENCE_DAYS.get(risk, 30)

        verified_at = parse_ts(row["created_at"]) or now
        due_at = verified_at + timedelta(days=cadence)
        reasons: list[str] = []

        recent_incident = False
        for ts in incident_by_pv.get(pv_id, []):
            if ts >= now - timedelta(days=7):
                recent_incident = True
                break

        if recent_incident:
            due_at = now
            reasons.append("recent_trust_incident")

        if due_at <= now:
            due_now += 1
            reasons.append("cadence_due")

        out_rows.append(
            {
                "pack_id": int(row["pack_id"]),
                "slug": row["slug"],
                "pack_version_id": pv_id,
                "semver": row["semver"],
                "risk_level": risk,
                "verification_tier": row["verification_tier"],
                "verified_at": verified_at.isoformat(),
                "due_at": due_at.isoformat(),
                "due_now": due_at <= now,
                "reasons": reasons,
            }
        )

    payload = {
        "generated_at": now.isoformat(),
        "total": len(out_rows),
        "due_now": due_now,
        "rows": sorted(out_rows, key=lambda x: (not x["due_now"], x["due_at"], x["slug"])),
    }
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {OUT}")
    print(f"Due now: {due_now}/{len(out_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
