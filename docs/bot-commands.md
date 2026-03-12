# Bot command mapping (Telegram-ready)

Use these endpoints from your bot backend:

- `POST /bot/command`
  - body: `{ "user_id": "telegram:<chat_id>", "text": "/store" }`
- `POST /bot/callback`
  - body: `{ "user_id": "telegram:<chat_id>", "callback_data": "approve:12" }`

Optional auth hardening:
- set env `BOTSTORE_BOT_KEY` on server
- then send header `X-Botstore-Key: <same-value>` to all `/bot/*` endpoints

## Supported commands

- `/store`
  - Returns store URL + button payload to open BotStore webview.
- `/install <pack-slug>`
  - Installs one pack.
- `/bundle <bundle-slug>`
  - Installs bundle + defined child packs.
- `/approvals`
  - Lists pending approval queue for user and returns inline button payloads for approve/reject.
- `/approve <approval-id>`
  - Approves pending approval item.
- `/reject <approval-id>`
  - Rejects pending approval item.
- `/installs`
  - Returns install count for user.

## Example response

```json
{
  "ok": true,
  "message": "Open store",
  "action": "open_store",
  "data": {
    "url": "http://127.0.0.1:8787/?user_id=telegram:8258812165",
    "buttons": [[{"text":"Open BotStore","callback_data":"open:http://127.0.0.1:8787/?user_id=telegram:8258812165","style":"primary"}]]
  }
}
```
