#!/usr/bin/env python3
import json
import os
import sqlite3
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = os.getenv("BOTSTORE_API_BASE", "http://127.0.0.1:8787")
SRC_SQLITE = Path(os.getenv("BOTSTORE_SRC_SQLITE", str(Path(__file__).resolve().parents[1] / "api" / "botstore.db")))


def http_json(path: str, method: str = "GET", payload=None):
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_BASE + path, method=method, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def safe_post(path: str, payload: dict):
    try:
        return http_json(path, "POST", payload), None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        return None, {"status": e.code, "body": body[:500]}


def main():
    if not SRC_SQLITE.exists():
        raise SystemExit(f"source sqlite not found: {SRC_SQLITE}")

    conn = sqlite3.connect(SRC_SQLITE)
    conn.row_factory = sqlite3.Row

    creators = [dict(r) for r in conn.execute("SELECT id,name,verification,trust_score FROM creator ORDER BY id").fetchall()]
    packs = [dict(r) for r in conn.execute("SELECT id,slug,title,type,version,description,risk_level,scopes_csv,bundle_pack_ids_csv,is_featured,creator_id FROM pack ORDER BY id").fetchall()]

    # Existing destination state
    dst_catalog = http_json("/catalog")
    dst_by_slug = {p["slug"]: p for p in dst_catalog}
    dst_creators = http_json("/creators")
    dst_creator_by_name = {c["name"]: c for c in dst_creators}

    # Ensure creators
    created_creators = []
    for c in creators:
        if c["name"] in dst_creator_by_name:
            continue
        payload = {
            "name": c["name"],
            "verification": c.get("verification") or "unverified",
            "trust_score": float(c.get("trust_score") or 0.5),
        }
        out, err = safe_post("/creators", payload)
        if out:
            created_creators.append(c["name"])
        else:
            # creator might already exist due race; ignore 400 duplicates
            pass

    # Refresh creators map
    dst_creators = http_json("/creators")
    dst_creator_by_name = {c["name"]: c for c in dst_creators}

    src_creator_by_id = {c["id"]: c for c in creators}

    # Two-pass pack creation: non-bundle then bundle
    created = []
    skipped = []
    failed = []

    non_bundles = [p for p in packs if p.get("type") != "bundle"]
    bundles = [p for p in packs if p.get("type") == "bundle"]

    def create_pack(src_pack, bundle_ids=None):
        if src_pack["slug"] in dst_by_slug:
            skipped.append(src_pack["slug"])
            return

        src_creator = src_creator_by_id.get(src_pack.get("creator_id"))
        creator_id = None
        if src_creator:
            creator = dst_creator_by_name.get(src_creator["name"])
            creator_id = creator["id"] if creator else None

        payload = {
            "slug": src_pack["slug"],
            "title": src_pack["title"],
            "type": src_pack["type"],
            "version": src_pack.get("version") or "0.1.0",
            "description": src_pack.get("description") or "",
            "risk_level": src_pack.get("risk_level") or "low",
            "scopes": [s for s in (src_pack.get("scopes_csv") or "").split(",") if s],
            "bundle_pack_ids": bundle_ids or [],
            "is_featured": False,
            "creator_id": creator_id,
        }
        out, err = safe_post("/packs", payload)
        if out:
            created.append(src_pack["slug"])
            dst_by_slug[src_pack["slug"]] = {"slug": src_pack["slug"], "id": out.get("id")}
        else:
            failed.append({"slug": src_pack["slug"], "error": err})

    for p in non_bundles:
        create_pack(p)

    # refresh catalog for bundle child id mapping
    dst_catalog = http_json("/catalog")
    dst_by_slug = {p["slug"]: p for p in dst_catalog}
    src_pack_by_id = {p["id"]: p for p in packs}

    for p in bundles:
        child_ids = []
        raw = p.get("bundle_pack_ids_csv") or ""
        for sid in [x.strip() for x in raw.split(",") if x.strip().isdigit()]:
            src_child = src_pack_by_id.get(int(sid))
            if not src_child:
                continue
            dst_child = dst_by_slug.get(src_child["slug"])
            if dst_child:
                child_ids.append(dst_child["id"])
        create_pack(p, bundle_ids=child_ids)

    result = {
        "source_sqlite": str(SRC_SQLITE),
        "api_base": API_BASE,
        "source_counts": {"creators": len(creators), "packs": len(packs)},
        "created_creators": created_creators,
        "created_packs": len(created),
        "skipped_packs": len(skipped),
        "failed_packs": failed[:50],
    }

    out_path = Path(__file__).resolve().parents[1] / "research" / "bootstrap-postgres-from-sqlite-report.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"report: {out_path}")


if __name__ == "__main__":
    main()
