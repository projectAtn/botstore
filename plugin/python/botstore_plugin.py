#!/usr/bin/env python3
"""BotStore plugin for existing bots.

Goal: let any bot expose BotStore with a single command namespace (/botstore)
and natural-language fallback without forcing users into a separate bot.
"""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class BotStorePluginConfig:
    api_base: str = "http://127.0.0.1:8787"
    botstore_key: Optional[str] = None
    command_prefix: str = "/botstore"


class BotStorePlugin:
    def __init__(self, config: BotStorePluginConfig):
        self.config = config

    def _headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self.config.botstore_key:
            h["X-Botstore-Key"] = self.config.botstore_key
        return h

    def _post_json(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        req = urllib.request.Request(
            self.config.api_base.rstrip("/") + path,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers=self._headers(),
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _get_json(self, path: str) -> Dict[str, Any]:
        req = urllib.request.Request(
            self.config.api_base.rstrip("/") + path,
            method="GET",
            headers=self._headers(),
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def bind_target(self, user_id: str, runtime_id: str, agent_id: str, channel: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "user_id": user_id,
            "runtime_id": runtime_id,
            "agent_id": agent_id,
            "channel": channel,
            "set_default": True,
        }
        return self._post_json("/targets/bind", payload)

    def where(self, user_id: str) -> Dict[str, Any]:
        from urllib.parse import quote

        return self._get_json(f"/where?user_id={quote(user_id)}")

    def handle_text(self, user_id: str, text: str) -> Dict[str, Any]:
        """Route host-bot text into BotStore.

        Rules:
        - '/botstore' -> '/store'
        - '/botstore <subcmd>' -> '/<subcmd>'
        - plain text -> conversational search/install assistant
        """
        t = (text or "").strip()
        if not t:
            cmd = "/store"
        elif t.startswith(self.config.command_prefix):
            tail = t[len(self.config.command_prefix) :].strip()
            if not tail:
                cmd = "/store"
            elif tail.startswith("/"):
                cmd = tail
            else:
                cmd = "/" + tail
        else:
            cmd = t

        return self._post_json("/bot/command", {"user_id": user_id, "text": cmd})

    def handle_callback(self, user_id: str, callback_data: str) -> Dict[str, Any]:
        return self._post_json("/bot/callback", {"user_id": user_id, "callback_data": callback_data})


if __name__ == "__main__":
    # Tiny smoke test usage
    plugin = BotStorePlugin(BotStorePluginConfig())
    print(plugin.handle_text("telegram:demo", "/botstore"))
