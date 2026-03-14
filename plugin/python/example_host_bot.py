#!/usr/bin/env python3
"""Example host bot integration with BotStorePlugin.

This demonstrates how an existing bot can delegate /botstore commands and
normal user intent text to BotStore.
"""

import os

from botstore_plugin import BotStorePlugin, BotStorePluginConfig


def main() -> None:
    plugin = BotStorePlugin(
        BotStorePluginConfig(
            api_base=os.getenv("BOTSTORE_API", "http://127.0.0.1:8787"),
            botstore_key=os.getenv("BOTSTORE_BOT_KEY"),
            command_prefix="/botstore",
        )
    )

    user_id = "telegram:8258812165"

    # Link this user to a runtime target once:
    plugin.bind_target(user_id=user_id, runtime_id="openclaw-main", agent_id="market-bot", channel="telegram")

    # Command mode
    print(plugin.handle_text(user_id, "/botstore install research-analyst"))

    # Conversational mode
    print(plugin.handle_text(user_id, "I need help with campaign orchestration and SEO"))

    # Visibility mode
    print(plugin.handle_text(user_id, "/botstore where"))


if __name__ == "__main__":
    main()
