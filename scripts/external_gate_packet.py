#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path('/Users/claw/.openclaw/workspace/botstore')
R = ROOT / 'research'
OUT = R / 'external-rollout-checklist.json'
HEARTBEAT_MAX_AGE_HOURS = 2


@dataclass
class GateResult:
    key: str
    required: bool
    pass_status: bool
    evidence: list[str]
    missing: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            'key': self.key,
            'required': self.required,
            'pass': self.pass_status,
            'evidence': self.evidence,
            'missing': self.missing,
        }


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def pick_latest(pattern: str) -> Path | None:
    matches = sorted(R.glob(pattern), key=lambda p: p.stat().st_mtime)
    return matches[-1] if matches else None


def pick_first(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.exists():
            return p
    return None


def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except Exception:
        return None


def flatten_strings(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, list):
        for item in value:
            out.extend(flatten_strings(item))
    elif isinstance(value, dict):
        for v in value.values():
            out.extend(flatten_strings(v))
    return out


def has_unpinned_placeholders(strings: list[str]) -> bool:
    return any('<' in s or '>' in s for s in strings)


def has_wildcards(strings: list[str]) -> bool:
    return any('*' in s for s in strings)


def gate_packet() -> dict[str, Any]:
    launch_scorecard_path = pick_latest('launch-scorecard-*.json')
    conformance_path = R / 'openclaw-conformance-result.json'
    trust_smoke_path = pick_first([
        R / 'cryptographic-smoke-report.json',
        R / 'trust-chain-smoke-result.json',
    ])
    trust_negative_path = pick_first([
        R / 'cryptographic-negative-matrix-report.json',
        R / 'trust-chain-negative-matrix-result.json',
    ])
    alert_test_path = R / 'alert-test-report.json'
    phase_gate_path = R / 'phase-gate-summary.json'
    trust_policy_path = R / 'trust_policy_v1.json'
    trust_prod_template_path = R / 'trust_policy_production_template.json'
    heartbeat_path = R / 'heartbeat.json'
    canary_week_report_path = pick_first([
        R / 'canary-week-report.json',
        R / 'canary-week-report.md',
    ])

    launch = load_json(launch_scorecard_path) if launch_scorecard_path else {}
    conformance = load_json(conformance_path)
    trust_smoke = load_json(trust_smoke_path) if trust_smoke_path else {}
    trust_negative = load_json(trust_negative_path) if trust_negative_path else {}
    alert_test = load_json(alert_test_path)
    phase_gate = load_json(phase_gate_path)
    trust_policy = load_json(trust_policy_path)
    trust_prod_template = load_json(trust_prod_template_path)
    heartbeat = load_json(heartbeat_path)

    checks: list[GateResult] = []

    # 1) Trust production mode
    trust_mode = str(trust_policy.get('mode', '')).lower()
    checks.append(GateResult(
        key='trust_production_mode',
        required=True,
        pass_status=trust_mode == 'production',
        evidence=[f"trust_policy.mode={trust_mode or 'missing'}"],
        missing=[] if trust_mode == 'production' else ['Set research/trust_policy_v1.json mode to production for external rollout.'],
    ))

    # 2) Exact pins (strict identities; no placeholders/wildcards)
    authorities = trust_prod_template.get('authorities', [])
    required_atts = trust_prod_template.get('required_attestations', [])
    pin_strings = flatten_strings(authorities) + flatten_strings(required_atts)
    has_placeholders = has_unpinned_placeholders(pin_strings)
    has_star = has_wildcards(pin_strings)
    has_exact_ref = all('@refs/heads/' in s for s in pin_strings if 'github.com/' in s and '/.github/workflows/' in s)
    exact_pins_ok = bool(pin_strings) and not has_placeholders and not has_star and has_exact_ref
    checks.append(GateResult(
        key='exact_identity_pins',
        required=True,
        pass_status=exact_pins_ok,
        evidence=[
            f'pin_string_count={len(pin_strings)}',
            f'contains_placeholders={has_placeholders}',
            f'contains_wildcards={has_star}',
            f'exact_ref_pins={has_exact_ref}',
        ],
        missing=[] if exact_pins_ok else [
            'Replace <ORG>/<REPO> placeholders and wildcard patterns with exact workflow identities pinned to refs/heads/main.',
        ],
    ))

    # 3) Attestation enforcement
    neg_results = trust_negative.get('results', []) if isinstance(trust_negative.get('results'), list) else []
    has_missing_att_case = any('att' in str((row or {}).get('case', '')).lower() for row in neg_results)
    missing_att_case_pass = any('att' in str((row or {}).get('case', '')).lower() and bool((row or {}).get('pass')) for row in neg_results)
    atts_declared = isinstance(required_atts, list) and len(required_atts) >= 1
    attestation_ok = atts_declared and bool(trust_negative.get('all_pass')) and has_missing_att_case and missing_att_case_pass
    checks.append(GateResult(
        key='attestation_enforced',
        required=True,
        pass_status=attestation_ok,
        evidence=[
            f'required_attestation_count={len(required_atts) if isinstance(required_atts, list) else 0}',
            f'trust_negative_all_pass={bool(trust_negative.get("all_pass"))}',
            f'missing_attestation_case_present={has_missing_att_case}',
            f'missing_attestation_case_pass={missing_att_case_pass}',
        ],
        missing=[] if attestation_ok else [
            'Require attestation predicates in production template and keep failing negative attestation matrix passing.',
        ],
    ))

    # 4) No scope widening
    launch_checks = launch.get('checks', {}) if isinstance(launch.get('checks'), dict) else {}
    conf_checks = conformance.get('checks', {}) if isinstance(conformance.get('checks'), dict) else {}
    no_scope_widening_ok = bool(launch_checks.get('typed_action_map_ok')) and bool(launch_checks.get('auth_bypass_check_ok')) and bool((conf_checks.get('typed_action_map') or {}).get('all_pass')) and bool((conf_checks.get('auth_bypass_check') or {}).get('all_pass'))
    checks.append(GateResult(
        key='no_scope_widening',
        required=True,
        pass_status=no_scope_widening_ok,
        evidence=[
            f"launch.typed_action_map_ok={bool(launch_checks.get('typed_action_map_ok'))}",
            f"launch.auth_bypass_check_ok={bool(launch_checks.get('auth_bypass_check_ok'))}",
            f"conformance.typed_action_map.all_pass={bool((conf_checks.get('typed_action_map') or {}).get('all_pass'))}",
            f"conformance.auth_bypass_check.all_pass={bool((conf_checks.get('auth_bypass_check') or {}).get('all_pass'))}",
        ],
        missing=[] if no_scope_widening_ok else [
            'Typed action-map and auth-bypass checks must pass in both launch scorecard and conformance artifacts.',
        ],
    ))

    # 5) Conformance
    conformance_ok = bool((conf_checks.get('health') or {}).get('ok')) and bool((conf_checks.get('typed_action_map') or {}).get('all_pass')) and bool((conf_checks.get('auth_bypass_check') or {}).get('all_pass'))
    checks.append(GateResult(
        key='conformance_green',
        required=True,
        pass_status=conformance_ok,
        evidence=[
            f"health.ok={bool((conf_checks.get('health') or {}).get('ok'))}",
            f"typed_action_map.all_pass={bool((conf_checks.get('typed_action_map') or {}).get('all_pass'))}",
            f"auth_bypass_check.all_pass={bool((conf_checks.get('auth_bypass_check') or {}).get('all_pass'))}",
        ],
        missing=[] if conformance_ok else ['Conformance report must be green (health + typed map + auth-bypass).'],
    ))

    # 6) Alerts
    alerts_ok = bool(alert_test.get('all_pass'))
    checks.append(GateResult(
        key='alerts_green',
        required=True,
        pass_status=alerts_ok,
        evidence=[f"alert_test.all_pass={alerts_ok}"],
        missing=[] if alerts_ok else ['Monitoring alert tests must pass before external rollout.'],
    ))

    # 7) Heartbeat freshness
    hb_ts = parse_iso(heartbeat.get('generated_at'))
    now = datetime.now(timezone.utc)
    hb_age = (now - hb_ts) if hb_ts else None
    hb_fresh_ok = bool(hb_age is not None and hb_age <= timedelta(hours=HEARTBEAT_MAX_AGE_HOURS))
    checks.append(GateResult(
        key='heartbeat_fresh',
        required=True,
        pass_status=hb_fresh_ok,
        evidence=[
            f"heartbeat.generated_at={heartbeat.get('generated_at')}",
            f"heartbeat.age_minutes={(hb_age.total_seconds() / 60.0) if hb_age else 'missing'}",
            f'heartbeat.max_age_hours={HEARTBEAT_MAX_AGE_HOURS}',
        ],
        missing=[] if hb_fresh_ok else [
            f'Heartbeat must be refreshed within {HEARTBEAT_MAX_AGE_HOURS} hours of gate decision.',
        ],
    ))

    # 8) 7-day canary complete
    canary_json_path = R / 'canary-week-report.json'
    canary_json = load_json(canary_json_path) if canary_json_path.exists() else {}
    days_observed = int(canary_json.get('days_observed', 0) or 0)
    canary_go = str(canary_json.get('go_nogo', '')).upper() == 'GO'
    canary_incidents_clear = int(canary_json.get('open_incidents', 0) or 0) == 0
    canary_ok = canary_json_path.exists() and days_observed >= 7 and canary_go and canary_incidents_clear
    checks.append(GateResult(
        key='canary_7_day_complete',
        required=True,
        pass_status=canary_ok,
        evidence=[
            f'canary_report_path={canary_json_path if canary_json_path.exists() else "missing"}',
            f'days_observed={days_observed}',
            f'go_nogo={canary_json.get("go_nogo", "missing")}',
            f'open_incidents={canary_json.get("open_incidents", "missing")}',
        ],
        missing=[] if canary_ok else [
            'Provide research/canary-week-report.json with >=7 days observed, GO decision, and open_incidents=0.',
        ],
    ))

    # Supporting artifact from phase gate summary
    phase_go = str(phase_gate.get('go_nogo', '')).upper() == 'GO'
    checks.append(GateResult(
        key='phase_gate_summary_go',
        required=True,
        pass_status=phase_go,
        evidence=[f"phase_gate.go_nogo={phase_gate.get('go_nogo', 'missing')}"],
        missing=[] if phase_go else ['Phase gate summary must be GO.'],
    ))

    missing_required = [
        {'key': c.key, 'missing': c.missing}
        for c in checks
        if c.required and not c.pass_status
    ]

    packet = {
        'generated_at': now.isoformat(),
        'go_nogo': 'GO' if not missing_required else 'NO_GO',
        'summary': {
            'required_total': sum(1 for c in checks if c.required),
            'required_pass': sum(1 for c in checks if c.required and c.pass_status),
            'required_fail': len(missing_required),
        },
        'sources': {
            'launch_scorecard': str(launch_scorecard_path) if launch_scorecard_path else None,
            'conformance': str(conformance_path) if conformance_path.exists() else None,
            'trust_smoke': str(trust_smoke_path) if trust_smoke_path else None,
            'trust_negative': str(trust_negative_path) if trust_negative_path else None,
            'alert_test': str(alert_test_path) if alert_test_path.exists() else None,
            'phase_gate_summary': str(phase_gate_path) if phase_gate_path.exists() else None,
            'trust_policy': str(trust_policy_path) if trust_policy_path.exists() else None,
            'trust_policy_production_template': str(trust_prod_template_path) if trust_prod_template_path.exists() else None,
            'heartbeat': str(heartbeat_path) if heartbeat_path.exists() else None,
            'canary_week_report': str(canary_week_report_path) if canary_week_report_path else None,
        },
        'checks': [c.as_dict() for c in checks],
        'missing_required_items': missing_required,
    }

    return packet


def main() -> int:
    packet = gate_packet()
    OUT.write_text(json.dumps(packet, indent=2) + '\n')
    print(f'Wrote {OUT}')
    print(f"Decision: {packet['go_nogo']} ({packet['summary']['required_pass']}/{packet['summary']['required_total']})")
    return 0 if packet['go_nogo'] == 'GO' else 1


if __name__ == '__main__':
    raise SystemExit(main())
