# BotStore Manifest + Adapter Contract v1

Date: 2026-03-18
Status: Draft for implementation

## Goal
Make BotStore installable by any autonomous agent runtime (OpenClaw + others) via one normalized contract.

---

## 1) BotStore Pack Manifest (runtime-neutral)

```json
{
  "manifest_version": "1.0",
  "pack": {
    "id": "pack_123",
    "slug": "incident-security-response-team",
    "title": "Incident Security Response Team",
    "type": "team",
    "version": "0.1.0",
    "description": "Incident triage + containment + compliance communication",
    "risk_level": "high",
    "scopes": ["audit.log.read", "audit.log.write", "risk.evaluate", "message.send"],
    "creator": {
      "id": "creator_22",
      "name": "Ops Foundry",
      "verification": "verified",
      "trust_score": 0.93
    },
    "qa": {
      "status": "pass",
      "suite": "team-high-pressure-v3",
      "updated_at": "2026-03-18T12:45:00Z",
      "must_pass_policy": {
        "required": 10,
        "passed": 10
      }
    }
  },
  "composition": {
    "shared_skills": ["security-alert-triager", "deploy-rollback-guardian"],
    "roles": [
      {
        "role": "Head of Security Ops",
        "personality_slug": "forensic-analyst-persona",
        "owned_skills": ["incident-triage-commander"],
        "deliverables": ["incident-timeline", "containment-plan"]
      }
    ],
    "orchestration": {
      "handoff_order": ["Head of Security Ops", "SRE Lead", "Policy Officer"],
      "approval_gates": ["security", "compliance"],
      "conflict_policy": "Containment-first; compliance signoff before closure"
    }
  },
  "integrity": {
    "standalone_skill_only": true,
    "missing_skills": [],
    "non_skill_refs": []
  },
  "compatibility": {
    "openclaw": {"supported": true, "min_version": "0.2.0"},
    "crewai": {"supported": true, "min_version": "0.9.0"},
    "langgraph": {"supported": true, "min_version": "0.2.0"},
    "autogen": {"supported": false, "notes": "adapter pending"}
  },
  "signing": {
    "signed": false,
    "sig_alg": "ed25519",
    "signature": null,
    "provenance": {
      "source": "botstore",
      "build_id": "ci-20260318-001"
    }
  }
}
```

---

## 2) Adapter Contract (runtime-facing)

Each adapter must implement these operations:

1. `resolve(manifest)`
   - Validate compatibility and required runtime capabilities.
2. `install(manifest, target)`
   - Install packs/skills/teams in runtime-native format.
3. `validate(manifest, target)`
   - Dry-run preflight with actionable errors.
4. `rollback(install_id)`
   - Revert last install if runtime supports rollback.
5. `status(install_id)`
   - Return runtime installation state.
6. `outcome(report)`
   - Post success/failure and telemetry back to BotStore.

### Standard adapter response shape

```json
{
  "ok": true,
  "runtime": "openclaw",
  "operation": "install",
  "install_id": "rt_987",
  "status": "installed",
  "warnings": [],
  "errors": []
}
```

---

## 3) Required APIs in BotStore

- `GET /manifest/{slug}`
- `POST /adapter/{runtime}/resolve`
- `POST /adapter/{runtime}/install`
- `POST /adapter/{runtime}/validate`
- `POST /adapter/{runtime}/rollback`
- `GET /adapter/{runtime}/status/{install_id}`
- `POST /adapter/{runtime}/outcome`

---

## 4) Rollout sequence

1. Ship OpenClaw adapter first (native path).
2. Ship CrewAI adapter second (highest external ROI).
3. Add LangGraph adapter third.
4. Gate each adapter by regression + trust/QA checks.

---

## 5) Acceptance criteria

- Same pack manifest installs in >=2 runtimes with no manual edits.
- Adapter preflight catches missing capabilities before install.
- Outcome telemetry returns to BotStore and updates trust/QA analytics.
