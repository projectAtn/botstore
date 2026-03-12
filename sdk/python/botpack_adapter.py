from dataclasses import dataclass
from typing import Any, Protocol


class RuntimeBridge(Protocol):
    def call_capability(self, capability: str, payload: dict[str, Any]) -> Any: ...


@dataclass
class PolicyEngine:
    sensitive: set[str]

    def approval_required(self, capabilities: list[str], risk_level: str) -> bool:
        if risk_level == "high":
            return True
        return any(c in self.sensitive for c in capabilities)


@dataclass
class BotPackAdapter:
    runtime_name: str
    bridge: RuntimeBridge
    policy: PolicyEngine

    def install(self, pack: dict[str, Any], user_id: str) -> dict[str, Any]:
        caps = pack.get("capabilities", [])
        risk = pack.get("policy", {}).get("riskLevel", "low")
        return {
            "runtime": self.runtime_name,
            "user_id": user_id,
            "pack_id": pack.get("id"),
            "approval_required": self.policy.approval_required(caps, risk),
            "status": "pending_approval" if self.policy.approval_required(caps, risk) else "installed",
        }

    def execute(self, capability: str, payload: dict[str, Any]) -> Any:
        return self.bridge.call_capability(capability, payload)
