#!/usr/bin/env bash
set -euo pipefail

# Usage: trust_cosign_verify.sh <artifact-uri>
ARTIFACT_URI="${1:-}"
if [[ -z "$ARTIFACT_URI" ]]; then
  echo "usage: $0 <artifact-uri>" >&2
  exit 2
fi

if ! command -v cosign >/dev/null 2>&1; then
  echo "cosign not found; install cosign for trust-chain verification" >&2
  exit 127
fi

cosign verify "$ARTIFACT_URI"
