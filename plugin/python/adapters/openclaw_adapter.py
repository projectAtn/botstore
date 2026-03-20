from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    from ..botstore_plugin import BotStorePlugin
    from .base import AdapterResult
except Exception:  # pragma: no cover
    from botstore_plugin import BotStorePlugin
    from adapters.base import AdapterResult


@dataclass
class OpenClawAdapter:
    """Reference runtime adapter for OpenClaw.

    This adapter is intentionally strict about the control-plane flow:
    - resolve capability gaps via InstallAttempt v2
    - authorize sensitive actions per-call
    - report outcomes with observed scopes
    """

    plugin: BotStorePlugin
    name: str = "openclaw"

    def resolve_gap(
        self,
        *,
        task_id: str,
        tenant_id: str,
        user_id: str,
        agent_id: str,
        runtime_id: str,
        runtime_version: str,
        runtime_band: str,
        required_capabilities: list[str],
        enable_safe_exploration: bool = False,
        exploration_rate: float = 0.05,
        install_target_preference: Optional[str] = None,
        allow_gateway_plugin_store_autonomous: bool = False,
    ) -> AdapterResult:
        try:
            payload: Dict[str, Any] = {
                "task_id": task_id,
                "tenant_id": tenant_id,
                "user_id": user_id,
                "agent_id": agent_id,
                "runtime_id": runtime_id,
                "runtime_version": runtime_version,
                "runtime_band": runtime_band,
                "required_capabilities": required_capabilities,
                "enable_safe_exploration": enable_safe_exploration,
                "exploration_rate": exploration_rate,
                "install_target_preference": install_target_preference,
                "allow_gateway_plugin_store_autonomous": allow_gateway_plugin_store_autonomous,
            }
            data = self.plugin._post_json("/agent/install-by-capability-v2", payload)
            return AdapterResult(ok=bool(data.get("ok")), action="resolve_gap", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="resolve_gap", data={}, error=str(e))

    def install_status(self, *, tenant_id: Optional[str] = None, limit: int = 50) -> AdapterResult:
        try:
            qs = f"?limit={int(limit)}"
            if tenant_id:
                qs += f"&tenant_id={tenant_id}"
            data = self.plugin._get_json(f"/policy/decision-log{qs}")
            return AdapterResult(ok=True, action="install_status", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="install_status", data={}, error=str(e))

    def pre_action_authorize(
        self,
        *,
        attempt_id: str,
        pack_version_id: int,
        artifact_digest: str,
        requested_action: str,
        requested_scope: str,
        runtime_attestation: Optional[str] = None,
        justification: str = "",
    ) -> AdapterResult:
        try:
            payload = {
                "attempt_id": attempt_id,
                "pack_version_id": int(pack_version_id),
                "artifact_digest": artifact_digest,
                "requested_action": requested_action,
                "requested_scope": requested_scope,
                "runtime_attestation": runtime_attestation,
                "justification": justification,
            }
            data = self.plugin._post_json("/agent/action-authorize", payload)
            allowed = data.get("decision") in {"allow", "allow_with_runtime_proof"}
            return AdapterResult(ok=allowed, action="pre_action_authorize", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="pre_action_authorize", data={}, error=str(e))

    def pause_for_approval(
        self,
        *,
        attempt_id: str,
        tenant_id: str,
        session_key: str,
        run_id: str,
        reason: str = "approval_required",
        approval_mode: str = "once",
        ttl_minutes: int = 60,
    ) -> AdapterResult:
        try:
            payload = {
                "attempt_id": attempt_id,
                "tenant_id": tenant_id,
                "session_key": session_key,
                "run_id": run_id,
                "reason": reason,
                "approval_mode": approval_mode,
                "ttl_minutes": ttl_minutes,
            }
            data = self.plugin._post_json("/agent/approval-checkpoint/pause", payload)
            return AdapterResult(ok=bool(data.get("ok")), action="pause_for_approval", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="pause_for_approval", data={}, error=str(e))

    def resume_after_approval(self, *, checkpoint_id: str, approved: bool) -> AdapterResult:
        try:
            payload = {"checkpoint_id": checkpoint_id, "approved": approved}
            data = self.plugin._post_json("/agent/approval-checkpoint/resume", payload)
            return AdapterResult(ok=bool(data.get("ok")), action="resume_after_approval", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="resume_after_approval", data={}, error=str(e))

    def report_outcome(
        self,
        *,
        attempt_id: str,
        task_id: str,
        tenant_id: str,
        runtime_id: str,
        runtime_version: str,
        result: str,
        task_completed_after_install: bool,
        observed_scopes: list[str],
        incident_flag: bool = False,
        latency_ms: Optional[float] = None,
        human_intervention: str = "none",
    ) -> AdapterResult:
        try:
            payload = {
                "attempt_id": attempt_id,
                "task_id": task_id,
                "tenant_id": tenant_id,
                "runtime_id": runtime_id,
                "runtime_version": runtime_version,
                "result": result,
                "latency_ms": latency_ms,
                "human_intervention": human_intervention,
                "task_completed_after_install": task_completed_after_install,
                "observed_scopes": observed_scopes,
                "incident_flag": incident_flag,
                "privacy_mode": "standard",
            }
            data = self.plugin._post_json("/agent/outcome-v2", payload)
            return AdapterResult(ok=bool(data.get("ok")), action="report_outcome", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="report_outcome", data={}, error=str(e))

    @staticmethod
    def action_scope_map(tool_name: str, operation: str = "") -> Dict[str, str]:
        """Typed mapping used by middleware before side-effecting execution.

        Never infer sensitive scopes from free-form shell text.
        """

        key = f"{tool_name}:{operation}".strip(":")
        table = {
            "message.send": {"action_class": "message.send", "requested_scope": "message.send", "side_effect_level": "external_send"},
            "message.send:send": {"action_class": "message.send", "requested_scope": "message.send", "side_effect_level": "external_send"},
            "nodes.invoke": {"action_class": "device.invoke", "requested_scope": "device.invoke", "side_effect_level": "write"},
            "nodes.run": {"action_class": "device.command", "requested_scope": "device.command", "side_effect_level": "write"},
            "browser.act": {"action_class": "browser.act", "requested_scope": "browser.act", "side_effect_level": "write"},
            "exec": {"action_class": "shell.exec", "requested_scope": "shell.exec", "side_effect_level": "write"},
        }
        return table.get(key) or table.get(tool_name, {"action_class": "unknown", "requested_scope": "unknown", "side_effect_level": "write"})

    @staticmethod
    def hash_attestation(raw: str) -> str:
        return hashlib.sha256((raw or "").encode("utf-8")).hexdigest()
