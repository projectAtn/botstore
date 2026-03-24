#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BOTSTORE_API:-http://127.0.0.1:8787}"
BUNDLE_ID="${1:-default}"

curl -fsS -X POST "$BASE_URL/policy/bundles/$BUNDLE_ID/rollback" | python3 -m json.tool
