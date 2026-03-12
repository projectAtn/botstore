# Bot command mapping (Telegram-ready)

Use this endpoint from your bot backend:

- `POST /bot/command`
  - body: `{ "user_id": "telegram:<chat_id>", "text": "/store" }`

## Supported commands

- `/store`
  - Returns store URL + button payload to open BotStore webview.
- `/install <pack-slug>`
  - Installs one pack.
- `/bundle <bundle-slug>`
  - Installs bundle + defined child packs.
- `/approvals`
  - Lists pending approval queue for user.
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
