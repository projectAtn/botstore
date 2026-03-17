from dataclasses import dataclass
from typing import Any, Dict

from ..botstore_plugin import BotStorePlugin
from .base import AdapterResult


@dataclass
class E2BSandboxAdapter:
    """PoC adapter for E2B-style sandbox verification workflows.

    Goal: validate a pack can be discovered/installed safely before broad rollout.
    """

    plugin: BotStorePlugin
    name: str = "e2b"

    def search(self, user_id: str, query: str, runtime: str = "openclaw") -> AdapterResult:
        try:
            payload: Dict[str, Any] = {
                "user_id": user_id,
                "runtime": runtime,
                "query": query,
                "limit": 3,
            }
            data = self.plugin._post_json("/agent/search", payload)
            return AdapterResult(ok=True, action="search", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="search", data={}, error=str(e))

    def install(self, user_id: str, slug: str) -> AdapterResult:
        try:
            # In sandbox mode this should be a dry-run in future versions.
            data = self.plugin.handle_text(user_id, f"/botstore install {slug}")
            return AdapterResult(ok=True, action="install", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="install", data={}, error=str(e))

    def where(self, user_id: str) -> AdapterResult:
        try:
            data = self.plugin.where(user_id)
            return AdapterResult(ok=True, action="where", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="where", data={}, error=str(e))
