# BotStore Plugin (for existing bots)

Use this plugin to add BotStore to any existing bot without forcing users to switch to a dedicated BotStore bot.

## What it gives you
- `/botstore` command namespace inside your current bot.
- Conversational fallback (plain text intent -> pack suggestions).
- Target linking (`runtime_id` + `agent_id`) so install location is explicit.
- Callback passthrough for inline install/approve actions.

## Files
- `plugin/python/botstore_plugin.py`
- `plugin/python/example_host_bot.py`

## Install in host bot code
```python
from botstore_plugin import BotStorePlugin, BotStorePluginConfig

plugin = BotStorePlugin(BotStorePluginConfig(
    api_base="http://127.0.0.1:8787",
    botstore_key="devkey",
    command_prefix="/botstore",
))
```

## Typical host-bot routing
```python
# incoming message text from user
response = plugin.handle_text(user_id="telegram:8258812165", text="/botstore install research-analyst")

# send response["message"] back to user
# if response has buttons, map to your channel inline button format
```

## Link install target (important)
Users should be linked to a runtime target once:

```python
plugin.bind_target(
    user_id="telegram:8258812165",
    runtime_id="openclaw-main",
    agent_id="market-bot",
    channel="telegram",
)
```

After this, installs are marked as activated on that target.

## Commands users can run via `/botstore`
- `/botstore` -> opens store welcome
- `/botstore install <slug>`
- `/botstore bundle <slug>`
- `/botstore approvals`
- `/botstore approve <id>`
- `/botstore reject <id>`
- `/botstore where` (shows where packages are activated)
- `/botstore link <runtime_id> <agent_id>`

## Conversational mode
Users can type normal language without slash commands, e.g.:
- "I need help with campaign orchestration and SEO"

BotStore returns matching packs + install buttons.
