from dataclasses import dataclass
from typing import Any, Dict, Protocol


@dataclass
class AdapterResult:
    ok: bool
    action: str
    data: Dict[str, Any]
    error: str = ""


class BotStoreAdapter(Protocol):
    name: str

    def search(self, user_id: str, query: str, runtime: str = "openclaw") -> AdapterResult: ...

    def install(self, user_id: str, slug: str) -> AdapterResult: ...

    def where(self, user_id: str) -> AdapterResult: ...
