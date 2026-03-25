#!/usr/bin/env python3
import json
import time
import urllib.request
from pathlib import Path

import os

BASE = os.getenv("BOTSTORE_API_BASE", "http://127.0.0.1:8787")
OUT = Path(__file__).resolve().parents[1] / "research" / "pack-test-report.md"
JSON_OUT = Path(__file__).resolve().parents[1] / "research" / "pack-test-result.json"
SUITE = "pack-smoke-v1"


def http_json(path: str, method: str = "GET", payload=None):
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE + path, method=method, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def run() -> tuple[list[dict], dict]:
    packs = http_json("/catalog")
    results = []

    for p in packs:
        t0 = time.time()
        checks = []

        # Check 1: compatibility endpoint
        try:
            comp = http_json(f"/agent/compatibility/{p['id']}?runtime=openclaw&version=0.1.0")
            checks.append({"name": "compatibility", "pass": bool(comp.get("status"))})
        except Exception:
            checks.append({"name": "compatibility", "pass": False})

        # Check 2: policy evaluate endpoint
        try:
            pol = http_json("/agent/policy-evaluate", "POST", {
                "user_id": "test-user",
                "runtime": "openclaw",
                "pack_id": p["id"],
            })
            checks.append({"name": "policy_evaluate", "pass": pol.get("decision") in {"allow", "require_approval"}})
        except Exception:
            checks.append({"name": "policy_evaluate", "pass": False})

        # Check 3: install flow
        try:
            install = http_json("/installs", "POST", {"user_id": "pack-test-user", "pack_id": p["id"]})
            checks.append({"name": "install", "pass": bool(install.get("install", {}).get("id"))})
        except Exception:
            checks.append({"name": "install", "pass": False})

        # Check 4: outcome logging
        try:
            out = http_json("/agent/outcome", "POST", {
                "user_id": "pack-test-user",
                "task_id": f"smoke-{p['slug']}",
                "runtime": "openclaw",
                "pack_id": p["id"],
                "success": True,
                "latency_ms": 100,
            })
            checks.append({"name": "outcome_log", "pass": bool(out.get("ok"))})
        except Exception:
            checks.append({"name": "outcome_log", "pass": False})

        passed = sum(1 for c in checks if c["pass"])
        score = round(100 * passed / len(checks))
        latency_ms = round((time.time() - t0) * 1000, 1)
        results.append({
            "pack_id": p["id"],
            "slug": p["slug"],
            "type": p["type"],
            "score": score,
            "latency_ms": latency_ms,
            "checks": checks,
            "pass": score >= 75,
        })

    summary = {
        "total": len(results),
        "pass": sum(1 for r in results if r["pass"]),
        "avg_score": round(sum(r["score"] for r in results) / max(len(results), 1), 1),
    }
    return results, summary


def publish_qa_artifacts(results: list[dict]):
    report_path = str(OUT.relative_to(Path(__file__).resolve().parents[1]))
    published = 0
    failed = 0

    for r in results:
        status = "pass" if r["pass"] else "fail"
        summary = f"score={r['score']}; latency_ms={r['latency_ms']}"
        payload = {
            "pack_id": r["pack_id"],
            "status": status,
            "suite": SUITE,
            "report_path": report_path,
            "summary": summary,
        }
        try:
            http_json("/qa/report", "POST", payload)
            published += 1
        except Exception:
            failed += 1

    return {"published": published, "failed": failed}


def main():
    results, summary = run()
    JSON_OUT.write_text(json.dumps({"summary": summary, "results": results}, indent=2))

    lines = [
        "# Pack Test Runner Report",
        "",
        f"Suite: {SUITE}",
        f"Total packs: {summary['total']}",
        f"Pass: {summary['pass']}",
        f"Average score: {summary['avg_score']}",
        "",
        "| slug | type | score | latency_ms | pass |",
        "|---|---|---:|---:|---|",
    ]
    for r in results:
        lines.append(f"| `{r['slug']}` | {r['type']} | {r['score']} | {r['latency_ms']} | {'✅' if r['pass'] else '❌'} |")

    OUT.write_text("\n".join(lines) + "\n")

    qa_push = publish_qa_artifacts(results)
    print(f"Wrote {OUT}")
    print(f"Wrote {JSON_OUT}")
    print(f"QA artifact push: published={qa_push['published']} failed={qa_push['failed']}")


if __name__ == "__main__":
    main()
