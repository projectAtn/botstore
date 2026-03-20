#!/usr/bin/env python3
"""OpenClaw reference adapter smoke flow.

Runs:
1) resolve_gap (install-by-capability-v2)
2) pre_action_authorize
3) report_outcome (success)
4) report_outcome (scope violation -> quarantine)
5) fetch control-plane status + policy decision log
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from botstore_plugin import BotStorePlugin, BotStorePluginConfig
from adapters.openclaw_adapter import OpenClawAdapter


def main() -> int:
    api = os.getenv("BOTSTORE_API", "http://127.0.0.1:8787")
    key = os.getenv("BOTSTORE_BOT_KEY", "")
    tenant_id = os.getenv("TENANT_ID", "default")
    runtime_id = os.getenv("RUNTIME_ID", "openclaw")
    runtime_band = os.getenv("RUNTIME_BAND", "B")
    user_id = os.getenv("USER_ID", "telegram:openclaw_adapter_demo")
    agent_id = os.getenv("AGENT_ID", "openclaw-agent-demo")

    ts = int(time.time())
    task_id = f"task-openclaw-smoke-{ts}"

    plugin = BotStorePlugin(BotStorePluginConfig(api_base=api, botstore_key=(key or None), command_prefix="/botstore"))
    adapter = OpenClawAdapter(plugin)

    resolve = adapter.resolve_gap(
        task_id=task_id,
        tenant_id=tenant_id,
        user_id=user_id,
        agent_id=agent_id,
        runtime_id=runtime_id,
        runtime_version="0.2.0",
        runtime_band=runtime_band,
        required_capabilities=["deploy.rollback"],
        enable_safe_exploration=True,
        exploration_rate=0.05,
        install_target_preference="agent_workspace",
        allow_gateway_plugin_store_autonomous=False,
    )
    if not resolve.ok:
        raise RuntimeError(resolve.error or "resolve_gap failed")

    selected = resolve.data.get("selected") or {}
    attempt_id = resolve.data.get("attempt_id")
    pack_version_id = int(selected.get("pack_version_id"))
    artifact_digest = selected.get("artifact_digest")

    auth = adapter.pre_action_authorize(
        attempt_id=attempt_id,
        pack_version_id=pack_version_id,
        artifact_digest=artifact_digest,
        requested_action="message.send",
        requested_scope="message.send",
        justification="openclaw adapter smoke",
    )
    if not auth.ok:
        # allow deny in strict policies, but preserve payload
        pass

    pause = adapter.pause_for_approval(
        attempt_id=attempt_id,
        tenant_id=tenant_id,
        session_key=f"session:{user_id}",
        run_id=f"run-{ts}",
        ttl_minutes=30,
    )
    resume = None
    if pause.ok and pause.data.get("checkpoint_id"):
        resume = adapter.resume_after_approval(
            checkpoint_id=str(pause.data.get("checkpoint_id")),
            approved=True,
        )

    out_ok = adapter.report_outcome(
        attempt_id=attempt_id,
        task_id=task_id,
        tenant_id=tenant_id,
        runtime_id=runtime_id,
        runtime_version="0.2.0",
        result="success",
        task_completed_after_install=True,
        observed_scopes=["message.send"],
        incident_flag=False,
        latency_ms=250,
    )
    if not out_ok.ok:
        raise RuntimeError(out_ok.error or "outcome success report failed")

    out_violation = adapter.report_outcome(
        attempt_id=attempt_id,
        task_id=f"{task_id}-violation",
        tenant_id=tenant_id,
        runtime_id=runtime_id,
        runtime_version="0.2.0",
        result="fail",
        task_completed_after_install=False,
        observed_scopes=["payment.charge"],
        incident_flag=True,
        latency_ms=300,
    )

    rollback = adapter.rollback_attempt(attempt_id=attempt_id, tenant_id=tenant_id, reason="scope_violation_quarantine")

    status = plugin._get_json(f"/status/control-plane?tenant_id={tenant_id}&lookback_days=30")
    decisions = plugin._get_json(f"/policy/decision-log?tenant_id={tenant_id}&limit=20")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api": api,
        "tenant_id": tenant_id,
        "runtime_id": runtime_id,
        "runtime_band": runtime_band,
        "task_id": task_id,
        "attempt_id": attempt_id,
        "resolve": resolve.data,
        "authorize": auth.data,
        "pause": pause.data,
        "resume": (resume.data if resume else None),
        "outcome_success": out_ok.data,
        "outcome_violation": out_violation.data,
        "rollback": rollback.data,
        "status": status,
        "decision_log_count": decisions.get("count"),
    }

    out_json = Path("/Users/claw/.openclaw/workspace/botstore/research/openclaw-adapter-e2e-result.json")
    out_md = Path("/Users/claw/.openclaw/workspace/botstore/research/openclaw-adapter-e2e-report.md")
    out_json.write_text(json.dumps(payload, indent=2))

    out_md.write_text(
        "\n".join(
            [
                "# OpenClaw Adapter E2E",
                "",
                f"- Time: {payload['generated_at']}",
                f"- API: {api}",
                f"- Attempt: `{attempt_id}`",
                f"- Runtime: `{runtime_id}` band `{runtime_band}`",
                "",
                "## Resolve",
                "```json",
                json.dumps(resolve.data, indent=2),
                "```",
                "",
                "## Authorize",
                "```json",
                json.dumps(auth.data, indent=2),
                "```",
                "",
                "## Approval pause",
                "```json",
                json.dumps(pause.data, indent=2),
                "```",
                "",
                "## Approval resume",
                "```json",
                json.dumps((resume.data if resume else {"ok": False, "reason": "pause failed"}), indent=2),
                "```",
                "",
                "## Outcome violation",
                "```json",
                json.dumps(out_violation.data, indent=2),
                "```",
                "",
                "## Rollback",
                "```json",
                json.dumps(rollback.data, indent=2),
                "```",
                "",
                f"Decision log rows: {decisions.get('count')}",
            ]
        )
        + "\n"
    )

    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
