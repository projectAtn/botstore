from dataclasses import dataclass
from typing import Any, Dict

try:
    from ..botstore_plugin import BotStorePlugin
    from .base import AdapterResult
except Exception:  # pragma: no cover
    from botstore_plugin import BotStorePlugin
    from adapters.base import AdapterResult


@dataclass
class ActivepiecesAdapter:
    """PoC adapter for Activepieces-like action blocks.

    Intended mapping:
    - Piece action: Search Packs
    - Piece action: Install Pack
    - Piece action: Where Installed
    """

    plugin: BotStorePlugin
    name: str = "activepieces"

    def search(self, user_id: str, query: str, runtime: str = "openclaw") -> AdapterResult:
        try:
            payload: Dict[str, Any] = {
                "user_id": user_id,
                "runtime": runtime,
                "query": query,
                "limit": 10,
                "constraints": {"risk_max": "medium"},
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
            data = self.plugin.where(user_id)
            return AdapterResult(ok=True, action="where", data=data)
        except Exception as e:
            return AdapterResult(ok=False, action="where", data={}, error=str(e))
