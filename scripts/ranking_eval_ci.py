#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

import os

BASE = os.getenv("BOTSTORE_API_BASE", "http://127.0.0.1:8787")
ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "research" / "ranking-eval-current.json"
OUT_MD = ROOT / "research" / "ranking-eval-report.md"
LAST_JSON = ROOT / "research" / "ranking-eval-last.json"

# Expected slugs can include alternatives to tolerate normal ranking variations.
GOLDEN = [
    {
        "id": "ops-calendar-crm",
        "query": "triage inbox schedule meetings and keep CRM synced",
        "expected": ["crm-sync-bidirectional", "calendar-ops-coordinator", "email-outreach-sequencer"],
    },
    {
        "id": "security-governance",
        "query": "prioritize security alerts enforce policy and maintain audit trail",
        "expected": ["security-alert-triager", "deploy-rollback-guardian", "incident-triage-commander"],
    },
    {
        "id": "content-growth",
        "query": "repurpose content into short posts and SEO briefs",
        "expected": ["shortform-content-factory", "seo-brief-builder", "keyword-cluster-mapper"],
    },
    {
        "id": "community-support",
        "query": "manage support across telegram discord whatsapp",
        "expected": ["telegram-community-manager", "discord-community-manager", "whatsapp-support-copilot"],
    },
    {
        "id": "research-citations",
        "query": "research mode with citations and source confidence",
        "expected": ["research-librarian-persona", "citation-verifier", "research-reliability-bundle"],
    },
    {
        "id": "finance-controls",
        "query": "reconcile invoices and audit expense policy exceptions",
        "expected": ["finance-control-bundle", "invoice-expense-audit-bundle", "invoice-reconciliation"],
    },
    {
        "id": "market-intel",
        "query": "monitor reddit x and github for user pain points and competitor moves",
        "expected": ["market-intel-signal-bundle", "reddit-scout-pro", "github-issue-radar"],
    },
    {
        "id": "personality-compliance",
        "query": "strict compliance officer personality that blocks risky requests",
        "expected": ["strict-compliance-officer-persona"],
    },
]


def http_json(path: str, method: str = "GET", payload=None):
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE + path, method=method, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def run_eval():
    cases = []
    for g in GOLDEN:
        res = http_json(
            "/agent/search",
            "POST",
            {
                "user_id": "ranking-eval-ci",
                "runtime": "openclaw-main",
                "query": g["query"],
                "missing_capabilities": [],
                "constraints": {"risk_max": "medium"},
                "limit": 10,
            },
        )
        results = res.get("results", [])
        slugs = [r.get("slug") for r in results]

        best_rank = None
        best_slug = None
        for target in g["expected"]:
            if target in slugs:
                rank = slugs.index(target) + 1
                if best_rank is None or rank < best_rank:
                    best_rank = rank
                    best_slug = target

        cases.append(
            {
                "id": g["id"],
                "query": g["query"],
                "expected": g["expected"],
                "best_match_slug": best_slug,
                "best_rank": best_rank,
                "hit_top3": best_rank is not None and best_rank <= 3,
                "hit_top5": best_rank is not None and best_rank <= 5,
                "top5": slugs[:5],
            }
        )

    summary = {
        "total": len(cases),
        "hit_top3": sum(1 for c in cases if c["hit_top3"]),
        "hit_top5": sum(1 for c in cases if c["hit_top5"]),
    }
    summary["top3_rate"] = round(summary["hit_top3"] / max(summary["total"], 1), 3)
    summary["top5_rate"] = round(summary["hit_top5"] / max(summary["total"], 1), 3)

    return cases, summary


def load_last():
    if LAST_JSON.exists():
        try:
            return json.loads(LAST_JSON.read_text())
        except Exception:
            return None
    return None


def compute_drift(current: dict, previous: dict | None):
    if not previous:
        return {"has_previous": False}

    prev_by_id = {c["id"]: c for c in previous.get("cases", [])}
    rank_deltas = []
    regressions = []
    for c in current.get("cases", []):
        p = prev_by_id.get(c["id"])
        if not p:
            continue
        cr = c.get("best_rank")
        pr = p.get("best_rank")
        if cr is None and pr is None:
            delta = 0
        elif cr is None:
            delta = 99
        elif pr is None:
            delta = -99
        else:
            delta = cr - pr
        rank_deltas.append(delta)
        if delta > 0:
            regressions.append({"id": c["id"], "delta": delta, "prev_rank": pr, "curr_rank": cr})

    prev_summary = previous.get("summary", {})
    curr_summary = current.get("summary", {})
    return {
        "has_previous": True,
        "top3_rate_delta": round(curr_summary.get("top3_rate", 0) - prev_summary.get("top3_rate", 0), 3),
        "top5_rate_delta": round(curr_summary.get("top5_rate", 0) - prev_summary.get("top5_rate", 0), 3),
        "mean_rank_delta": round(sum(rank_deltas) / max(len(rank_deltas), 1), 3),
        "regressions": regressions,
    }


def write_report(payload: dict):
    lines = [
        "# Ranking Eval CI Report",
        "",
        f"Generated: {payload['generatedAt']}",
        "",
        f"Top-3 hit: **{payload['summary']['hit_top3']}/{payload['summary']['total']}** ({payload['summary']['top3_rate']})",
        f"Top-5 hit: **{payload['summary']['hit_top5']}/{payload['summary']['total']}** ({payload['summary']['top5_rate']})",
        "",
        "## Cases",
        "",
        "| case | best match | rank | top3 | top5 |",
        "|---|---|---:|---|---|",
    ]
    for c in payload["cases"]:
        lines.append(
            f"| `{c['id']}` | `{c['best_match_slug']}` | {c['best_rank']} | {'✅' if c['hit_top3'] else '❌'} | {'✅' if c['hit_top5'] else '❌'} |"
        )

    drift = payload.get("drift", {})
    lines += ["", "## Drift"]
    if not drift.get("has_previous"):
        lines.append("- No previous baseline found.")
    else:
        lines.append(f"- top3_rate_delta: {drift.get('top3_rate_delta')}")
        lines.append(f"- top5_rate_delta: {drift.get('top5_rate_delta')}")
        lines.append(f"- mean_rank_delta: {drift.get('mean_rank_delta')}")
        if drift.get("regressions"):
            lines.append("- Regressions:")
            for r in drift["regressions"]:
                lines.append(f"  - `{r['id']}` rank {r['prev_rank']} -> {r['curr_rank']} (delta {r['delta']})")
        else:
            lines.append("- Regressions: none")

    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    previous = load_last()
    cases, summary = run_eval()
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "cases": cases,
    }
    payload["drift"] = compute_drift(payload, previous)

    OUT_JSON.write_text(json.dumps(payload, indent=2))
    LAST_JSON.write_text(json.dumps(payload, indent=2))
    write_report(payload)

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {LAST_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"Top3: {summary['hit_top3']}/{summary['total']} | Top5: {summary['hit_top5']}/{summary['total']}")


if __name__ == "__main__":
    main()
