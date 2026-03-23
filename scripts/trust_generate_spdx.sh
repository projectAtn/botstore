#!/usr/bin/env bash
set -euo pipefail

# Minimal SPDX JSON generator for artifact metadata (placeholder for full sbom tooling)
# Usage: trust_generate_spdx.sh <name> <version> <out-file>
NAME="${1:-}"
VERSION="${2:-}"
OUT="${3:-}"

if [[ -z "$NAME" || -z "$VERSION" || -z "$OUT" ]]; then
  echo "usage: $0 <name> <version> <out-file>" >&2
  exit 2
fi

cat > "$OUT" <<JSON
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "SPDXID": "SPDXRef-DOCUMENT",
  "name": "${NAME}-sbom",
  "documentNamespace": "https://botstore.local/spdx/${NAME}/${VERSION}",
  "creationInfo": {
    "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "creators": ["Tool: botstore-trust-generate-spdx"]
  },
  "packages": [
    {
      "name": "${NAME}",
      "SPDXID": "SPDXRef-Package-${NAME}",
      "versionInfo": "${VERSION}",
      "downloadLocation": "NOASSERTION",
      "filesAnalyzed": false,
      "licenseConcluded": "NOASSERTION",
      "licenseDeclared": "NOASSERTION"
    }
  ]
}
JSON

echo "Wrote $OUT"
