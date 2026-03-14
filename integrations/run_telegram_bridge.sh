#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="${1:-$SCRIPT_DIR/.env.telegram}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing env file: $ENV_FILE"
  echo "Copy $SCRIPT_DIR/.env.telegram.example -> $SCRIPT_DIR/.env.telegram and fill values."
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]]; then
  echo "TELEGRAM_BOT_TOKEN missing in $ENV_FILE"
  exit 1
fi

if [[ -z "${BOTSTORE_API:-}" ]]; then
  export BOTSTORE_API="http://127.0.0.1:8787"
fi

echo "Starting Telegram bridge..."
echo "BOTSTORE_API=$BOTSTORE_API"
python3 "$SCRIPT_DIR/telegram_bridge.py"
