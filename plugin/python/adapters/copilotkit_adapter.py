from dataclasses import dataclass
from typing import Any, Dict

try:
    from ..botstore_plugin import BotStorePlugin
    from .base import AdapterResult
except Exception:  # pragma: no cover
    from botstore_plugin import BotStorePlugin
    from adapters.base import AdapterResult


@dataclass
class CopilotKitAdapter:
    """PoC adapter for CopilotKit-style assistant actions.

    This wraps BotStorePlugin in action-like methods that can be bound to
    CopilotKit tool/action handlers.
    """

    plugin: BotStorePlugin
    name: str = "copilotkit"

    def search(self, user_id: str, query: str, runtime: str = "openclaw") -> AdapterResult:
        try:
            payload: Dict[str, Any] = {
                "user_id": user_id,
                "runtime": runtime,
                "query": query,
                "limit": 5,
            }
            data = self.plugin._post_json("/agent/search", payload)
            return AdapterResult(ok=True, action="search", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="search", data={}, error=str(e))

    def install(self, user_id: str, slug: str) -> AdapterResult:
        try:
            data = self.plugin.handle_text(user_id, f"/botstore install {slug}")
            return AdapterResult(ok=True, action="install", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="install", data={}, error=str(e))

    def where(self, user_id: str) -> AdapterResult:
        try:
            data = self.plugin.handle_text(user_id, "/botstore where")
            return AdapterResult(ok=True, action="where", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="where", data={}, error=str(e))
