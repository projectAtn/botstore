# Telegram bridge (BotStore chat)

This bridge wires Telegram messages directly into BotStore chat commands.

## Environment

```bash
export TELEGRAM_BOT_TOKEN="<botfather-token>"
export BOTSTORE_API="http://127.0.0.1:8787"
export BOTSTORE_BOT_KEY="devkey"   # must match API server if auth enabled
```

## Run

### Option A: direct env exports
```bash
cd botstore/integrations
python3 telegram_bridge.py
```

### Option B: env file + helper script (recommended)
```bash
cd botstore/integrations
cp .env.telegram.example .env.telegram
# edit .env.telegram with your real token
./run_telegram_bridge.sh
```

## Identity isolation (important)

Bridge now namespaces users by bot identity:
- `user_id = telegram:<bot_username>:<chat_id>` (fallback `telegram:<bot_id>:<chat_id>`)

This keeps installs separated per Telegram bot, even if the same human chat id exists across multiple bots.

## Supported in Telegram chat

- `/store`
- `/install <pack-slug>`
- `/bundle <bundle-slug>`
- `/approvals`
- `/approve <id>`
- `/reject <id>`
- `/installs`

Inline callback buttons from `/store` and `/approvals` are handled automatically.
