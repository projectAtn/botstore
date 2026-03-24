#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = os.getenv("BOTSTORE_API", "http://127.0.0.1:8787").rstrip("/")
ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT_JSON = ROOT / 'research' / 'cryptographic-smoke-report.json'
OUT_MD = ROOT / 'research' / 'cryptographic-smoke-report.md'


def req(method: str, path: str, payload: dict) -> dict:
    r = urllib.request.Request(BASE + path, data=json.dumps(payload).encode('utf-8'), method=method, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main() -> int:
    ts = str(time.time_ns())
    slug = f'crypto-smoke-{ts}'
    cap = f'crypto.cap.{ts}'

    creator = req('POST', '/creators', {'name': f'Crypto Smoke {ts}', 'verification': 'verified', 'trust_score': 0.9})
    pack = req('POST', '/packs', {
        'slug': slug,
        'title': 'Crypto Smoke Pack',
        'type': 'skill',
        'version': '1.0.0',
        'description': 'crypto smoke',
        'risk_level': 'medium',
        'scopes': ['log.read'],
        'creator_id': creator['id'],
    })
    pv = req('POST', f"/packs/{pack['id']}/versions", {
        'semver': '1.0.1',
        'manifest_version': 'v2',
        'capabilities_declared': [cap],
        'scopes_requested': ['log.read'],
        'actions_supported': ['inspect.status'],
        'compatible_runtimes': ['openclaw'],
        'policy_requirements': {'runtime_band_max': 'B'},
        'verification_tier': 'tier2_verified'
    })
    req('PUT', f"/packs/{pack['id']}/versions/{pv['id']}/trust", {
        'artifact_uri': f'oci://botstore/{slug}:1.0.1',
        'signature_refs': [f'sig://local/{slug}'],
        'sbom_ref': f'sbom://local/{slug}.spdx.json',
        'attestation_refs': [f'att://build/{slug}', f'att://verify/{slug}', f'att://conformance/{slug}', f'att://qa/{slug}', f'att://prov/{slug}']
    })

    install_before = req('POST', '/agent/install-by-capability-v2', {
        'task_id': f'crypto-before-{ts}',
        'tenant_id': 'default',
        'user_id': 'telegram:crypto-smoke',
        'agent_id': 'agent-crypto-smoke',
        'runtime_id': 'openclaw',
        'runtime_version': '0.2.0',
        'runtime_band': 'B',
        'required_capabilities': [cap]
    })

    cosign_available = shutil.which('cosign') is not None
    verify_crypto = req('POST', f"/packs/{pack['id']}/versions/{pv['id']}/trust/verify-crypto", {})

    install_after = req('POST', '/agent/install-by-capability-v2', {
        'task_id': f'crypto-after-{ts}',
        'tenant_id': 'default',
        'user_id': 'telegram:crypto-smoke',
        'agent_id': 'agent-crypto-smoke',
        'runtime_id': 'openclaw',
        'runtime_version': '0.2.0',
        'runtime_band': 'B',
        'required_capabilities': [cap]
    })

    report = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'base_url': BASE,
        'cosign_available': cosign_available,
        'install_before': install_before,
        'verify_crypto': verify_crypto,
        'install_after': install_after,
        'notes': [
            'In production mode, install admission should require successful cryptographic receipt.',
            'When cosign is unavailable, verify-crypto is expected to fail closed.'
        ]
    }
    OUT_JSON.write_text(json.dumps(report, indent=2))
    OUT_MD.write_text('\n'.join([
        '# Cryptographic Smoke Report',
        '',
        f"- Generated: {report['generated_at']}",
        f"- cosign available: {cosign_available}",
        f"- verify-crypto ok: {bool(verify_crypto.get('ok'))}",
        f"- install before ok: {bool(install_before.get('ok'))}",
        f"- install after ok: {bool(install_after.get('ok'))}",
    ]) + '\n')
    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
