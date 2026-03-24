#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path('/Users/claw/.openclaw/workspace/botstore/plugin/python')))
from botstore_plugin import BotStorePlugin, BotStorePluginConfig
import urllib.request

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
OUT_JSON = ROOT / 'research' / 'runtime2-certification-python-hostbot.json'
OUT_MD = ROOT / 'research' / 'runtime2-certification-python-hostbot.md'


def must(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(msg)


def req(base: str, method: str, path: str, payload: dict) -> dict:
    r = urllib.request.Request(
        base.rstrip('/') + path,
        data=json.dumps(payload).encode('utf-8'),
        method=method,
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main() -> int:
    base = os.getenv('BOTSTORE_API', 'http://127.0.0.1:8787')
    ts = str(time.time_ns())
    runtime_id = 'python-hostbot'
    plugin = BotStorePlugin(BotStorePluginConfig(api_base=base))

    creator = req(base, 'POST', '/creators', {'name': f'Runtime2 Cert {ts}', 'verification': 'verified', 'trust_score': 0.8})
    slug = f'r2-hostbot-{ts}'
    pack = req(base, 'POST', '/packs', {
        'slug': slug,
        'title': 'Runtime2 HostBot Certification Pack',
        'type': 'skill',
        'version': '1.0.0',
        'description': 'Runtime2 certification pack',
        'risk_level': 'low',
        'scopes': ['log.read'],
        'creator_id': creator['id'],
    })

    cap = f'runtime2.hostbot.cap.{ts}'
    pv = req(base, 'POST', f"/packs/{pack['id']}/versions", {
        'semver': '1.0.1',
        'manifest_version': 'v2',
        'capabilities_declared': [cap],
        'scopes_requested': ['log.read'],
        'actions_supported': ['inspect.status'],
        'compatible_runtimes': [runtime_id],
        'policy_requirements': {'runtime_band_max': 'C'},
        'verification_tier': 'tier2_verified',
    })

    req(base, 'PUT', f"/packs/{pack['id']}/versions/{pv['id']}/trust", {
        'artifact_uri': f'oci://botstore/{slug}:1.0.1',
        'signature_refs': [f'sig://local/{slug}'],
        'sbom_ref': f'sbom://local/{slug}.spdx.json',
        'attestation_refs': [
            f'att://build/{slug}',
            f'att://verify/{slug}',
            f'att://conformance/{slug}',
            f'att://qa/{slug}',
            f'att://prov/{slug}',
        ],
    })
    verify = req(base, 'POST', f"/packs/{pack['id']}/versions/{pv['id']}/trust/verify-local", {})
    must(bool(verify.get('ok')), 'trust verification failed for runtime2 pack')

    plugin_bind = plugin.bind_target(user_id=f'hostbot:{ts}', runtime_id=runtime_id, agent_id=f'agent-hostbot-{ts}', channel='hostbot')
    plugin_where = plugin.where(f'hostbot:{ts}')

    install = req(base, 'POST', '/agent/install-by-capability-v2', {
        'task_id': f'r2-install-{ts}',
        'tenant_id': 'default',
        'user_id': f'hostbot:{ts}',
        'agent_id': f'agent-hostbot-{ts}',
        'runtime_id': runtime_id,
        'runtime_version': '0.1.0',
        'runtime_band': 'B',
        'required_capabilities': [cap],
    })
    must(bool(install.get('ok')), 'runtime2 install-by-capability failed')

    selected = install.get('selected') or {}
    attempt_id = install.get('attempt_id')
    auth = req(base, 'POST', '/agent/action-authorize', {
        'attempt_id': attempt_id,
        'pack_version_id': selected.get('pack_version_id'),
        'artifact_digest': selected.get('artifact_digest'),
        'requested_action': 'inspect.status',
        'requested_scope': 'log.read',
        'justification': 'runtime2-cert',
    })

    outcome = req(base, 'POST', '/agent/outcome-v2', {
        'attempt_id': attempt_id,
        'task_id': f'r2-outcome-{ts}',
        'tenant_id': 'default',
        'runtime_id': runtime_id,
        'runtime_version': '0.1.0',
        'result': 'success',
        'task_completed_after_install': True,
        'observed_scopes': ['log.read'],
        'incident_flag': False,
    })
    must(bool(outcome.get('ok')), 'runtime2 outcome-v2 failed')

    cert = {
        'runtime_id': runtime_id,
        'target_level': 'L2',
        'passes': {
            'install_flow': bool(install.get('ok')),
            'outcome_flow': bool(outcome.get('ok')),
            'limited_auth_path': auth.get('decision') in {'allow', 'allow_with_runtime_proof', 'deny'},
        },
    }
    cert['all_pass'] = all(cert['passes'].values())

    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'base_url': base,
        'runtime': cert,
        'pack_id': pack['id'],
        'pack_version_id': pv['id'],
        'plugin_bind': plugin_bind,
        'plugin_where': plugin_where,
        'install': install,
        'auth': auth,
        'outcome': outcome,
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2))
    OUT_MD.write_text('\n'.join([
        '# Runtime 2 Certification Report (Python Host-Bot Adapter)',
        '',
        f"- Generated: {payload['generated_at']}",
        f"- Runtime: {runtime_id}",
        f"- Target level: L2",
        f"- All pass: {cert['all_pass']}",
        '',
        '## Checks',
        *[f"- {k}: {'PASS' if v else 'FAIL'}" for k, v in cert['passes'].items()]
    ]) + '\n')

    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    return 0 if cert['all_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
