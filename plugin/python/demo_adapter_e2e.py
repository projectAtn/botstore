#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from botstore_plugin import BotStorePlugin, BotStorePluginConfig
from adapters.copilotkit_adapter import CopilotKitAdapter


def main() -> int:
    api = os.getenv("BOTSTORE_API", "http://127.0.0.1:8787")
    key = os.getenv("BOTSTORE_BOT_KEY", "devkey")

    plugin = BotStorePlugin(BotStorePluginConfig(api_base=api, botstore_key=key, command_prefix="/botstore"))
    adapter = CopilotKitAdapter(plugin)

    user_id = "telegram:botstore_demo:1001"

    # 1) Link target
    bind = plugin.bind_target(user_id=user_id, runtime_id="openclaw-main", agent_id="demo-agent", channel="telegram")

    # 2) Search
    search = adapter.search(user_id, "triage inbox and schedule meetings with followups")
    if not search.ok:
        raise RuntimeError(search.error)

    top = (search.data.get("results") or [])[0]
    top_slug = top.get("slug") if top else "research-analyst"

    # 3) Install top result
    install = adapter.install(user_id, top_slug)
    if not install.ok:
        raise RuntimeError(install.error)

    # 4) Where installed
    where = adapter.where(user_id)
    if not where.ok:
        raise RuntimeError(where.error)

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api": api,
        "user_id": user_id,
        "bind": bind,
        "top_result_slug": top_slug,
        "install": install.data,
        "where": where.data,
    }

    result_json = Path("/Users/claw/.openclaw/workspace/botstore/research/adapter-e2e-result.json")
    result_md = Path("/Users/claw/.openclaw/workspace/botstore/research/adapter-e2e-report.md")
    result_json.write_text(json.dumps(out, indent=2))

    lines = [
        "# Adapter E2E Demo (CopilotKitAdapter)",
        "",
        f"- Time: {out['generated_at']}",
        f"- API: {api}",
        f"- User: `{user_id}`",
        f"- Bound target: `{bind.get('runtime_id')}/{bind.get('agent_id')}`",
        f"- Top search result: `{top_slug}`",
        "",
        "## Install response",
        "```json",
        json.dumps(install.data, indent=2),
        "```",
        "",
        "## Where response",
        "```json",
        json.dumps(where.data, indent=2),
        "```",
    ]
    result_md.write_text("\n".join(lines) + "\n")

    print(f"Wrote {result_json}")
    print(f"Wrote {result_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
