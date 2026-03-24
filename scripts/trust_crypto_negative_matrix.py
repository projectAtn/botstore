#!/usr/bin/env python3
from __future__ import annotations

import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = 'http://127.0.0.1:8787'
ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT_JSON = ROOT / 'research' / 'cryptographic-negative-matrix-report.json'
OUT_MD = ROOT / 'research' / 'cryptographic-negative-matrix-report.md'


def req(method: str, path: str, payload: dict) -> dict:
    r = urllib.request.Request(BASE + path, data=json.dumps(payload).encode('utf-8'), method=method, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main() -> int:
    ts = str(time.time_ns())
    creator = req('POST', '/creators', {'name': f'Crypto Neg {ts}', 'verification': 'verified', 'trust_score': 0.9})

    cases = [
        ('missing_sig', {'signature_refs': []}),
        ('missing_att', {'attestation_refs': []}),
    ]

    results = []
    for idx, (name, mutate) in enumerate(cases, start=1):
        slug = f'crypto-neg-{ts}-{idx}'
        cap = f'crypto.neg.cap.{ts}.{idx}'
        pack = req('POST', '/packs', {
            'slug': slug,
            'title': f'Crypto Neg {idx}',
            'type': 'skill',
            'version': '1.0.0',
            'description': 'crypto neg',
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
        payload = {
            'artifact_uri': f'oci://botstore/{slug}:1.0.1',
            'signature_refs': [f'sig://local/{slug}'],
            'sbom_ref': f'sbom://local/{slug}.spdx.json',
            'attestation_refs': [f'att://build/{slug}', f'att://verify/{slug}', f'att://conformance/{slug}', f'att://qa/{slug}', f'att://prov/{slug}']
        }
        payload.update(mutate)
        req('PUT', f"/packs/{pack['id']}/versions/{pv['id']}/trust", payload)
        vr = req('POST', f"/packs/{pack['id']}/versions/{pv['id']}/trust/verify-crypto", {})
        results.append({'case': name, 'verify_crypto': vr, 'pass': vr.get('ok') is False})

    all_pass = all(r['pass'] for r in results)
    out = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'all_pass': all_pass,
        'results': results,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2))
    OUT_MD.write_text('\n'.join([
        '# Cryptographic Negative Matrix',
        '',
        f"- Generated: {out['generated_at']}",
        f"- All pass: {all_pass}",
        '',
        '## Cases',
        *[f"- {r['case']}: {'PASS' if r['pass'] else 'FAIL'}" for r in results]
    ]) + '\n')
    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0 if all_pass else 1


if __name__ == '__main__':
    raise SystemExit(main())
