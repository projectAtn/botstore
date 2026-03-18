#!/usr/bin/env python3
import json
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:8787"


def http_json(path: str, method: str = "GET", payload=None):
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE + path, method=method, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def fail(msg: str):
    print(f"[FAIL] {msg}")
    sys.exit(1)


def main():
    print("[1/7] health")
    health = http_json("/health")
    if not health.get("ok"):
        fail("health endpoint not ok")

    print("[2/7] catalog non-empty")
    catalog = http_json("/catalog")
    if not isinstance(catalog, list) or not catalog:
        fail("catalog is empty")

    print("[3/7] interop import/export smoke")
    td = Path(tempfile.mkdtemp(prefix="botstore-regression-"))
    try:
        skill_dir = td / "skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            "# Regression Skill\n\nSmoke skill for CI regression.\n\n- `files.read`\n- `files.write`\n",
            encoding="utf-8",
        )
        imported = http_json("/interop/import-skill-folder", "POST", {"skill_path": str(skill_dir)})
        slug = imported.get("slug")
        if not slug:
            fail("interop import did not return slug")
        exported = http_json("/interop/export-skill", "POST", {"slug": slug, "out_dir": str(td / "out")})
        if not exported.get("ok"):
            fail("interop export failed")
    finally:
        shutil.rmtree(td, ignore_errors=True)

    print("[4/7] direct featured create should be blocked")
    payload = {
        "slug": "regression-featured-block",
        "title": "Regression Featured Block",
        "type": "skill",
        "version": "0.1.0",
        "description": "regression",
        "risk_level": "low",
        "scopes": ["files.read"],
        "bundle_pack_ids": [],
        "is_featured": True,
        "creator_id": None,
    }
    req = urllib.request.Request(
        BASE + "/packs", method="POST", data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req, timeout=20)
        fail("featured create was not blocked")
    except urllib.error.HTTPError as e:
        if e.code != 400:
            fail(f"unexpected status for featured block: {e.code}")

    print("[5/7] QA report upsert")
    target = next((p for p in catalog if p.get("slug") == "inbox-zero-pilot"), catalog[0])
    qa = http_json(
        "/qa/report",
        "POST",
        {
            "pack_id": target["id"],
            "status": "pass",
            "suite": "regression-ci",
            "report_path": "research/ci-regression.md",
            "summary": "regression smoke pass",
        },
    )
    if qa.get("status") != "pass":
        fail("qa upsert did not persist pass")

    print("[6/7] promote path should work after QA pass")
    promoted = http_json(f"/packs/{target['id']}/promote?featured=true", "PUT")
    if not promoted.get("is_featured"):
        fail("promotion did not set is_featured")

    print("[7/7] catalog exposes QA metadata")
    fresh = http_json("/catalog")
    row = next((p for p in fresh if p.get("id") == target["id"]), None)
    if not row:
        fail("target pack missing from catalog")
    if not row.get("qa_status"):
        fail("qa_status missing in catalog payload")

    print("[PASS] Regression CI smoke succeeded")


if __name__ == "__main__":
    main()
