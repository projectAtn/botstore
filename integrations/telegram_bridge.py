#!/usr/bin/env python3
import json
import os
import time
import urllib.parse
import urllib.request
from typing import Dict, Optional

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
BOTSTORE_API = os.getenv("BOTSTORE_API", "http://127.0.0.1:8787").rstrip("/")
BOTSTORE_KEY = os.getenv("BOTSTORE_BOT_KEY", "").strip()

if not BOT_TOKEN:
    raise SystemExit("Missing TELEGRAM_BOT_TOKEN")

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"


def http_json(url: str, method: str = "GET", payload: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
    data = None
    req_headers = headers or {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=req_headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8")
    return json.loads(body)


def call_botstore(path: str, payload: dict) -> dict:
    headers = {}
    if BOTSTORE_KEY:
        headers["X-Botstore-Key"] = BOTSTORE_KEY
    return http_json(f"{BOTSTORE_API}{path}", method="POST", payload=payload, headers=headers)


def tg_send(chat_id: int, text: str, buttons: list | None = None) -> None:
    payload = {"chat_id": chat_id, "text": text}
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}
    http_json(f"{API_BASE}/sendMessage", method="POST", payload=payload)


def handle_message(msg: dict) -> None:
    chat_id = msg["chat"]["id"]
    text = (msg.get("text") or "").strip()
    if not text:
        return
    user_id = f"telegram:{chat_id}"
    res = call_botstore("/bot/command", {"user_id": user_id, "text": text})
    tg_send(chat_id, res.get("message", "OK"), res.get("data", {}).get("buttons"))


def handle_callback(cb: dict) -> None:
    chat_id = cb["message"]["chat"]["id"]
    data = (cb.get("data") or "").strip()
    user_id = f"telegram:{chat_id}"
    res = call_botstore("/bot/callback", {"user_id": user_id, "callback_data": data})
    tg_send(chat_id, res.get("message", "Done"), res.get("data", {}).get("buttons"))
    http_json(f"{API_BASE}/answerCallbackQuery", method="POST", payload={"callback_query_id": cb["id"]})


def main() -> None:
    offset = 0
    print("Telegram bridge started")
    while True:
        try:
            url = f"{API_BASE}/getUpdates?timeout=25&offset={offset}"
            data = http_json(url)
            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                if "message" in upd:
                    handle_message(upd["message"])
                elif "callback_query" in upd:
                    handle_callback(upd["callback_query"])
        except Exception as e:
            print("bridge error:", e)
            time.sleep(2)


if __name__ == "__main__":
    main()
