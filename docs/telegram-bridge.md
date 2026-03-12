# Telegram bridge (BotStore chat)

This bridge wires Telegram messages directly into BotStore chat commands.

## Environment

```bash
export TELEGRAM_BOT_TOKEN="<botfather-token>"
export BOTSTORE_API="http://127.0.0.1:8787"
export BOTSTORE_BOT_KEY="devkey"   # must match API server if auth enabled
```

## Run

```bash
cd botstore/integrations
python3 telegram_bridge.py
```

## Supported in Telegram chat

- `/store`
- `/install <pack-slug>`
- `/bundle <bundle-slug>`
- `/approvals`
- `/approve <id>`
- `/reject <id>`
- `/installs`

Inline callback buttons from `/store` and `/approvals` are handled automatically.
