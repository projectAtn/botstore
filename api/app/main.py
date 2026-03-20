import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from enum import Enum
from typing import Optional, Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Field, SQLModel, Session, create_engine, select


class PackType(str, Enum):
    personality = "personality"
    skill = "skill"
    bundle = "bundle"


class InstallStatus(str, Enum):
    pending_approval = "pending_approval"
    installed = "installed"
    denied = "denied"
    rolled_back = "rolled_back"


class VerificationStatus(str, Enum):
    unverified = "unverified"
    verified = "verified"


class ApprovalStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class RuntimeBand(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class InstallAttemptStatus(str, Enum):
    gap_detected = "gap_detected"
    candidate_set_ready = "candidate_set_ready"
    policy_decided = "policy_decided"
    approval_required = "approval_required"
    approval_granted = "approval_granted"
    artifact_verified = "artifact_verified"
    installed = "installed"
    activated = "activated"
    rolled_back = "rolled_back"
    outcome_reported = "outcome_reported"
    denied = "denied"
    failed = "failed"


SENSITIVE_SCOPES = {
    "email.send",
    "message.send",
    "social.post",
    "payment.charge",
    "files.delete",
}

POLICY_REASON_CODES = {
    "RUNTIME_BAND_TOO_WEAK": "runtime_band_too_weak",
    "SENSITIVE_OR_LOW_VERIFICATION": "sensitive_or_low_verification",
    "LOW_RISK_CONTEXT": "low_risk_context",
    "APPROVAL_GRANT_ISSUED": "approval_grant_issued",
}


class Creator(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    verification: VerificationStatus = VerificationStatus.unverified
    trust_score: float = 0.5


class CreatorCreate(SQLModel):
    name: str
    verification: VerificationStatus = VerificationStatus.unverified
    trust_score: float = 0.5


class SkillImportRequest(BaseModel):
    skill_path: str
    creator_id: Optional[int] = None
    pack_type: PackType = PackType.skill


class SkillExportRequest(BaseModel):
    slug: str
    out_dir: str


class TeamRoleInput(BaseModel):
    role: str
    personality_slug: str
    owned_skills: list[str] = []
    deliverables: list[str] = []


class TeamComposeRequest(BaseModel):
    name: str
    objective: str
    role_slugs: list[str]
    risk_level: str = "medium"
    additional_shared_skills: list[str] = []


class TeamValidateRequest(BaseModel):
    team: dict[str, Any]
    required_capabilities: list[str] = []
    required_roles: list[str] = []
    expected_artifacts: list[str] = []


class TeamSimulateRequest(BaseModel):
    team: dict[str, Any]
    scenario_ids: list[str] = []


class TeamPublishRequest(BaseModel):
    team: dict[str, Any]
    creator_id: Optional[int] = None


class Pack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    title: str
    type: PackType
    version: str = "0.1.0"
    description: str
    risk_level: str = "low"
    scopes_csv: str = ""
    bundle_pack_ids_csv: str = ""
    is_featured: bool = False
    creator_id: Optional[int] = Field(default=None, foreign_key="creator.id")


class PackVersion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pack_id: int = Field(foreign_key="pack.id", index=True)
    semver: str = Field(default="0.1.0", index=True)
    manifest_version: str = "v2"
    artifact_digest: str = Field(index=True)
    verification_tier: str = "tier0_listed"
    compatible_runtimes_json: str = "[]"
    policy_requirements_json: str = "{}"
    expected_approval_friction: float = 0.0
    capabilities_declared_json: str = "[]"
    scopes_requested_json: str = "[]"
    actions_supported_json: str = "[]"
    capabilities_verified_json: str = "[]"
    scopes_observed_json: str = "[]"
    is_current: bool = True
    created_at: str = ""


class InstallAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: str = Field(index=True, unique=True)
    task_id: str = Field(index=True)
    tenant_id: str = Field(index=True)
    user_id: str = Field(index=True)
    agent_id_hash: str = Field(index=True)
    runtime_id: str = Field(index=True)
    runtime_version: Optional[str] = None
    runtime_band: RuntimeBand = RuntimeBand.D
    missing_capabilities_json: str = "[]"
    candidate_snapshot_id: str = Field(index=True)
    candidate_snapshot_json: str = "[]"
    selected_pack_version_id: Optional[int] = Field(default=None, foreign_key="packversion.id", index=True)
    policy_decision_id: Optional[int] = Field(default=None, foreign_key="policydecision.id", index=True)
    approval_grant_id: Optional[int] = Field(default=None, foreign_key="approvalgrant.id", index=True)
    install_status: str = "pending"
    activation_status: str = "pending"
    rollback_status: str = "not_requested"
    status: InstallAttemptStatus = InstallAttemptStatus.gap_detected
    created_at: str = ""
    updated_at: str = ""


class PolicyDecision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: str = Field(index=True)
    effect: str
    reason_codes_json: str = "[]"
    blocking_conditions_json: str = "[]"
    required_approvals_json: str = "[]"
    minimum_verification_tier: Optional[str] = None
    runtime_requirements_json: str = "{}"
    policy_hash: str = ""
    created_at: str = ""


class ApprovalGrant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    grant_id: str = Field(index=True, unique=True)
    attempt_id: str = Field(index=True)
    tenant_id: str = Field(index=True)
    approver_id: str = "system"
    artifact_digest: str = Field(index=True)
    pack_version_id: int = Field(foreign_key="packversion.id", index=True)
    allowed_scopes_json: str = "[]"
    allowed_actions_json: str = "[]"
    runtime_id: str = Field(index=True)
    runtime_band: RuntimeBand = RuntimeBand.D
    expires_at: str = ""
    policy_hash: str = ""
    justification: Optional[str] = None
    signature: str
    created_at: str = ""


class CandidateImpression(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: str = Field(index=True)
    candidate_snapshot_id: str = Field(index=True)
    rank: int
    pack_id: int = Field(index=True)
    pack_version_id: int = Field(index=True)
    artifact_digest: str = Field(index=True)
    score: float
    selected: bool = False
    policy_effect: str = "allow"
    policy_reason_codes_json: str = "[]"
    exploration_bucket: str = "none"
    propensity: float = 1.0
    features_json: str = "{}"
    created_at: str = ""


class ActionAuthorization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: str = Field(index=True)
    pack_version_id: int = Field(index=True)
    artifact_digest: str = Field(index=True)
    requested_action: str
    requested_scope: str
    decision: str
    reason_codes_json: str = "[]"
    grant_id: Optional[str] = None
    justification: Optional[str] = None
    runtime_attestation_hash: Optional[str] = None
    created_at: str = ""


class OutcomeReport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: str = Field(index=True)
    task_id: str = Field(index=True)
    tenant_id: str = Field(index=True)
    task_class: Optional[str] = None
    selected_pack_version_id: Optional[int] = Field(default=None, index=True)
    runtime_id: str = Field(index=True)
    runtime_version: Optional[str] = None
    result: str = "blocked"
    error_code: Optional[str] = None
    latency_ms: Optional[float] = None
    human_intervention: str = "none"
    task_completed_after_install: bool = False
    observed_scopes_json: str = "[]"
    side_effect_counts_json: str = "{}"
    incident_flag: bool = False
    recovery_action: Optional[str] = None
    confidence: Optional[float] = None
    privacy_mode: str = "standard"
    reward: float = 0.0
    created_at: str = ""


class TrustIncident(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: str = Field(index=True)
    tenant_id: str = Field(index=True)
    pack_version_id: Optional[int] = Field(default=None, index=True)
    severity: str = "high"
    incident_type: str
    details_json: str = "{}"
    quarantined: bool = False
    created_at: str = ""


class PackCreate(SQLModel):
    slug: str
    title: str
    type: PackType
    version: str = "0.1.0"
    description: str
    risk_level: str = "low"
    scopes: list[str] = []
    bundle_pack_ids: list[int] = []
    is_featured: bool = False
    creator_id: Optional[int] = None


class PackVersionCreate(SQLModel):
    semver: str = "0.1.0"
    manifest_version: str = "v2"
    capabilities_declared: list[str] = []
    scopes_requested: list[str] = []
    actions_supported: list[str] = []
    compatible_runtimes: list[str] = ["openclaw"]
    policy_requirements: dict[str, Any] = {}
    verification_tier: str = "tier0_listed"


class BundleValidateRequest(SQLModel):
    title: str = ""
    description: str = ""
    child_pack_ids: list[int] = []
    proposed_risk_level: str = "medium"


class CatalogPack(SQLModel):
    id: int
    slug: str
    title: str
    type: PackType
    version: str
    description: str
    risk_level: str
    scopes: list[str]
    bundle_pack_ids: list[int] = []
    requires_approval: bool
    is_featured: bool = False
    creator_id: Optional[int] = None
    creator_name: Optional[str] = None
    creator_verification: Optional[VerificationStatus] = None
    creator_trust_score: Optional[float] = None
    qa_status: Optional[str] = None
    qa_suite: Optional[str] = None
    qa_updated_at: Optional[str] = None
    qa_report_path: Optional[str] = None


class PackQAReport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pack_id: int = Field(foreign_key="pack.id", index=True, unique=True)
    status: str = "pending"
    suite: str = "default"
    report_path: Optional[str] = None
    summary: Optional[str] = None
    updated_at: str = ""


class PackQAUpdate(SQLModel):
    pack_id: int
    status: str
    suite: str = "default"
    report_path: Optional[str] = None
    summary: Optional[str] = None


class JobEnqueueRequest(BaseModel):
    job_type: str
    payload: dict[str, Any] = {}


class ArtifactPublishRequest(BaseModel):
    source_path: str
    artifact_name: Optional[str] = None


class Install(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    pack_id: int = Field(foreign_key="pack.id")
    version: str
    status: InstallStatus = InstallStatus.installed
    approval_required: bool = False


class InstallCreate(SQLModel):
    user_id: str
    pack_id: int
    runtime_id: Optional[str] = None
    agent_id: Optional[str] = None


class InstallResult(SQLModel):
    install: Install
    approval_id: Optional[int] = None


class Approval(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    install_id: int = Field(foreign_key="install.id")
    user_id: str = Field(index=True)
    pack_id: int = Field(foreign_key="pack.id")
    requested_action: str = "install_pack"
    status: ApprovalStatus = ApprovalStatus.pending
    decision_note: Optional[str] = None


class ApprovalDecision(SQLModel):
    approve: bool
    note: Optional[str] = None


class BundleInstallCreate(SQLModel):
    user_id: str
    pack_ids: list[int]


class BundleInstallResult(SQLModel):
    installs: list[InstallResult]


class BotCommandInstallRequest(SQLModel):
    user_id: str
    pack_slug: str


class BotCommandBundleInstallRequest(SQLModel):
    user_id: str
    bundle_slug: str


class BotCommandRequest(SQLModel):
    user_id: str
    text: str


class BotCommandResponse(SQLModel):
    ok: bool = True
    message: str
    action: str
    data: dict = {}


class BotCallbackRequest(SQLModel):
    user_id: str
    callback_data: str


class AgentSearchRequest(SQLModel):
    user_id: str
    runtime: str
    runtime_version: Optional[str] = None
    intent: str = ""
    missing_capabilities: list[str] = []
    limit: int = 10


class AgentSearchConstraints(SQLModel):
    risk_max: Optional[str] = None
    tier_min: Optional[str] = None
    latency_ms_max: Optional[int] = None


class AgentSearchQuery(SQLModel):
    user_id: str = "anonymous"
    runtime: str = "openclaw"
    runtime_version: Optional[str] = None
    query: str = ""
    missing_capabilities: list[str] = []
    constraints: Optional[AgentSearchConstraints] = None
    limit: int = 10


class AgentInstallByCapabilityRequest(SQLModel):
    user_id: str
    runtime: str
    required_capabilities: list[str]


class AgentPolicyEvaluateRequest(SQLModel):
    user_id: str
    runtime: str
    pack_id: int


class AgentPolicyEvaluateResponse(SQLModel):
    decision: str
    reason: str


class AgentOutcomeRequest(SQLModel):
    user_id: str
    task_id: str
    runtime: str
    pack_id: int
    success: bool
    latency_ms: Optional[float] = None
    error_class: Optional[str] = None


class AgentInstallByCapabilityV2Request(SQLModel):
    task_id: str
    tenant_id: str = "default"
    user_id: str
    agent_id: str
    runtime_id: str
    runtime_version: Optional[str] = None
    runtime_band: RuntimeBand = RuntimeBand.D
    required_capabilities: list[str] = []
    limit: int = 10


class AgentActionAuthorizeRequest(SQLModel):
    attempt_id: str
    pack_version_id: int
    artifact_digest: str
    requested_action: str
    requested_scope: str
    runtime_attestation: Optional[str] = None
    justification: str = ""


class AgentActionAuthorizeResponse(SQLModel):
    decision: str
    reason: str
    grant_token: Optional[str] = None
    grant_id: Optional[str] = None
    expires_at: Optional[str] = None


class AgentOutcomeV2Request(SQLModel):
    attempt_id: str
    task_id: str
    tenant_id: str = "default"
    task_class: Optional[str] = None
    runtime_id: str
    runtime_version: Optional[str] = None
    result: str = "blocked"
    error_code: Optional[str] = None
    latency_ms: Optional[float] = None
    human_intervention: str = "none"
    task_completed_after_install: bool = False
    observed_scopes: list[str] = []
    side_effect_counts: dict[str, int] = {}
    incident_flag: bool = False
    recovery_action: Optional[str] = None
    confidence: Optional[float] = None
    privacy_mode: str = "standard"


class InstallSetup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    install_id: int = Field(foreign_key="install.id", unique=True, index=True)
    gmail_connected: bool = False
    calendar_connected: bool = False
    notion_connected: bool = False
    slack_connected: bool = False


class InstallSetupUpdate(SQLModel):
    gmail_connected: bool = False
    calendar_connected: bool = False
    notion_connected: bool = False
    slack_connected: bool = False


class UserRuntimeBinding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    runtime_id: str = Field(index=True)
    agent_id: str = Field(index=True)
    channel: Optional[str] = None
    is_default: bool = False


class UserRuntimeBindingCreate(SQLModel):
    user_id: str
    runtime_id: str
    agent_id: str
    channel: Optional[str] = None
    set_default: bool = True


class InstallActivation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    install_id: int = Field(foreign_key="install.id", unique=True, index=True)
    user_id: str = Field(index=True)
    runtime_id: Optional[str] = Field(default=None, index=True)
    agent_id: Optional[str] = Field(default=None, index=True)
    status: str = "installed_registry"
    message: str = "Installed in registry only (not yet linked to a runtime target)."


class AgentOutcome(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    task_id: str = Field(index=True)
    runtime: str = Field(index=True)
    pack_id: int = Field(foreign_key="pack.id", index=True)
    success: bool
    latency_ms: Optional[float] = None
    error_class: Optional[str] = None


class OpsProgress(BaseModel):
    phase: str
    percent: int
    bar: str
    current_task: str
    next_task: str


class OpsProgressUpdate(BaseModel):
    phase: str = "execution"
    percent: int
    current_task: str = ""
    next_task: str = ""


DEFAULT_SQLITE_URL = "sqlite:///./botstore.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL).strip() or DEFAULT_SQLITE_URL

engine_kwargs = {"echo": False}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)
OPS_PROGRESS_PATH = Path("../research/ops-progress.json")
ROLE_AGENT_CATALOG_PATH = Path("../research/singular-role-agent-offerings-v1.json")
TEAM_SCENARIOS_PATH = Path("../research/team-pack-qa-scenarios-v2.json")
TEAM_PUBLISHED_PATH = Path("../research/team-published.jsonl")
JOB_QUEUE_PATH = Path(os.getenv("JOB_QUEUE_PATH", "../research/job-queue.jsonl"))
JOB_STATUS_PATH = Path(os.getenv("JOB_STATUS_PATH", "../research/job-status.json"))
ARTIFACTS_DIR = Path(os.getenv("ARTIFACTS_DIR", "../research/artifacts"))

app = FastAPI(title="BotStore API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(engine)


app.mount("/web", StaticFiles(directory="../web", html=True), name="web")


def _enforce_bot_auth(x_botstore_key: Optional[str]) -> None:
    required = os.getenv("BOTSTORE_BOT_KEY", "").strip()
    if required and x_botstore_key != required:
        raise HTTPException(
            status_code=401,
            detail="unauthorized bot key (set X-Botstore-Key header to the configured BOTSTORE_BOT_KEY)",
        )


def _scopes_to_csv(scopes: list[str]) -> str:
    return ",".join(sorted({s.strip() for s in scopes if s.strip()}))


def _csv_to_scopes(scopes_csv: str) -> list[str]:
    if not scopes_csv:
        return []
    return [s.strip() for s in scopes_csv.split(",") if s.strip()]


def _csv_to_ints(values_csv: str) -> list[int]:
    if not values_csv:
        return []
    out: list[int] = []
    for raw in values_csv.split(","):
        raw = raw.strip()
        if not raw:
            continue
        if raw.isdigit():
            out.append(int(raw))
    return out


def _json_list(value: Any) -> list:
    if isinstance(value, list):
        return value
    if not value:
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []


def _json_obj(value: Any) -> dict:
    if isinstance(value, dict):
        return value
    if not value:
        return {}
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _runtime_band_rank(band: RuntimeBand | str) -> int:
    b = str(band)
    return {"A": 1, "B": 2, "C": 3, "D": 4}.get(b, 4)


def _policy_sign(payload: dict) -> str:
    secret = os.getenv("BOTSTORE_POLICY_SIGNING_KEY", "dev-insecure-signing-key")
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    sig = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).decode("utf-8").rstrip("=")


def _make_policy_hash(payload: dict) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def _ints_to_csv(values: list[int]) -> str:
    uniq = sorted({int(v) for v in values if int(v) > 0})
    return ",".join(str(v) for v in uniq)


def _norm_token(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def _load_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_job_status() -> dict[str, Any]:
    data = _load_json(JOB_STATUS_PATH)
    return data if isinstance(data, dict) else {}


def _save_job_status(data: dict[str, Any]) -> None:
    JOB_STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    JOB_STATUS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _append_job_queue(entry: dict[str, Any]) -> None:
    JOB_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JOB_QUEUE_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def _team_skill_slugs(team: dict[str, Any]) -> list[str]:
    slugs: list[str] = []
    for s in team.get("shared_skills", []) or []:
        if isinstance(s, str) and s.strip():
            slugs.append(s.strip())
    for role in team.get("roles", []) or []:
        for s in role.get("owned_skills", []) or []:
            if isinstance(s, str) and s.strip():
                slugs.append(s.strip())
    return sorted(set(slugs))


def _team_skill_integrity(team: dict[str, Any]) -> dict:
    requested = _team_skill_slugs(team)
    valid_skill_slugs: list[str] = []
    missing_skills: list[str] = []
    non_skill_refs: list[dict[str, str]] = []

    with Session(engine) as session:
        for slug in requested:
            p = session.exec(select(Pack).where(Pack.slug == slug)).first()
            if not p:
                missing_skills.append(slug)
                continue
            if p.type != PackType.skill:
                non_skill_refs.append({"slug": slug, "type": str(p.type)})
                continue
            valid_skill_slugs.append(slug)

    return {
        "requested": requested,
        "valid_skill_slugs": sorted(set(valid_skill_slugs)),
        "missing_skills": sorted(set(missing_skills)),
        "non_skill_refs": non_skill_refs,
    }


def _team_eval(team: dict[str, Any], req_caps: list[str], req_roles: list[str], req_artifacts: list[str]) -> dict:
    req_caps_set = {c.strip() for c in req_caps if c.strip()}
    req_roles_set = {_norm_token(r) for r in req_roles if r}
    req_art_set = {_norm_token(a) for a in req_artifacts if a}

    role_names = {_norm_token((r or {}).get("role", "")) for r in (team.get("roles", []) or [])}
    artifacts = set()
    for r in team.get("roles", []) or []:
        for d in (r.get("deliverables", []) or []):
            artifacts.add(_norm_token(str(d)))

    integrity = _team_skill_integrity(team)

    with Session(engine) as session:
        caps = set()
        for slug in integrity["valid_skill_slugs"]:
            p = session.exec(select(Pack).where(Pack.slug == slug)).first()
            if p:
                caps.update(_csv_to_scopes(p.scopes_csv))

    cap_cov = len(caps.intersection(req_caps_set)) / max(len(req_caps_set), 1) if req_caps_set else 1.0
    role_cov = len(role_names.intersection(req_roles_set)) / max(len(req_roles_set), 1) if req_roles_set else 1.0
    art_cov = len(artifacts.intersection(req_art_set)) / max(len(req_art_set), 1) if req_art_set else 1.0
    score = round((0.5 * cap_cov) + (0.3 * role_cov) + (0.2 * art_cov), 3)

    return {
        "score": score,
        "capability_coverage": round(cap_cov, 3),
        "role_coverage": round(role_cov, 3),
        "artifact_coverage": round(art_cov, 3),
        "missing_capabilities": sorted(req_caps_set - caps),
        "missing_roles": sorted(req_roles_set - role_names),
        "missing_artifacts": sorted(req_art_set - artifacts),
        "pass": score >= 0.8,
        "integrity": integrity,
    }


def _requires_approval(pack: Pack) -> bool:
    scopes = set(_csv_to_scopes(pack.scopes_csv))
    return pack.risk_level.lower() == "high" or bool(scopes.intersection(SENSITIVE_SCOPES))


SEARCH_SYNONYMS = {
    "schedule": ["calendar", "meeting", "timezone"],
    "email": ["inbox", "mail", "reply", "triage"],
    "research": ["source", "citation", "web", "verify", "writing"],
    "compliance": ["policy", "audit", "risk", "governance", "enforce"],
    "coding": ["code", "repo", "pr", "debug"],
    "support": ["ticket", "helpdesk", "customer"],
    "cost": ["budget", "spend", "finops"],
    "seo": ["search", "content", "ranking", "optimize"],
    "campaign": ["marketing", "orchestration", "conversion", "growth"],
    "repurpose": ["rewrite", "transform", "content", "distribution"],
    "creator": ["content", "audience", "publish", "social"],
}


CAPABILITY_ALIASES = {
    "audit.log.read": ["files.read", "web.fetch"],
    "audit.log.write": ["files.write"],
    "policy.enforce": ["message.send", "email.send"],
    "risk.evaluate": ["memory.read", "memory.write"],
    "marketing.seo": ["web.search", "web.fetch"],
    "marketing.content_repurpose": ["files.write", "web.fetch"],
    "marketing.campaign_orchestration": ["message.send", "email.send", "calendar.write"],
    "marketing.analytics": ["files.read", "memory.read"],
}


def _tokenize(text: str) -> set[str]:
    norm = "".join(ch.lower() if ch.isalnum() else " " for ch in (text or ""))
    parts = {p for p in norm.split() if len(p) >= 2}
    expanded = set(parts)
    for t in list(parts):
        expanded.update(SEARCH_SYNONYMS.get(t, []))
    return expanded


def _risk_rank(risk: str) -> int:
    return {"low": 1, "medium": 2, "high": 3}.get((risk or "low").lower(), 2)


def _tier_rank(score: float) -> int:
    if score >= 0.95:
        return 3  # gold-ish
    if score >= 0.85:
        return 2  # silver-ish
    return 1  # bronze-ish


def _expand_capabilities(capabilities: list[str]) -> list[str]:
    expanded: list[str] = []
    for c in capabilities:
        c = c.strip()
        if not c:
            continue
        expanded.append(c)
        expanded.extend(CAPABILITY_ALIASES.get(c, []))
    # preserve order, de-dup
    out = []
    seen = set()
    for c in expanded:
        if c not in seen:
            out.append(c)
            seen.add(c)
    return out


def _pack_text_blob(pack: Pack) -> str:
    scopes = " ".join(_csv_to_scopes(pack.scopes_csv))
    return f"{pack.slug} {pack.title} {pack.description} {scopes}"


def _intent_boost(pack: Pack, query_tokens: set[str], required: list[str]) -> float:
    text = _pack_text_blob(pack).lower()
    caps = set(_csv_to_scopes(pack.scopes_csv))

    marketing_terms = {"marketing", "seo", "campaign", "repurpose", "content", "creator", "growth", "social"}
    security_terms = {"security", "compliance", "policy", "audit", "risk", "governance"}

    boost = 0.0

    if query_tokens.intersection(marketing_terms):
        has_marketing_text = any(t in text for t in ["marketing", "campaign", "seo", "social", "growth", "content", "repurpose"])
        has_governance_text = any(t in text for t in ["policy", "compliance", "audit", "security", "risk"])

        if has_marketing_text:
            boost += 0.22
        if any(c in caps for c in ["message.send", "web.search", "web.fetch"]):
            boost += 0.06
        if has_governance_text and not has_marketing_text:
            boost -= 0.22
        if any(t in text for t in ["approval", "policy", "compliance"]) and not any(t in text for t in ["campaign", "seo", "repurpose", "creator"]):
            boost -= 0.35

    if query_tokens.intersection(security_terms):
        if any(t in text for t in ["compliance", "policy", "audit", "security", "risk"]):
            boost += 0.2
        if _risk_rank(pack.risk_level) >= 2:
            boost += 0.05

    # Penalize personality packs for highly capability-specific requests
    if required and pack.type == PackType.personality:
        boost -= 0.1

    return boost


@app.get("/")
def root() -> FileResponse:
    return FileResponse("../web/index.html")


@app.get("/health")
def health() -> dict:
    return {"ok": True, "version": app.version}


def _bar(percent: int, width: int = 10) -> str:
    p = max(0, min(100, percent))
    filled = round((p / 100) * width)
    return "█" * filled + "░" * (width - filled)


@app.get("/ops/progress", response_model=OpsProgress)
def ops_progress() -> OpsProgress:
    # Dynamic progress sourced from a shared JSON state file when available.
    if OPS_PROGRESS_PATH.exists():
        try:
            payload = json.loads(OPS_PROGRESS_PATH.read_text())
            p = int(payload.get("percent", 0))
            return OpsProgress(
                phase=str(payload.get("phase", "execution")),
                percent=max(0, min(100, p)),
                bar=_bar(p),
                current_task=str(payload.get("current_task", "")),
                next_task=str(payload.get("next_task", "")),
            )
        except Exception:
            pass

    return OpsProgress(
        phase="execution",
        percent=0,
        bar=_bar(0),
        current_task="idle",
        next_task="awaiting next task",
    )


@app.post("/ops/progress", response_model=OpsProgress)
def set_ops_progress(payload: OpsProgressUpdate) -> OpsProgress:
    p = max(0, min(100, int(payload.percent)))
    data = {
        "phase": payload.phase,
        "percent": p,
        "current_task": payload.current_task,
        "next_task": payload.next_task,
    }
    OPS_PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    OPS_PROGRESS_PATH.write_text(json.dumps(data, indent=2))
    return OpsProgress(
        phase=payload.phase,
        percent=p,
        bar=_bar(p),
        current_task=payload.current_task,
        next_task=payload.next_task,
    )


@app.get("/.well-known/botstore.json")
def botstore_well_known() -> dict:
    return {
        "name": "BotStore",
        "description": "App store for autonomous agents: skills, personalities, trust gates, and safe installs.",
        "version": app.version,
        "discovery": {
            "capabilities_manifest": "/agent/capabilities-manifest",
            "openapi": "/openapi.json",
            "llms": "/llms.txt",
        },
        "agent_endpoints": {
            "search": "/agent/search",
            "search_capabilities": "/agent/search-capabilities",
            "install_by_capability": "/agent/install-by-capability",
            "policy_evaluate": "/agent/policy-evaluate",
            "compatibility": "/agent/compatibility/{pack_id}",
            "outcome": "/agent/outcome",
        },
        "bot_endpoints": {
            "command": "/bot/command",
            "callback": "/bot/callback",
            "where": "/where",
            "bind_target": "/targets/bind",
        },
        "auth": {
            "bot_endpoints_header": "X-Botstore-Key",
            "agent_endpoints": "public-by-default (can be gateway-protected)",
        },
    }


@app.get("/agent/capabilities-manifest")
def agent_capabilities_manifest() -> dict:
    canonical_caps = [
        "memory.read",
        "memory.write",
        "files.read",
        "files.write",
        "files.delete",
        "calendar.read",
        "calendar.write",
        "email.read",
        "email.send",
        "message.send",
        "social.post",
        "payment.charge",
        "web.search",
        "web.fetch",
        "code.exec",
        "policy.enforce",
        "risk.evaluate",
        "audit.log.read",
        "audit.log.write",
        "marketing.seo",
        "marketing.content_repurpose",
        "marketing.campaign_orchestration",
        "marketing.analytics",
    ]
    return {
        "manifest_version": "1.0",
        "runtime": "botstore",
        "capabilities": canonical_caps,
        "aliases": CAPABILITY_ALIASES,
        "risk_notes": {
            "sensitive_scopes": sorted(SENSITIVE_SCOPES),
            "approval_rule": "high risk or sensitive scopes require approval",
        },
    }


@app.get("/llms.txt", response_class=PlainTextResponse)
def llms_txt() -> str:
    return """# BotStore
BotStore is the app store for autonomous agents.

## For agents
Use these endpoints:
- GET /.well-known/botstore.json
- GET /agent/capabilities-manifest
- POST /agent/search
- POST /agent/install-by-capability
- POST /agent/policy-evaluate
- GET /agent/compatibility/{pack_id}
- POST /agent/outcome

## Notes
- Use structured capabilities and constraints where possible.
- For user-facing bot integrations use /bot/command and /bot/callback.
- Use /where and /targets/bind for explicit runtime-target install visibility.
"""


def _slugify(text: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower()).strip("-")
    return base or "imported-skill"


def _parse_skill_markdown(skill_md_path: Path) -> dict:
    raw = skill_md_path.read_text(encoding="utf-8")
    lines = [ln.rstrip() for ln in raw.splitlines()]

    title = None
    description = None
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#") and title is None:
            title = s.lstrip("#").strip()
            continue
        if not s.startswith("#") and description is None:
            description = s
            break

    scope_matches = re.findall(r"`([a-z]+(?:\.[a-z0-9_]+)+)`", raw.lower())
    scopes = sorted(set(scope_matches))

    inferred_risk = "high" if any(s in {"payment.charge", "files.delete"} for s in scopes) else "medium" if any(
        s in {"email.send", "message.send", "social.post"} for s in scopes
    ) else "low"

    title = title or skill_md_path.parent.name
    description = description or "Imported from OpenClaw skill folder"

    return {
        "title": title,
        "slug": _slugify(title),
        "description": description,
        "scopes": scopes,
        "risk_level": inferred_risk,
    }


def _ensure_pack_version(
    session: Session,
    pack: Pack,
    capabilities_declared: Optional[list[str]] = None,
    scopes_requested: Optional[list[str]] = None,
    actions_supported: Optional[list[str]] = None,
) -> PackVersion:
    existing = session.exec(
        select(PackVersion).where(
            PackVersion.pack_id == (pack.id or 0),
            PackVersion.semver == pack.version,
            PackVersion.is_current == True,
        )
    ).first()
    if existing:
        return existing

    capabilities = capabilities_declared if capabilities_declared is not None else _csv_to_scopes(pack.scopes_csv)
    scopes = scopes_requested if scopes_requested is not None else _csv_to_scopes(pack.scopes_csv)
    actions = actions_supported if actions_supported is not None else []
    raw = {
        "pack_id": pack.id,
        "slug": pack.slug,
        "version": pack.version,
        "capabilities_declared": sorted(set(capabilities)),
        "scopes_requested": sorted(set(scopes)),
        "actions_supported": sorted(set(actions)),
    }
    digest = "sha256:" + hashlib.sha256(json.dumps(raw, sort_keys=True).encode("utf-8")).hexdigest()

    pv = PackVersion(
        pack_id=pack.id or 0,
        semver=pack.version,
        artifact_digest=digest,
        verification_tier="tier0_listed",
        compatible_runtimes_json=json.dumps(["openclaw"]),
        policy_requirements_json=json.dumps({"runtime_band_max": "C"}),
        capabilities_declared_json=json.dumps(sorted(set(capabilities))),
        scopes_requested_json=json.dumps(sorted(set(scopes))),
        actions_supported_json=json.dumps(sorted(set(actions))),
        created_at=_iso_now(),
    )
    session.add(pv)
    session.commit()
    session.refresh(pv)
    return pv


@app.post("/creators", response_model=Creator)
def create_creator(payload: CreatorCreate) -> Creator:
    with Session(engine) as session:
        creator = Creator.model_validate(payload)
        session.add(creator)
        session.commit()
        session.refresh(creator)
        return creator


@app.get("/creators", response_model=list[Creator])
def list_creators() -> list[Creator]:
    with Session(engine) as session:
        return list(session.exec(select(Creator)).all())


@app.post("/packs", response_model=Pack)
def create_pack(payload: PackCreate) -> Pack:
    with Session(engine) as session:
        existing = session.exec(select(Pack).where(Pack.slug == payload.slug)).first()
        if existing:
            raise HTTPException(status_code=409, detail="slug already exists")
        if payload.creator_id and not session.get(Creator, payload.creator_id):
            raise HTTPException(status_code=404, detail="creator not found")
        if payload.type == PackType.bundle:
            for child_id in payload.bundle_pack_ids:
                child = session.get(Pack, child_id)
                if not child:
                    raise HTTPException(status_code=404, detail=f"bundle child pack not found: {child_id}")
        if payload.is_featured:
            raise HTTPException(
                status_code=400,
                detail="Featured publish must go through promotion gate (/packs/{id}/promote) after QA pass",
            )
        pack = Pack(
            slug=payload.slug,
            title=payload.title,
            type=payload.type,
            version=payload.version,
            description=payload.description,
            risk_level=payload.risk_level,
            scopes_csv=_scopes_to_csv(payload.scopes),
            bundle_pack_ids_csv=_ints_to_csv(payload.bundle_pack_ids),
            is_featured=payload.is_featured,
            creator_id=payload.creator_id,
        )
        session.add(pack)
        session.commit()
        session.refresh(pack)
        _ensure_pack_version(session, pack)
        return pack


@app.post("/packs/{pack_id}/versions", response_model=PackVersion)
def create_pack_version(pack_id: int, payload: PackVersionCreate) -> PackVersion:
    with Session(engine) as session:
        pack = session.get(Pack, pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")

        prior = session.exec(select(PackVersion).where(PackVersion.pack_id == pack_id, PackVersion.is_current == True)).all()
        for row in prior:
            row.is_current = False
            session.add(row)

        raw = {
            "pack_id": pack_id,
            "semver": payload.semver,
            "manifest_version": payload.manifest_version,
            "capabilities_declared": sorted(set(payload.capabilities_declared)),
            "scopes_requested": sorted(set(payload.scopes_requested)),
            "actions_supported": sorted(set(payload.actions_supported)),
        }
        digest = "sha256:" + hashlib.sha256(json.dumps(raw, sort_keys=True).encode("utf-8")).hexdigest()

        pv = PackVersion(
            pack_id=pack_id,
            semver=payload.semver,
            manifest_version=payload.manifest_version,
            artifact_digest=digest,
            verification_tier=payload.verification_tier,
            compatible_runtimes_json=json.dumps(sorted(set(payload.compatible_runtimes))),
            policy_requirements_json=json.dumps(payload.policy_requirements),
            capabilities_declared_json=json.dumps(sorted(set(payload.capabilities_declared))),
            scopes_requested_json=json.dumps(sorted(set(payload.scopes_requested))),
            actions_supported_json=json.dumps(sorted(set(payload.actions_supported))),
            created_at=_iso_now(),
            is_current=True,
        )
        session.add(pv)
        session.commit()
        session.refresh(pv)
        return pv


@app.get("/packs/{pack_id}/versions", response_model=list[PackVersion])
def list_pack_versions(pack_id: int) -> list[PackVersion]:
    with Session(engine) as session:
        return list(session.exec(select(PackVersion).where(PackVersion.pack_id == pack_id).order_by(PackVersion.id.desc())).all())


@app.post("/interop/import-skill-folder")
def interop_import_skill_folder(payload: SkillImportRequest) -> dict:
    skill_path = Path(payload.skill_path).expanduser().resolve()
    if not skill_path.exists() or not skill_path.is_dir():
        raise HTTPException(status_code=404, detail="skill folder not found")

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise HTTPException(status_code=400, detail="SKILL.md not found in folder")

    parsed = _parse_skill_markdown(skill_md)
    warnings: list[str] = []
    if not parsed["scopes"]:
        warnings.append("No tool scopes detected from SKILL.md backticks")

    with Session(engine) as session:
        creator_id = payload.creator_id
        if creator_id and not session.get(Creator, creator_id):
            raise HTTPException(status_code=404, detail="creator not found")

        existing = session.exec(select(Pack).where(Pack.slug == parsed["slug"])).first()
        if existing:
            return {
                "created": False,
                "reason": "slug already exists",
                "pack_id": existing.id,
                "slug": existing.slug,
                "warnings": warnings,
            }

        pack = Pack(
            slug=parsed["slug"],
            title=parsed["title"],
            type=payload.pack_type,
            version="0.1.0",
            description=parsed["description"],
            risk_level=parsed["risk_level"],
            scopes_csv=_scopes_to_csv(parsed["scopes"]),
            bundle_pack_ids_csv="",
            is_featured=False,
            creator_id=creator_id,
        )
        session.add(pack)
        session.commit()
        session.refresh(pack)
        _ensure_pack_version(session, pack, capabilities_declared=parsed["scopes"], scopes_requested=parsed["scopes"], actions_supported=[])

        return {
            "created": True,
            "pack_id": pack.id,
            "slug": pack.slug,
            "title": pack.title,
            "pack_type": str(pack.type),
            "scopes": parsed["scopes"],
            "warnings": warnings,
        }


@app.post("/interop/export-skill")
def interop_export_skill(payload: SkillExportRequest) -> dict:
    with Session(engine) as session:
        pack = session.exec(select(Pack).where(Pack.slug == payload.slug)).first()
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")

        out_root = Path(payload.out_dir).expanduser().resolve()
        target_dir = out_root / pack.slug
        target_dir.mkdir(parents=True, exist_ok=True)

        scopes = _csv_to_scopes(pack.scopes_csv)
        scope_block = "\n".join([f"- `{s}`" for s in scopes]) if scopes else "- (none declared)"
        skill_md = f"""# {pack.title}\n\n{pack.description}\n\n## Exported from BotStore\n- slug: `{pack.slug}`\n- type: `{pack.type}`\n- version: `{pack.version}`\n- risk_level: `{pack.risk_level}`\n\n## Declared scopes\n{scope_block}\n"""
        (target_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

        manifest = {
            "slug": pack.slug,
            "title": pack.title,
            "type": str(pack.type),
            "version": pack.version,
            "description": pack.description,
            "risk_level": pack.risk_level,
            "scopes": scopes,
            "exported_from": "botstore",
        }
        (target_dir / "botstore-export.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return {
            "ok": True,
            "slug": pack.slug,
            "path": str(target_dir),
            "files": ["SKILL.md", "botstore-export.json"],
        }


@app.get("/teams/custom/roles")
def teams_custom_roles() -> dict:
    role_catalog = _load_json(ROLE_AGENT_CATALOG_PATH) or {}
    roles = role_catalog.get("agents", []) if isinstance(role_catalog, dict) else []
    return {"roles": roles, "count": len(roles)}


@app.get("/teams/custom/scenarios")
def teams_custom_scenarios() -> dict:
    scenarios_doc = _load_json(TEAM_SCENARIOS_PATH) or {}
    scenarios = scenarios_doc.get("scenarios", []) if isinstance(scenarios_doc, dict) else []
    return {"scenarios": scenarios, "count": len(scenarios)}


@app.post("/teams/custom/compose")
def teams_custom_compose(payload: TeamComposeRequest) -> dict:
    role_catalog = _load_json(ROLE_AGENT_CATALOG_PATH) or {}
    roles = role_catalog.get("agents", []) if isinstance(role_catalog, dict) else []
    by_slug = {r.get("slug"): r for r in roles}

    selected_roles = []
    missing_role_slugs = []
    shared_skills = set(payload.additional_shared_skills or [])

    for rs in payload.role_slugs:
        r = by_slug.get(rs)
        if not r:
            missing_role_slugs.append(rs)
            continue
        selected_roles.append(
            {
                "role": r.get("role"),
                "personality_slug": r.get("personality_slug"),
                "owned_skills": r.get("starter_skills", []),
                "deliverables": ["status-report", "action-items"],
            }
        )
        for sk in r.get("suggested_shared_skills", []) or []:
            shared_skills.add(sk)

    team = {
        "slug": _slugify(payload.name),
        "title": payload.name,
        "purpose": payload.objective,
        "team_type": "custom",
        "shared_skills": sorted(s for s in shared_skills if isinstance(s, str) and s.strip()),
        "roles": selected_roles,
        "risk_level": payload.risk_level,
    }

    integrity = _team_skill_integrity(team)
    valid = set(integrity.get("valid_skill_slugs", []))

    team["shared_skills"] = [s for s in team.get("shared_skills", []) if s in valid]
    for role in team.get("roles", []) or []:
        role["owned_skills"] = [s for s in (role.get("owned_skills", []) or []) if s in valid]

    return {
        "ok": True,
        "team": team,
        "missing_role_slugs": missing_role_slugs,
        "dropped_non_market_skills": {
            "missing": integrity.get("missing_skills", []),
            "non_skill_refs": integrity.get("non_skill_refs", []),
        },
    }


@app.post("/teams/custom/validate")
def teams_custom_validate(payload: TeamValidateRequest) -> dict:
    team = payload.team or {}
    issues: list[dict] = []

    if len(team.get("roles", []) or []) < 2:
        issues.append({"severity": "warning", "code": "team.low_role_count", "message": "Team should include at least 2 roles"})

    risk = (team.get("risk_level") or "low").lower()
    if risk in {"medium", "high"}:
        has_governance = any(
            any(k in (str(r.get("personality_slug") or "").lower()) for k in ["compliance", "privacy", "forensic"])
            for r in (team.get("roles", []) or [])
        )
        if not has_governance:
            issues.append(
                {
                    "severity": "warning",
                    "code": "team.governance_missing",
                    "message": "Medium/high risk teams should include governance/privacy/security personality",
                }
            )

    evalr = _team_eval(team, payload.required_capabilities, payload.required_roles, payload.expected_artifacts)
    integrity = evalr.get("integrity", {})

    if integrity.get("missing_skills"):
        issues.append(
            {
                "severity": "error",
                "code": "team.skills_missing_from_marketplace",
                "message": "Team references skills not present as standalone marketplace skills",
                "details": {"missing_skills": integrity.get("missing_skills", [])},
            }
        )
    if integrity.get("non_skill_refs"):
        issues.append(
            {
                "severity": "error",
                "code": "team.non_skill_refs",
                "message": "Team references non-skill packs; team sub-agent capabilities must map to standalone skill packs",
                "details": {"non_skill_refs": integrity.get("non_skill_refs", [])},
            }
        )

    if not evalr.get("pass"):
        issues.append(
            {
                "severity": "warning",
                "code": "team.coverage_gap",
                "message": "Team coverage below pass threshold",
                "details": {
                    "missing_capabilities": evalr.get("missing_capabilities", []),
                    "missing_roles": evalr.get("missing_roles", []),
                    "missing_artifacts": evalr.get("missing_artifacts", []),
                },
            }
        )

    has_errors = any(i.get("severity") == "error" for i in issues)
    final_pass = bool(evalr.get("pass")) and not has_errors

    return {
        "ok": not has_errors,
        "score": evalr.get("score"),
        "pass": final_pass,
        "coverage": {
            "capability": evalr.get("capability_coverage"),
            "role": evalr.get("role_coverage"),
            "artifact": evalr.get("artifact_coverage"),
        },
        "missing": {
            "capabilities": evalr.get("missing_capabilities", []),
            "roles": evalr.get("missing_roles", []),
            "artifacts": evalr.get("missing_artifacts", []),
            "skills": integrity.get("missing_skills", []),
        },
        "integrity": {
            "valid_skill_slugs": integrity.get("valid_skill_slugs", []),
            "non_skill_refs": integrity.get("non_skill_refs", []),
        },
        "issues": issues,
    }


@app.post("/teams/custom/simulate")
def teams_custom_simulate(payload: TeamSimulateRequest) -> dict:
    scenarios_doc = _load_json(TEAM_SCENARIOS_PATH) or {}
    scenarios = scenarios_doc.get("scenarios", []) if isinstance(scenarios_doc, dict) else []

    picked = scenarios
    if payload.scenario_ids:
        allow = set(payload.scenario_ids)
        picked = [s for s in scenarios if s.get("id") in allow]

    rows = []
    for scen in picked:
        evalr = _team_eval(
            payload.team or {},
            scen.get("required_capabilities", []),
            scen.get("required_roles", []),
            scen.get("expected_artifacts", []),
        )
        rows.append(
            {
                "scenario_id": scen.get("id"),
                "score": evalr.get("score"),
                "pass": evalr.get("pass"),
                "missing_capabilities": evalr.get("missing_capabilities", []),
                "missing_roles": evalr.get("missing_roles", []),
                "missing_artifacts": evalr.get("missing_artifacts", []),
            }
        )

    total = len(rows)
    passed = sum(1 for r in rows if r.get("pass"))
    avg = round(sum(float(r.get("score") or 0) for r in rows) / max(total, 1), 3)
    return {
        "ok": True,
        "summary": {"total": total, "pass": passed, "avg_score": avg},
        "scenarios": rows,
    }


@app.post("/teams/custom/publish")
def teams_custom_publish(payload: TeamPublishRequest) -> dict:
    team = payload.team or {}
    slug = str(team.get("slug") or _slugify(team.get("title") or "custom-team"))
    title = str(team.get("title") or slug)
    purpose = str(team.get("purpose") or "Custom team pack")
    risk = str(team.get("risk_level") or "medium").lower()

    with Session(engine) as session:
        if payload.creator_id and not session.get(Creator, payload.creator_id):
            raise HTTPException(status_code=404, detail="creator not found")

        existing = session.exec(select(Pack).where(Pack.slug == slug)).first()
        if existing:
            raise HTTPException(status_code=409, detail="slug already exists")

        integrity = _team_skill_integrity(team)
        if integrity.get("missing_skills") or integrity.get("non_skill_refs"):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Team publish blocked: all team capabilities must map to standalone marketplace skills",
                    "missing_skills": integrity.get("missing_skills", []),
                    "non_skill_refs": integrity.get("non_skill_refs", []),
                },
            )

        skill_slugs = integrity.get("valid_skill_slugs", [])
        child_ids = []
        for s in skill_slugs:
            p = session.exec(select(Pack).where(Pack.slug == s)).first()
            if p:
                child_ids.append(p.id)

        pack = Pack(
            slug=slug,
            title=title,
            type=PackType.bundle,
            version="0.1.0",
            description=f"Team Pack: {purpose}",
            risk_level=risk if risk in {"low", "medium", "high"} else "medium",
            scopes_csv="",
            bundle_pack_ids_csv=_ints_to_csv([int(x) for x in child_ids if x]),
            is_featured=False,
            creator_id=payload.creator_id,
        )
        session.add(pack)
        session.commit()
        session.refresh(pack)

        TEAM_PUBLISHED_PATH.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "published_at": datetime.now(timezone.utc).isoformat(),
            "pack_id": pack.id,
            "slug": slug,
            "title": title,
            "team": team,
            "skill_integrity": {
                "valid_skill_slugs": skill_slugs,
                "missing_skills": [],
                "non_skill_refs": [],
            },
        }
        with TEAM_PUBLISHED_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

        return {
            "ok": True,
            "pack_id": pack.id,
            "slug": pack.slug,
            "bundle_child_count": len(child_ids),
            "missing_skills": [],
            "non_skill_refs": [],
        }


@app.post("/jobs/enqueue")
def jobs_enqueue(payload: JobEnqueueRequest) -> dict:
    allowed = {"ci_gate_run_all", "ranking_eval_ci", "team_qa_v3_plus_reddit"}
    if payload.job_type not in allowed:
        raise HTTPException(status_code=400, detail=f"unsupported job_type: {payload.job_type}")

    job_id = f"job_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc).isoformat()
    entry = {
        "job_id": job_id,
        "job_type": payload.job_type,
        "payload": payload.payload or {},
        "created_at": now,
    }
    _append_job_queue(entry)

    status = _load_job_status()
    status[job_id] = {
        "job_id": job_id,
        "job_type": payload.job_type,
        "status": "queued",
        "created_at": now,
        "updated_at": now,
    }
    _save_job_status(status)
    return {"ok": True, "job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
def jobs_status(job_id: str) -> dict:
    status = _load_job_status()
    row = status.get(job_id)
    if not row:
        raise HTTPException(status_code=404, detail="job not found")
    return row


@app.get("/jobs")
def jobs_list(limit: int = 50) -> dict:
    status = _load_job_status()
    rows = list(status.values())
    rows.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return {"count": len(rows[:limit]), "jobs": rows[:limit]}


@app.post("/artifacts/publish")
def artifacts_publish(payload: ArtifactPublishRequest) -> dict:
    source = Path(payload.source_path).expanduser().resolve()
    if not source.exists() or not source.is_file():
        raise HTTPException(status_code=404, detail="source file not found")

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    name = payload.artifact_name or source.name
    safe_name = re.sub(r"[^a-zA-Z0-9._-]+", "-", name)
    target = (ARTIFACTS_DIR / safe_name).resolve()

    # Ensure target is within ARTIFACTS_DIR
    if ARTIFACTS_DIR.resolve() not in target.parents and target != ARTIFACTS_DIR.resolve():
        raise HTTPException(status_code=400, detail="invalid artifact_name")

    shutil.copy2(source, target)
    return {
        "ok": True,
        "artifact": safe_name,
        "path": str(target),
        "size_bytes": target.stat().st_size,
    }


@app.post("/qa/report")
def upsert_qa_report(payload: PackQAUpdate) -> dict:
    status = (payload.status or "").strip().lower()
    if status not in {"pending", "pass", "fail"}:
        raise HTTPException(status_code=400, detail="status must be one of: pending, pass, fail")

    with Session(engine) as session:
        pack = session.get(Pack, payload.pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")

        row = session.exec(select(PackQAReport).where(PackQAReport.pack_id == payload.pack_id)).first()
        now = datetime.now(timezone.utc).isoformat()
        if row:
            row.status = status
            row.suite = payload.suite or row.suite or "default"
            row.report_path = payload.report_path
            row.summary = payload.summary
            row.updated_at = now
        else:
            row = PackQAReport(
                pack_id=payload.pack_id,
                status=status,
                suite=payload.suite or "default",
                report_path=payload.report_path,
                summary=payload.summary,
                updated_at=now,
            )
            session.add(row)

        session.commit()
        session.refresh(row)
        return {
            "ok": True,
            "pack_id": row.pack_id,
            "status": row.status,
            "suite": row.suite,
            "updated_at": row.updated_at,
            "report_path": row.report_path,
        }


@app.get("/qa/report/{pack_id}")
def get_qa_report(pack_id: int) -> dict:
    with Session(engine) as session:
        row = session.exec(select(PackQAReport).where(PackQAReport.pack_id == pack_id)).first()
        if not row:
            return {"pack_id": pack_id, "status": "missing"}
        return {
            "pack_id": row.pack_id,
            "status": row.status,
            "suite": row.suite,
            "report_path": row.report_path,
            "summary": row.summary,
            "updated_at": row.updated_at,
        }


@app.put("/packs/{pack_id}/promote", response_model=Pack)
def promote_pack(pack_id: int, featured: bool = True) -> Pack:
    with Session(engine) as session:
        pack = session.get(Pack, pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")

        if featured:
            qa = session.exec(select(PackQAReport).where(PackQAReport.pack_id == pack_id)).first()
            if not qa or qa.status != "pass":
                raise HTTPException(status_code=400, detail="QA pass required before promotion")

        pack.is_featured = featured
        session.add(pack)
        session.commit()
        session.refresh(pack)
        return pack


@app.post("/bundles/validate")
def validate_bundle(payload: BundleValidateRequest) -> dict:
    issues: list[dict] = []

    child_ids = [int(x) for x in payload.child_pack_ids if int(x) > 0]
    if not child_ids:
        return {
            "ok": False,
            "issues": [
                {
                    "severity": "error",
                    "code": "bundle.empty",
                    "message": "Bundle must include at least one child pack",
                    "pack_ids": [],
                }
            ],
            "summary": {"errors": 1, "warnings": 0},
        }

    if len(set(child_ids)) != len(child_ids):
        dupes = sorted({x for x in child_ids if child_ids.count(x) > 1})
        issues.append(
            {
                "severity": "error",
                "code": "bundle.duplicate_child_ids",
                "message": f"Duplicate child pack IDs detected: {dupes}",
                "pack_ids": dupes,
            }
        )

    with Session(engine) as session:
        children: list[Pack] = []
        for child_id in sorted(set(child_ids)):
            c = session.get(Pack, child_id)
            if not c:
                issues.append(
                    {
                        "severity": "error",
                        "code": "bundle.child_missing",
                        "message": f"Child pack not found: {child_id}",
                        "pack_ids": [child_id],
                    }
                )
                continue
            children.append(c)

    for c in children:
        if c.type == PackType.bundle:
            issues.append(
                {
                    "severity": "warning",
                    "code": "bundle.nested_bundle",
                    "message": f"Nested bundle detected: {c.slug}",
                    "pack_ids": [c.id],
                }
            )

    # Risk-level consistency check
    risk_rank = {"low": 1, "medium": 2, "high": 3}
    highest_child_risk = max((risk_rank.get((c.risk_level or "low").lower(), 1) for c in children), default=1)
    proposed = risk_rank.get((payload.proposed_risk_level or "medium").lower(), 2)
    if proposed < highest_child_risk:
        issues.append(
            {
                "severity": "warning",
                "code": "bundle.risk_mismatch",
                "message": "Proposed bundle risk is lower than highest child risk",
                "pack_ids": [c.id for c in children if risk_rank.get((c.risk_level or "low").lower(), 1) == highest_child_risk],
            }
        )

    # Duplicate-problem and redundancy checks
    def _text_tokens(p: Pack) -> set[str]:
        text = f"{p.title} {p.description}".lower()
        return _tokenize(text)

    for i in range(len(children)):
        for j in range(i + 1, len(children)):
            a = children[i]
            b = children[j]
            ta = _text_tokens(a)
            tb = _text_tokens(b)
            text_overlap = len(ta.intersection(tb)) / max(len(ta.union(tb)), 1)
            sa = set(_csv_to_scopes(a.scopes_csv))
            sb = set(_csv_to_scopes(b.scopes_csv))
            scope_overlap = len(sa.intersection(sb)) / max(len(sa.union(sb)), 1)

            if text_overlap >= 0.62:
                issues.append(
                    {
                        "severity": "warning",
                        "code": "bundle.problem_overlap",
                        "message": f"Potential duplicate problem target: {a.slug} and {b.slug}",
                        "pack_ids": [a.id, b.id],
                    }
                )
            elif text_overlap >= 0.4 and scope_overlap >= 0.75:
                issues.append(
                    {
                        "severity": "warning",
                        "code": "bundle.capability_redundancy",
                        "message": f"High capability redundancy: {a.slug} and {b.slug}",
                        "pack_ids": [a.id, b.id],
                    }
                )

    errors = sum(1 for x in issues if x["severity"] == "error")
    warnings = sum(1 for x in issues if x["severity"] == "warning")
    return {"ok": errors == 0, "issues": issues, "summary": {"errors": errors, "warnings": warnings}}


@app.get("/packs", response_model=list[Pack])
def list_packs(type: Optional[PackType] = None) -> list[Pack]:
    with Session(engine) as session:
        query = select(Pack)
        if type:
            query = query.where(Pack.type == type)
        return list(session.exec(query).all())


@app.get("/catalog", response_model=list[CatalogPack])
def catalog(type: Optional[PackType] = None, featured_only: bool = False) -> list[CatalogPack]:
    with Session(engine) as session:
        query = select(Pack)
        if type:
            query = query.where(Pack.type == type)
        if featured_only:
            query = query.where(Pack.is_featured == True)
        packs = list(session.exec(query).all())
        qa_rows = list(session.exec(select(PackQAReport)).all())
        qa_by_pack = {q.pack_id: q for q in qa_rows}

        out: list[CatalogPack] = []
        for p in packs:
            creator = session.get(Creator, p.creator_id) if p.creator_id else None
            qa = qa_by_pack.get(p.id or -1)
            out.append(
                CatalogPack(
                    id=p.id or 0,
                    slug=p.slug,
                    title=p.title,
                    type=p.type,
                    version=p.version,
                    description=p.description,
                    risk_level=p.risk_level,
                    scopes=_csv_to_scopes(p.scopes_csv),
                    bundle_pack_ids=_csv_to_ints(p.bundle_pack_ids_csv),
                    requires_approval=_requires_approval(p),
                    is_featured=p.is_featured,
                    creator_id=p.creator_id,
                    creator_name=creator.name if creator else None,
                    creator_verification=creator.verification if creator else None,
                    creator_trust_score=creator.trust_score if creator else None,
                    qa_status=qa.status if qa else None,
                    qa_suite=qa.suite if qa else None,
                    qa_updated_at=qa.updated_at if qa else None,
                    qa_report_path=qa.report_path if qa else None,
                )
            )
        return out


def _pack_score_for_capabilities(pack: Pack, required: list[str]) -> float:
    pack_caps = set(_csv_to_scopes(pack.scopes_csv))
    req = [c.strip() for c in required if c.strip()]
    if not req:
        return 0.0

    covered = len([c for c in req if c in pack_caps])
    coverage = covered / max(len(req), 1)

    has_sensitive_req = any(c in SENSITIVE_SCOPES for c in req)
    if has_sensitive_req:
        # For sensitive capability requests, prefer governance-capable packs.
        risk_adjust = {"low": -0.03, "medium": 0.02, "high": 0.06}.get(pack.risk_level.lower(), 0.0)
    else:
        risk_adjust = -{"low": 0.0, "medium": 0.08, "high": 0.2}.get(pack.risk_level.lower(), 0.1)

    type_bias = {PackType.skill: 0.05, PackType.bundle: -0.02, PackType.personality: -0.08}.get(pack.type, 0.0)
    return coverage + risk_adjust + type_bias


@app.post("/agent/search-capabilities")
def agent_search_capabilities(payload: AgentSearchRequest) -> dict:
    with Session(engine) as session:
        packs = list(session.exec(select(Pack)).all())
        ranked = []
        for p in packs:
            score = _pack_score_for_capabilities(p, payload.missing_capabilities)
            if score <= 0:
                continue
            ranked.append({
                "pack_id": p.id,
                "slug": p.slug,
                "title": p.title,
                "type": p.type,
                "score": round(score, 4),
                "capabilities": _csv_to_scopes(p.scopes_csv),
                "requires_approval": _requires_approval(p),
            })
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return {
            "runtime": payload.runtime,
            "intent": payload.intent,
            "required_capabilities": payload.missing_capabilities,
            "results": ranked[: max(1, min(payload.limit, 50))],
        }


@app.post("/agent/search")
def agent_search(payload: AgentSearchQuery) -> dict:
    query_tokens = _tokenize(payload.query)
    required = _expand_capabilities([c.strip() for c in payload.missing_capabilities if c.strip()])
    constraints = payload.constraints or AgentSearchConstraints()

    with Session(engine) as session:
        packs = list(session.exec(select(Pack)).all())
        ranked: list[dict] = []

        for p in packs:
            creator = session.get(Creator, p.creator_id) if p.creator_id else None
            creator_trust = float(creator.trust_score) if creator else 0.5
            creator_verified = 1.0 if (creator and creator.verification == VerificationStatus.verified) else 0.0

            capability_score = _pack_score_for_capabilities(p, required) if required else 0.0
            pack_tokens = _tokenize(_pack_text_blob(p))
            overlap = len(query_tokens.intersection(pack_tokens))
            text_score = overlap / max(len(query_tokens), 1) if query_tokens else 0.0

            trust_score = (0.08 * creator_trust) + (0.04 * creator_verified)
            intent_boost = _intent_boost(p, query_tokens, required)
            total = capability_score + (0.45 * text_score) + trust_score + intent_boost

            # Constraints
            if constraints.risk_max and _risk_rank(p.risk_level) > _risk_rank(constraints.risk_max):
                continue
            if constraints.tier_min and _tier_rank(total) < {"bronze": 1, "silver": 2, "gold": 3}.get(constraints.tier_min, 1):
                continue

            reasons = []
            if required:
                pack_caps = set(_csv_to_scopes(p.scopes_csv))
                covered = sorted([c for c in required if c in pack_caps])
                reasons.append(f"covers capabilities: {', '.join(covered) if covered else 'none'}")
            if query_tokens:
                reasons.append(f"query term overlap: {overlap}")
            reasons.append(f"risk={p.risk_level}")
            reasons.append(f"creator_trust={creator_trust}")
            reasons.append(f"intent_boost={round(intent_boost,3)}")

            ranked.append({
                "pack_id": p.id,
                "slug": p.slug,
                "title": p.title,
                "type": p.type,
                "score": round(total, 4),
                "capabilities": _csv_to_scopes(p.scopes_csv),
                "requires_approval": _requires_approval(p),
                "why": reasons,
            })

        ranked.sort(
            key=lambda x: (
                x["score"],
                1 if x["requires_approval"] else 0,
                x["slug"],
            ),
            reverse=True,
        )

        return {
            "query": payload.query,
            "parsed_terms": sorted(query_tokens),
            "required_capabilities": required,
            "constraints": constraints.model_dump(),
            "results": ranked[: max(1, min(payload.limit, 50))],
        }


def _policy_decide_for_version(
    pv: PackVersion,
    runtime_band: RuntimeBand,
    tenant_id: str,
    requested_scope: Optional[str] = None,
) -> tuple[str, list[str], list[str]]:
    _ = tenant_id
    scopes = set(_json_list(pv.scopes_requested_json))
    if requested_scope:
        scopes.add(requested_scope)
    sensitive_hit = bool(scopes.intersection(SENSITIVE_SCOPES))

    max_band = _json_obj(pv.policy_requirements_json).get("runtime_band_max", "C")
    if _runtime_band_rank(runtime_band) > _runtime_band_rank(max_band):
        return (
            "deny",
            [POLICY_REASON_CODES["RUNTIME_BAND_TOO_WEAK"]],
            [f"runtime band {runtime_band} exceeds max {max_band}"],
        )

    if sensitive_hit or pv.verification_tier in {"tier0_listed"}:
        return ("allow_with_approval", [POLICY_REASON_CODES["SENSITIVE_OR_LOW_VERIFICATION"]], [])

    return ("allow", [POLICY_REASON_CODES["LOW_RISK_CONTEXT"]], [])


@app.post("/agent/install-by-capability")
def agent_install_by_capability(payload: AgentInstallByCapabilityRequest) -> dict:
    search = agent_search_capabilities(
        AgentSearchRequest(
            user_id=payload.user_id,
            runtime=payload.runtime,
            missing_capabilities=payload.required_capabilities,
            limit=10,
        )
    )
    chosen = search.get("results", [])
    if not chosen:
        return {"ok": False, "message": "no matching packs", "installs": []}

    installs: list[dict] = []
    with Session(engine) as session:
        covered_caps: set[str] = set()
        req = [c.strip() for c in payload.required_capabilities if c.strip()]
        for candidate in chosen:
            pack = session.get(Pack, int(candidate["pack_id"]))
            if not pack:
                continue
            pack_caps = set(_csv_to_scopes(pack.scopes_csv))
            if not any(c in pack_caps for c in req if c not in covered_caps):
                continue
            res = _create_install(session, payload.user_id, pack)
            installs.append({
                "pack_id": pack.id,
                "slug": pack.slug,
                "install_id": res.install.id,
                "status": res.install.status,
                "approval_id": res.approval_id,
            })
            covered_caps.update(pack_caps)
            if all(c in covered_caps for c in req):
                break

    return {
        "ok": True,
        "required_capabilities": payload.required_capabilities,
        "installed_count": len(installs),
        "installs": installs,
    }


@app.post("/agent/install-by-capability-v2")
def agent_install_by_capability_v2(payload: AgentInstallByCapabilityV2Request) -> dict:
    attempt_id = f"att_{uuid.uuid4().hex[:16]}"
    candidate_snapshot_id = f"cand_{uuid.uuid4().hex[:12]}"

    with Session(engine) as session:
        candidates: list[dict] = []
        req = [c.strip() for c in payload.required_capabilities if c.strip()]
        pvs = list(session.exec(select(PackVersion).where(PackVersion.is_current == True)).all())
        for pv in pvs:
            pack = session.get(Pack, pv.pack_id)
            if not pack:
                continue
            compatible = set(_json_list(pv.compatible_runtimes_json))
            if compatible and payload.runtime_id not in compatible and "*" not in compatible:
                continue
            caps = set(_json_list(pv.capabilities_declared_json))
            coverage = len(caps.intersection(req)) / max(len(req), 1)
            if coverage <= 0:
                continue
            effect, reasons, blocking = _policy_decide_for_version(pv, payload.runtime_band, payload.tenant_id)
            if effect == "deny":
                continue
            risk_penalty = {"low": 0.02, "medium": 0.08, "high": 0.18}.get(pack.risk_level, 0.1)
            approval_friction = 0.2 if effect == "allow_with_approval" else 0.0
            score = round((coverage + 0.2) - risk_penalty - approval_friction, 4)
            candidates.append({
                "pack_id": pack.id,
                "pack_slug": pack.slug,
                "pack_version_id": pv.id,
                "artifact_digest": pv.artifact_digest,
                "verification_tier": pv.verification_tier,
                "capabilities_declared": sorted(caps),
                "scopes_requested": _json_list(pv.scopes_requested_json),
                "actions_supported": _json_list(pv.actions_supported_json),
                "policy_effect": effect,
                "policy_reasons": reasons,
                "policy_blocking": blocking,
                "score": score,
            })

        candidates.sort(key=lambda x: x["score"], reverse=True)
        candidates = candidates[: max(1, min(payload.limit, 50))]

        attempt = InstallAttempt(
            attempt_id=attempt_id,
            task_id=payload.task_id,
            tenant_id=payload.tenant_id,
            user_id=payload.user_id,
            agent_id_hash=hashlib.sha256(payload.agent_id.encode("utf-8")).hexdigest(),
            runtime_id=payload.runtime_id,
            runtime_version=payload.runtime_version,
            runtime_band=payload.runtime_band,
            missing_capabilities_json=json.dumps(req),
            candidate_snapshot_id=candidate_snapshot_id,
            candidate_snapshot_json=json.dumps(candidates),
            install_status="pending",
            activation_status="pending",
            rollback_status="not_requested",
            status=InstallAttemptStatus.candidate_set_ready,
            created_at=_iso_now(),
            updated_at=_iso_now(),
        )
        session.add(attempt)
        session.commit()
        session.refresh(attempt)

        for idx, cand in enumerate(candidates, start=1):
            session.add(
                CandidateImpression(
                    attempt_id=attempt_id,
                    candidate_snapshot_id=candidate_snapshot_id,
                    rank=idx,
                    pack_id=int(cand["pack_id"]),
                    pack_version_id=int(cand["pack_version_id"]),
                    artifact_digest=cand["artifact_digest"],
                    score=float(cand["score"]),
                    selected=False,
                    policy_effect=cand.get("policy_effect", "allow"),
                    policy_reason_codes_json=json.dumps(cand.get("policy_reasons", [])),
                    exploration_bucket="deterministic",
                    propensity=1.0,
                    features_json=json.dumps({
                        "coverage": len(set(cand.get("capabilities_declared", [])).intersection(req)) / max(len(req), 1),
                        "verification_tier": cand.get("verification_tier"),
                    }),
                    created_at=_iso_now(),
                )
            )
        session.commit()

        if not candidates:
            attempt.status = InstallAttemptStatus.failed
            attempt.install_status = "no_candidates"
            attempt.updated_at = _iso_now()
            session.add(attempt)
            session.commit()
            return {"ok": False, "attempt_id": attempt_id, "message": "no matching pack versions", "candidates": []}

        winner = candidates[0]
        pv = session.get(PackVersion, int(winner["pack_version_id"]))
        if not pv:
            raise HTTPException(status_code=500, detail="selected pack version missing")

        policy_payload = {
            "attempt_id": attempt_id,
            "tenant_id": payload.tenant_id,
            "runtime_band": payload.runtime_band,
            "pack_version_id": pv.id,
            "artifact_digest": pv.artifact_digest,
            "required_capabilities": req,
        }
        effect, reasons, blocking = _policy_decide_for_version(pv, payload.runtime_band, payload.tenant_id)
        policy_hash = _make_policy_hash(policy_payload)
        pd = PolicyDecision(
            attempt_id=attempt_id,
            effect=effect,
            reason_codes_json=json.dumps(reasons),
            blocking_conditions_json=json.dumps(blocking),
            required_approvals_json=json.dumps(["install"] if effect == "allow_with_approval" else []),
            minimum_verification_tier="tier1_signed" if effect == "allow_with_approval" else "tier0_listed",
            runtime_requirements_json=json.dumps({"runtime_band_max": _json_obj(pv.policy_requirements_json).get("runtime_band_max", "C")}),
            policy_hash=policy_hash,
            created_at=_iso_now(),
        )
        session.add(pd)
        session.commit()
        session.refresh(pd)

        attempt.selected_pack_version_id = pv.id
        attempt.policy_decision_id = pd.id
        attempt.status = InstallAttemptStatus.policy_decided

        winner_impression = session.exec(
            select(CandidateImpression).where(
                CandidateImpression.attempt_id == attempt_id,
                CandidateImpression.pack_version_id == (pv.id or 0),
            )
        ).first()
        if winner_impression:
            winner_impression.selected = True
            session.add(winner_impression)
            session.commit()

        grant: Optional[ApprovalGrant] = None
        if effect == "allow_with_approval":
            grant_id = f"gr_{uuid.uuid4().hex[:14]}"
            expires_at = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
            grant_payload = {
                "grant_id": grant_id,
                "attempt_id": attempt_id,
                "tenant_id": payload.tenant_id,
                "artifact_digest": pv.artifact_digest,
                "pack_version_id": pv.id,
                "allowed_scopes": _json_list(pv.scopes_requested_json),
                "allowed_actions": _json_list(pv.actions_supported_json),
                "runtime_id": payload.runtime_id,
                "runtime_band": payload.runtime_band,
                "expires_at": expires_at,
                "policy_hash": policy_hash,
            }
            grant = ApprovalGrant(
                grant_id=grant_id,
                attempt_id=attempt_id,
                tenant_id=payload.tenant_id,
                approver_id="policy-engine",
                artifact_digest=pv.artifact_digest,
                pack_version_id=pv.id or 0,
                allowed_scopes_json=json.dumps(grant_payload["allowed_scopes"]),
                allowed_actions_json=json.dumps(grant_payload["allowed_actions"]),
                runtime_id=payload.runtime_id,
                runtime_band=payload.runtime_band,
                expires_at=expires_at,
                policy_hash=policy_hash,
                justification="auto-generated approval requirement",
                signature=_policy_sign(grant_payload),
                created_at=_iso_now(),
            )
            session.add(grant)
            session.commit()
            session.refresh(grant)
            attempt.approval_grant_id = grant.id
            attempt.status = InstallAttemptStatus.approval_required
            attempt.install_status = "pending_approval"
        else:
            attempt.install_status = "installed"
            attempt.activation_status = "activated"
            attempt.status = InstallAttemptStatus.activated

        attempt.updated_at = _iso_now()
        session.add(attempt)
        session.commit()

        return {
            "ok": True,
            "attempt_id": attempt_id,
            "task_id": payload.task_id,
            "tenant_id": payload.tenant_id,
            "runtime": {
                "runtime_id": payload.runtime_id,
                "runtime_version": payload.runtime_version,
                "runtime_band": payload.runtime_band,
            },
            "candidate_snapshot_id": candidate_snapshot_id,
            "selected": winner,
            "policy": {
                "decision_id": pd.id,
                "effect": pd.effect,
                "reason_codes": _json_list(pd.reason_codes_json),
                "blocking_conditions": _json_list(pd.blocking_conditions_json),
                "policy_hash": pd.policy_hash,
            },
            "approval_grant": {
                "grant_id": grant.grant_id,
                "expires_at": grant.expires_at,
                "signature": grant.signature,
            } if grant else None,
            "install_status": attempt.install_status,
            "activation_status": attempt.activation_status,
            "status": attempt.status,
        }


@app.post("/agent/action-authorize", response_model=AgentActionAuthorizeResponse)
def agent_action_authorize(payload: AgentActionAuthorizeRequest) -> AgentActionAuthorizeResponse:
    with Session(engine) as session:
        attempt = session.exec(select(InstallAttempt).where(InstallAttempt.attempt_id == payload.attempt_id)).first()
        if not attempt:
            raise HTTPException(status_code=404, detail="attempt not found")
        pv = session.get(PackVersion, payload.pack_version_id)
        if not pv:
            raise HTTPException(status_code=404, detail="pack version not found")
        if pv.artifact_digest != payload.artifact_digest:
            return AgentActionAuthorizeResponse(decision="deny", reason="artifact digest mismatch")

        effect, reasons, blocking = _policy_decide_for_version(
            pv,
            attempt.runtime_band,
            attempt.tenant_id,
            requested_scope=payload.requested_scope,
        )
        if effect == "deny":
            session.add(
                ActionAuthorization(
                    attempt_id=attempt.attempt_id,
                    pack_version_id=payload.pack_version_id,
                    artifact_digest=payload.artifact_digest,
                    requested_action=payload.requested_action,
                    requested_scope=payload.requested_scope,
                    decision="deny",
                    reason_codes_json=json.dumps(reasons + blocking),
                    justification=payload.justification,
                    runtime_attestation_hash=(hashlib.sha256((payload.runtime_attestation or "").encode("utf-8")).hexdigest() if payload.runtime_attestation else None),
                    created_at=_iso_now(),
                )
            )
            session.commit()
            return AgentActionAuthorizeResponse(decision="deny", reason=",".join(reasons + blocking))

        requires_approval = effect == "allow_with_approval" or payload.requested_scope in SENSITIVE_SCOPES
        if requires_approval:
            expires_at = (datetime.now(timezone.utc) + timedelta(minutes=60)).isoformat()
            grant_id = f"gr_{uuid.uuid4().hex[:14]}"
            grant_payload = {
                "grant_id": grant_id,
                "attempt_id": attempt.attempt_id,
                "tenant_id": attempt.tenant_id,
                "artifact_digest": pv.artifact_digest,
                "pack_version_id": pv.id,
                "allowed_scopes": [payload.requested_scope],
                "allowed_actions": [payload.requested_action],
                "runtime_id": attempt.runtime_id,
                "runtime_band": attempt.runtime_band,
                "expires_at": expires_at,
                "policy_hash": _make_policy_hash({"attempt": attempt.attempt_id, "scope": payload.requested_scope, "action": payload.requested_action}),
                "justification": payload.justification,
            }
            sig = _policy_sign(grant_payload)
            grant = ApprovalGrant(
                grant_id=grant_id,
                attempt_id=attempt.attempt_id,
                tenant_id=attempt.tenant_id,
                approver_id="policy-engine",
                artifact_digest=pv.artifact_digest,
                pack_version_id=pv.id or 0,
                allowed_scopes_json=json.dumps([payload.requested_scope]),
                allowed_actions_json=json.dumps([payload.requested_action]),
                runtime_id=attempt.runtime_id,
                runtime_band=attempt.runtime_band,
                expires_at=expires_at,
                policy_hash=grant_payload["policy_hash"],
                justification=payload.justification,
                signature=sig,
                created_at=_iso_now(),
            )
            session.add(grant)
            session.commit()
            session.refresh(grant)

            attempt.approval_grant_id = grant.id
            attempt.updated_at = _iso_now()
            session.add(attempt)
            session.commit()

            session.add(
                ActionAuthorization(
                    attempt_id=attempt.attempt_id,
                    pack_version_id=payload.pack_version_id,
                    artifact_digest=payload.artifact_digest,
                    requested_action=payload.requested_action,
                    requested_scope=payload.requested_scope,
                    decision="allow_with_runtime_proof",
                    reason_codes_json=json.dumps([POLICY_REASON_CODES["APPROVAL_GRANT_ISSUED"]]),
                    grant_id=grant.grant_id,
                    justification=payload.justification,
                    runtime_attestation_hash=(hashlib.sha256((payload.runtime_attestation or "").encode("utf-8")).hexdigest() if payload.runtime_attestation else None),
                    created_at=_iso_now(),
                )
            )
            session.commit()

            grant_token = base64.urlsafe_b64encode(json.dumps({**grant_payload, "signature": sig}).encode("utf-8")).decode("utf-8")
            return AgentActionAuthorizeResponse(
                decision="allow_with_runtime_proof",
                reason="approved with signed grant",
                grant_token=grant_token,
                grant_id=grant.grant_id,
                expires_at=expires_at,
            )

        session.add(
            ActionAuthorization(
                attempt_id=attempt.attempt_id,
                pack_version_id=payload.pack_version_id,
                artifact_digest=payload.artifact_digest,
                requested_action=payload.requested_action,
                requested_scope=payload.requested_scope,
                decision="allow",
                reason_codes_json=json.dumps([POLICY_REASON_CODES["LOW_RISK_CONTEXT"]]),
                justification=payload.justification,
                runtime_attestation_hash=(hashlib.sha256((payload.runtime_attestation or "").encode("utf-8")).hexdigest() if payload.runtime_attestation else None),
                created_at=_iso_now(),
            )
        )
        session.commit()
        return AgentActionAuthorizeResponse(decision="allow", reason="action permitted")


@app.post("/agent/policy-evaluate", response_model=AgentPolicyEvaluateResponse)
def agent_policy_evaluate(payload: AgentPolicyEvaluateRequest) -> AgentPolicyEvaluateResponse:
    with Session(engine) as session:
        pack = session.get(Pack, payload.pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")
        if _requires_approval(pack):
            return AgentPolicyEvaluateResponse(decision="require_approval", reason="risk/scopes require approval")
        return AgentPolicyEvaluateResponse(decision="allow", reason="low-risk pack")


@app.post("/agent/outcome")
def agent_outcome(payload: AgentOutcomeRequest) -> dict:
    with Session(engine) as session:
        pack = session.get(Pack, payload.pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")
        row = AgentOutcome(
            user_id=payload.user_id,
            task_id=payload.task_id,
            runtime=payload.runtime,
            pack_id=payload.pack_id,
            success=payload.success,
            latency_ms=payload.latency_ms,
            error_class=payload.error_class,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return {"ok": True, "outcome_id": row.id}


@app.post("/agent/outcome-v2")
def agent_outcome_v2(payload: AgentOutcomeV2Request) -> dict:
    with Session(engine) as session:
        attempt = session.exec(select(InstallAttempt).where(InstallAttempt.attempt_id == payload.attempt_id)).first()
        if not attempt:
            raise HTTPException(status_code=404, detail="attempt not found")

        pv = session.get(PackVersion, attempt.selected_pack_version_id or 0) if attempt.selected_pack_version_id else None
        allowed_scopes = set()
        if attempt.approval_grant_id:
            grant = session.get(ApprovalGrant, attempt.approval_grant_id)
            if grant:
                allowed_scopes = set(_json_list(grant.allowed_scopes_json))
        if not allowed_scopes and pv:
            allowed_scopes = set(_json_list(pv.scopes_requested_json))

        observed = set(payload.observed_scopes)
        undeclared = sorted(observed - allowed_scopes)
        quarantine = len(undeclared) > 0

        reward = 0.0
        result = payload.result
        if result == "success" and not quarantine and not payload.incident_flag:
            reward = 1.0 if payload.human_intervention == "none" else 0.5
        elif result in {"blocked", "no_improvement", "partial"}:
            reward = 0.0
        elif result == "fail":
            reward = -0.5
        if payload.incident_flag or quarantine:
            reward = -1.0

        out = OutcomeReport(
            attempt_id=payload.attempt_id,
            task_id=payload.task_id,
            tenant_id=payload.tenant_id,
            task_class=payload.task_class,
            selected_pack_version_id=attempt.selected_pack_version_id,
            runtime_id=payload.runtime_id,
            runtime_version=payload.runtime_version,
            result=result,
            error_code=payload.error_code,
            latency_ms=payload.latency_ms,
            human_intervention=payload.human_intervention,
            task_completed_after_install=payload.task_completed_after_install,
            observed_scopes_json=json.dumps(sorted(observed)),
            side_effect_counts_json=json.dumps(payload.side_effect_counts),
            incident_flag=payload.incident_flag or quarantine,
            recovery_action=payload.recovery_action,
            confidence=payload.confidence,
            privacy_mode=payload.privacy_mode,
            reward=reward,
            created_at=_iso_now(),
        )
        session.add(out)

        attempt.status = InstallAttemptStatus.outcome_reported
        if result == "fail":
            attempt.install_status = "failed"
        if quarantine:
            attempt.status = InstallAttemptStatus.failed
            attempt.install_status = "quarantined"
            attempt.activation_status = "quarantined"
            attempt.rollback_status = "requested"
            session.add(
                TrustIncident(
                    attempt_id=attempt.attempt_id,
                    tenant_id=attempt.tenant_id,
                    pack_version_id=attempt.selected_pack_version_id,
                    severity="critical",
                    incident_type="observed_scope_not_subset_allowed",
                    details_json=json.dumps({
                        "allowed_scopes": sorted(allowed_scopes),
                        "observed_scopes": sorted(observed),
                        "undeclared_scopes": undeclared,
                    }),
                    quarantined=True,
                    created_at=_iso_now(),
                )
            )
        attempt.updated_at = _iso_now()
        session.add(attempt)

        # feed observed scopes back to pack version evidence
        if pv and observed:
            prior = set(_json_list(pv.scopes_observed_json))
            pv.scopes_observed_json = json.dumps(sorted(prior.union(observed)))
            session.add(pv)

        session.commit()
        session.refresh(out)

        return {
            "ok": True,
            "outcome_report_id": out.id,
            "attempt_id": payload.attempt_id,
            "reward": reward,
            "quarantined": quarantine,
            "undeclared_scopes": undeclared,
        }


@app.get("/agent/compatibility/{pack_id}")
def agent_compatibility(pack_id: int, runtime: str, version: Optional[str] = None) -> dict:
    _ = version
    with Session(engine) as session:
        pack = session.get(Pack, pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")
        caps = _csv_to_scopes(pack.scopes_csv)
        supported = True if caps else False
        return {
            "pack_id": pack_id,
            "runtime": runtime,
            "status": "native" if supported else "partial",
            "capabilities": caps,
            "requires_approval": _requires_approval(pack),
        }


@app.get("/bot/store", response_model=list[CatalogPack])
def bot_store(user_id: str, type: Optional[PackType] = None, x_botstore_key: Optional[str] = Header(None)) -> list[CatalogPack]:
    _enforce_bot_auth(x_botstore_key)
    _ = user_id  # reserved for personalization in later phases
    return catalog(type=type, featured_only=False)


@app.get("/bot/open-store-link")
def bot_open_store_link(user_id: str, base_url: str = "http://127.0.0.1:8787/", x_botstore_key: Optional[str] = Header(None)) -> dict:
    _enforce_bot_auth(x_botstore_key)
    return {"url": f"{base_url}?user_id={user_id}"}


@app.post("/bot/install", response_model=InstallResult)
def bot_install(payload: BotCommandInstallRequest, x_botstore_key: Optional[str] = Header(None)) -> InstallResult:
    _enforce_bot_auth(x_botstore_key)
    with Session(engine) as session:
        pack = _pack_by_slug(session, payload.pack_slug)
        if not pack:
            raise HTTPException(status_code=404, detail="pack slug not found")
        return _create_install(session, payload.user_id, pack)


@app.post("/bot/install-bundle", response_model=BundleInstallResult)
def bot_install_bundle(payload: BotCommandBundleInstallRequest, x_botstore_key: Optional[str] = Header(None)) -> BundleInstallResult:
    _enforce_bot_auth(x_botstore_key)
    with Session(engine) as session:
        bundle = _pack_by_slug(session, payload.bundle_slug)
        if not bundle:
            raise HTTPException(status_code=404, detail="bundle slug not found")
        if bundle.type != PackType.bundle:
            raise HTTPException(status_code=400, detail="slug is not a bundle")

        child_ids = _csv_to_ints(bundle.bundle_pack_ids_csv)
        installs: list[InstallResult] = [_create_install(session, payload.user_id, bundle)]
        for child_id in child_ids:
            child = session.get(Pack, child_id)
            if not child:
                raise HTTPException(status_code=404, detail=f"bundle child pack not found: {child_id}")
            installs.append(_create_install(session, payload.user_id, child))
        return BundleInstallResult(installs=installs)


@app.get("/bot/installs", response_model=list[Install])
def bot_installs(user_id: str, x_botstore_key: Optional[str] = Header(None)) -> list[Install]:
    _enforce_bot_auth(x_botstore_key)
    return list_installs(user_id=user_id)


@app.get("/bot/approvals", response_model=list[Approval])
def bot_approvals(user_id: str, pending_only: bool = True, x_botstore_key: Optional[str] = Header(None)) -> list[Approval]:
    _enforce_bot_auth(x_botstore_key)
    return list_approvals(user_id=user_id, status=ApprovalStatus.pending if pending_only else None)


@app.post("/bot/command", response_model=BotCommandResponse)
def bot_command(payload: BotCommandRequest, x_botstore_key: Optional[str] = Header(None)) -> BotCommandResponse:
    _enforce_bot_auth(x_botstore_key)
    text = (payload.text or "").strip()
    if not text:
        return BotCommandResponse(message="Empty command", action="help")

    parts = text.split()
    cmd = parts[0].lower()

    if cmd in {"/start", "/store", "/help"}:
        url = bot_open_store_link(user_id=payload.user_id, x_botstore_key=x_botstore_key)["url"]
        featured = [p for p in bot_store(user_id=payload.user_id, x_botstore_key=x_botstore_key) if p.is_featured][:3]

        products_lines = []
        product_buttons = []
        for p in featured:
            label = f"• {p.title} ({p.type.value})"
            suffix = " — approval may be required" if p.requires_approval else ""
            products_lines.append(label + suffix)
            cb = f"bundle:{p.slug}" if p.type == PackType.bundle else f"install:{p.slug}"
            product_buttons.append([{"text": f"Install: {p.title}", "callback_data": cb, "style": "primary"}])

        welcome = "\n".join([
            "👋 Welcome to BotStore — the marketplace for bot skills and personalities.",
            "",
            "🚀 Featured products:",
            *(products_lines or ["• No featured products yet"]),
            "",
            "🧭 Commands:",
            "/store - Open BotStore web view",
            "/install <pack-slug> - Install one product",
            "/bundle <bundle-slug> - Install a full bundle",
            "/approvals - Show pending approvals",
            "/approve <id> - Approve pending install",
            "/reject <id> - Reject pending install",
            "/installs - Show your install count",
            "/link <runtime_id> <agent_id> - Link install target",
            "/where - Show where packs are activated",
            "",
            "Tip: Use /approvals after installs to approve sensitive packs.",
        ])

        buttons = [
            [{"text": "🛍 Open BotStore", "callback_data": f"open:{url}", "style": "primary"}],
            [{"text": "📋 Approvals", "callback_data": "open:approvals", "style": "success"}],
            *product_buttons,
        ]

        return BotCommandResponse(
            message=welcome,
            action="open_store",
            data={"url": url, "buttons": buttons},
        )

    if cmd == "/install":
        if len(parts) < 2:
            return BotCommandResponse(ok=False, message="Usage: /install <pack-slug>", action="help")
        res = bot_install(BotCommandInstallRequest(user_id=payload.user_id, pack_slug=parts[1]), x_botstore_key=x_botstore_key)
        if res.approval_id:
            return BotCommandResponse(message=f"Install pending approval #{res.approval_id}", action="approval_pending", data={"approval_id": res.approval_id})
        with Session(engine) as session:
            act = session.exec(select(InstallActivation).where(InstallActivation.install_id == (res.install.id or 0))).first()
        msg = f"Installed {parts[1]}"
        if act:
            msg += f"\nStatus: {act.status}"
            if act.runtime_id and act.agent_id:
                msg += f"\nTarget: {act.runtime_id} / {act.agent_id}"
            msg += f"\n{act.message}"
        return BotCommandResponse(message=msg, action="installed", data={"install_id": res.install.id})

    if cmd == "/bundle":
        if len(parts) < 2:
            return BotCommandResponse(ok=False, message="Usage: /bundle <bundle-slug>", action="help")
        res = bot_install_bundle(BotCommandBundleInstallRequest(user_id=payload.user_id, bundle_slug=parts[1]), x_botstore_key=x_botstore_key)
        pending = len([x for x in res.installs if x.approval_id])
        installed = len([x for x in res.installs if x.install.status == InstallStatus.installed])
        return BotCommandResponse(message=f"Bundle processed: {installed} installed, {pending} pending approvals", action="bundle_installed")

    if cmd == "/approvals":
        approvals = bot_approvals(user_id=payload.user_id, pending_only=True, x_botstore_key=x_botstore_key)
        if not approvals:
            return BotCommandResponse(message="No pending approvals", action="approvals")
        summary = ", ".join([f"#{a.id}(pack:{a.pack_id})" for a in approvals])
        buttons = [[
            {"text": f"✅ Approve #{a.id}", "callback_data": f"approve:{a.id}", "style": "success"},
            {"text": f"❌ Reject #{a.id}", "callback_data": f"reject:{a.id}", "style": "danger"},
        ] for a in approvals[:5]]
        return BotCommandResponse(message=f"Pending approvals: {summary}", action="approvals", data={"count": len(approvals), "buttons": buttons})

    if cmd == "/approve":
        if len(parts) < 2 or not parts[1].isdigit():
            return BotCommandResponse(ok=False, message="Usage: /approve <approval-id>", action="help")
        approval_id = int(parts[1])
        updated = decide_approval(approval_id, ApprovalDecision(approve=True, note="approved via bot command"))
        return BotCommandResponse(message=f"Approved #{approval_id}", action="approved", data={"approval_id": updated.id})

    if cmd == "/reject":
        if len(parts) < 2 or not parts[1].isdigit():
            return BotCommandResponse(ok=False, message="Usage: /reject <approval-id>", action="help")
        approval_id = int(parts[1])
        updated = decide_approval(approval_id, ApprovalDecision(approve=False, note="rejected via bot command"))
        return BotCommandResponse(message=f"Rejected #{approval_id}", action="rejected", data={"approval_id": updated.id})

    if cmd == "/installs":
        installs = bot_installs(user_id=payload.user_id, x_botstore_key=x_botstore_key)
        return BotCommandResponse(message=f"Total installs: {len(installs)}", action="installs", data={"count": len(installs)})

    if cmd == "/where":
        state = where_installed(user_id=payload.user_id)
        installs = state.get("installs", [])
        if not installs:
            return BotCommandResponse(
                message="No installs yet. Tip: link a target first with /link <runtime_id> <agent_id>",
                action="where",
            )
        lines = ["Where packs are installed:"]
        for row in installs[:10]:
            target = f"{row.get('runtime_id')}/{row.get('agent_id')}" if row.get("runtime_id") else "(not linked)"
            lines.append(f"- {row.get('pack_slug')}: {row.get('activation_status')} → {target}")
        return BotCommandResponse(message="\n".join(lines), action="where", data={"count": len(installs)})

    if cmd == "/link":
        if len(parts) < 3:
            return BotCommandResponse(ok=False, message="Usage: /link <runtime_id> <agent_id>", action="help")
        row = bind_target(
            UserRuntimeBindingCreate(
                user_id=payload.user_id,
                runtime_id=parts[1],
                agent_id=parts[2],
                channel="telegram",
                set_default=True,
            )
        )
        return BotCommandResponse(
            message=f"Linked default install target: {row.runtime_id}/{row.agent_id}",
            action="linked_target",
        )

    # Conversational mode for human users (non-slash)
    if not cmd.startswith("/"):
        suggestion = agent_search(
            AgentSearchQuery(
                user_id=payload.user_id,
                runtime="openclaw",
                query=text,
                missing_capabilities=[],
                constraints=AgentSearchConstraints(risk_max="medium"),
                limit=8,
            )
        )
        raw_results = suggestion.get("results", [])
        # Favor actionable installs for humans: skill/bundle only and query overlap > 0 when possible.
        results = [
            r
            for r in raw_results
            if not (r.get("type") == PackType.personality or str(r.get("type")).endswith("personality"))
        ]
        overlapped = [
            r
            for r in results
            if any(("query term overlap:" in w) and (w.strip() != "query term overlap: 0") for w in r.get("why", []))
        ]
        if overlapped:
            results = overlapped
        results = results[:3]

        if not results:
            return BotCommandResponse(
                message="I couldn't find a confident install match yet. Try wording your goal like: 'triage inbox and schedule meetings' or 'SEO and campaign orchestration'.",
                action="assist_search",
            )

        has_target = False
        with Session(engine) as session:
            has_target = _resolve_binding(session, payload.user_id) is not None

        lines = ["I found these packs for your request:"]
        buttons = []
        for r in results:
            lines.append(f"- {r['title']} ({r['slug']})")
            cb = f"bundle:{r['slug']}" if r.get("type") == PackType.bundle or str(r.get("type")).endswith("bundle") else f"install:{r['slug']}"
            buttons.append([{"text": f"Install {r['title']}", "callback_data": cb, "style": "primary"}])

        if not has_target:
            lines.append("\nBefore installing for live use, link your bot target: /link <runtime_id> <agent_id>")
        lines.append("Use /where to see exactly where installs are activated.")

        return BotCommandResponse(message="\n".join(lines), action="assist_search", data={"buttons": buttons})

    return BotCommandResponse(ok=False, message="Unknown command. Use /store, /install <slug>, /bundle <slug>, /approvals, /approve <id>, /reject <id>, /installs, /where, /link", action="help")


@app.post("/bot/callback", response_model=BotCommandResponse)
def bot_callback(payload: BotCallbackRequest, x_botstore_key: Optional[str] = Header(None)) -> BotCommandResponse:
    _enforce_bot_auth(x_botstore_key)
    data = (payload.callback_data or "").strip()
    if data.startswith("install:"):
        slug = data.split(":", 1)[1]
        return bot_command(BotCommandRequest(user_id=payload.user_id, text=f"/install {slug}"), x_botstore_key=x_botstore_key)
    if data.startswith("bundle:"):
        slug = data.split(":", 1)[1]
        return bot_command(BotCommandRequest(user_id=payload.user_id, text=f"/bundle {slug}"), x_botstore_key=x_botstore_key)
    if data.startswith("approve:"):
        aid = data.split(":", 1)[1]
        return bot_command(BotCommandRequest(user_id=payload.user_id, text=f"/approve {aid}"), x_botstore_key=x_botstore_key)
    if data.startswith("reject:"):
        aid = data.split(":", 1)[1]
        return bot_command(BotCommandRequest(user_id=payload.user_id, text=f"/reject {aid}"), x_botstore_key=x_botstore_key)
    if data == "open:approvals":
        return bot_command(BotCommandRequest(user_id=payload.user_id, text="/approvals"), x_botstore_key=x_botstore_key)
    if data.startswith("open:"):
        url = data.split(":", 1)[1]
        return BotCommandResponse(message=f"Open: {url}", action="open_store", data={"url": url})
    return BotCommandResponse(ok=False, message="Unknown callback", action="help")


def _pack_by_slug(session: Session, slug: str) -> Optional[Pack]:
    return session.exec(select(Pack).where(Pack.slug == slug)).first()


def _resolve_binding(session: Session, user_id: str) -> Optional[UserRuntimeBinding]:
    binding = session.exec(
        select(UserRuntimeBinding).where(
            UserRuntimeBinding.user_id == user_id,
            UserRuntimeBinding.is_default == True,
        )
    ).first()
    if binding:
        return binding
    return session.exec(select(UserRuntimeBinding).where(UserRuntimeBinding.user_id == user_id)).first()


def _upsert_install_activation(
    session: Session,
    install: Install,
    user_id: str,
    runtime_id: Optional[str],
    agent_id: Optional[str],
) -> InstallActivation:
    row = session.exec(select(InstallActivation).where(InstallActivation.install_id == (install.id or 0))).first()
    if not row:
        row = InstallActivation(install_id=install.id or 0, user_id=user_id)

    if runtime_id and agent_id:
        row.runtime_id = runtime_id
        row.agent_id = agent_id
        if install.status == InstallStatus.installed:
            row.status = "activated"
            row.message = f"Activated in runtime '{runtime_id}' for agent '{agent_id}'."
        elif install.status == InstallStatus.pending_approval:
            row.status = "pending_approval"
            row.message = (
                f"Target linked ({runtime_id}/{agent_id}) but activation is waiting for approval."
            )
        else:
            row.status = "installed_registry"
            row.message = f"Linked target ({runtime_id}/{agent_id}); install status is {install.status}."
    else:
        row.status = "installed_registry"
        row.message = "Installed in registry only (no runtime target linked)."

    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def _create_install(
    session: Session,
    user_id: str,
    pack: Pack,
    runtime_id: Optional[str] = None,
    agent_id: Optional[str] = None,
) -> InstallResult:
    needs_approval = _requires_approval(pack)
    status = InstallStatus.pending_approval if needs_approval else InstallStatus.installed
    existing = session.exec(
        select(Install).where(
            Install.user_id == user_id,
            Install.pack_id == (pack.id or 0),
            Install.status.in_([InstallStatus.installed, InstallStatus.pending_approval]),
        )
    ).first()

    approval_id = None
    if existing:
        install = existing
        if install.status == InstallStatus.pending_approval:
            pending = session.exec(
                select(Approval).where(
                    Approval.install_id == (install.id or 0),
                    Approval.status == ApprovalStatus.pending,
                )
            ).first()
            if pending:
                approval_id = pending.id
    else:
        install = Install(
            user_id=user_id,
            pack_id=pack.id or 0,
            version=pack.version,
            status=status,
            approval_required=needs_approval,
        )
        session.add(install)
        session.commit()
        session.refresh(install)

        if needs_approval:
            approval = Approval(install_id=install.id or 0, user_id=user_id, pack_id=pack.id or 0)
            session.add(approval)
            session.commit()
            session.refresh(approval)
            approval_id = approval.id

    if not (runtime_id and agent_id):
        binding = _resolve_binding(session, user_id)
        if binding:
            runtime_id = binding.runtime_id
            agent_id = binding.agent_id

    _upsert_install_activation(session, install, user_id, runtime_id, agent_id)
    install_out = Install(
        id=install.id,
        user_id=user_id,
        pack_id=pack.id or 0,
        version=pack.version,
        status=status,
        approval_required=needs_approval,
    )
    return InstallResult(install=install_out, approval_id=approval_id)


@app.post("/targets/bind", response_model=UserRuntimeBinding)
def bind_target(payload: UserRuntimeBindingCreate) -> UserRuntimeBinding:
    with Session(engine) as session:
        if payload.set_default:
            existing_defaults = session.exec(
                select(UserRuntimeBinding).where(
                    UserRuntimeBinding.user_id == payload.user_id,
                    UserRuntimeBinding.is_default == True,
                )
            ).all()
            for row in existing_defaults:
                row.is_default = False
                session.add(row)

        row = session.exec(
            select(UserRuntimeBinding).where(
                UserRuntimeBinding.user_id == payload.user_id,
                UserRuntimeBinding.runtime_id == payload.runtime_id,
                UserRuntimeBinding.agent_id == payload.agent_id,
            )
        ).first()
        if not row:
            row = UserRuntimeBinding(
                user_id=payload.user_id,
                runtime_id=payload.runtime_id,
                agent_id=payload.agent_id,
                channel=payload.channel,
                is_default=payload.set_default,
            )
        else:
            row.channel = payload.channel
            row.is_default = payload.set_default or row.is_default

        session.add(row)
        session.commit()
        session.refresh(row)

        # Backfill activation visibility for existing installs of this user.
        installs = list(session.exec(select(Install).where(Install.user_id == payload.user_id)).all())
        for ins in installs:
            _upsert_install_activation(session, ins, payload.user_id, row.runtime_id, row.agent_id)

        return row


@app.get("/targets", response_model=list[UserRuntimeBinding])
def list_targets(user_id: str) -> list[UserRuntimeBinding]:
    with Session(engine) as session:
        return list(session.exec(select(UserRuntimeBinding).where(UserRuntimeBinding.user_id == user_id)).all())


@app.get("/where")
def where_installed(user_id: str) -> dict:
    with Session(engine) as session:
        installs = list(session.exec(select(Install).where(Install.user_id == user_id)).all())
        rows = []
        for ins in installs:
            pack = session.get(Pack, ins.pack_id)
            act = session.exec(select(InstallActivation).where(InstallActivation.install_id == (ins.id or 0))).first()
            rows.append(
                {
                    "install_id": ins.id,
                    "pack_slug": pack.slug if pack else None,
                    "pack_title": pack.title if pack else None,
                    "install_status": ins.status,
                    "activation_status": act.status if act else "unknown",
                    "runtime_id": act.runtime_id if act else None,
                    "agent_id": act.agent_id if act else None,
                    "message": act.message if act else "no activation record",
                }
            )
        return {"user_id": user_id, "installs": rows}


@app.post("/installs", response_model=InstallResult)
def install_pack(payload: InstallCreate) -> InstallResult:
    with Session(engine) as session:
        pack = session.get(Pack, payload.pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")
        return _create_install(session, payload.user_id, pack, runtime_id=payload.runtime_id, agent_id=payload.agent_id)


@app.post("/installs/by-slug/{slug}", response_model=InstallResult)
def install_pack_by_slug(slug: str, user_id: str, runtime_id: Optional[str] = None, agent_id: Optional[str] = None) -> InstallResult:
    with Session(engine) as session:
        pack = _pack_by_slug(session, slug)
        if not pack:
            raise HTTPException(status_code=404, detail="pack slug not found")
        return _create_install(session, user_id, pack, runtime_id=runtime_id, agent_id=agent_id)


@app.post("/one-click-install/{pack_id}", response_model=InstallResult)
def one_click_install(pack_id: int, user_id: str = "demo-user") -> InstallResult:
    with Session(engine) as session:
        pack = session.get(Pack, pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")
        return _create_install(session, user_id, pack)


@app.post("/one-click-install-bundle", response_model=BundleInstallResult)
def one_click_install_bundle(payload: BundleInstallCreate) -> BundleInstallResult:
    with Session(engine) as session:
        installs: list[InstallResult] = []
        for pack_id in payload.pack_ids:
            pack = session.get(Pack, pack_id)
            if not pack:
                raise HTTPException(status_code=404, detail=f"pack not found: {pack_id}")
            installs.append(_create_install(session, payload.user_id, pack))
        return BundleInstallResult(installs=installs)


@app.post("/one-click-install-bundle/{bundle_pack_id}", response_model=BundleInstallResult)
def one_click_install_bundle_pack(bundle_pack_id: int, user_id: str = "demo-user") -> BundleInstallResult:
    with Session(engine) as session:
        bundle = session.get(Pack, bundle_pack_id)
        if not bundle:
            raise HTTPException(status_code=404, detail="bundle pack not found")
        if bundle.type != PackType.bundle:
            raise HTTPException(status_code=400, detail="pack is not a bundle")

        child_ids = _csv_to_ints(bundle.bundle_pack_ids_csv)
        if not child_ids:
            raise HTTPException(status_code=400, detail="bundle has no defined child packs")

        installs: list[InstallResult] = []
        installs.append(_create_install(session, user_id, bundle))
        for child_id in child_ids:
            child = session.get(Pack, child_id)
            if not child:
                raise HTTPException(status_code=404, detail=f"bundle child pack not found: {child_id}")
            installs.append(_create_install(session, user_id, child))
        return BundleInstallResult(installs=installs)


@app.post("/installs/{install_id}/rollback", response_model=Install)
def rollback_install(install_id: int) -> Install:
    with Session(engine) as session:
        install = session.get(Install, install_id)
        if not install:
            raise HTTPException(status_code=404, detail="install not found")
        install.status = InstallStatus.rolled_back
        session.add(install)
        session.commit()
        session.refresh(install)
        return install


@app.get("/installs", response_model=list[Install])
def list_installs(user_id: Optional[str] = None) -> list[Install]:
    with Session(engine) as session:
        query = select(Install)
        if user_id:
            query = query.where(Install.user_id == user_id)
        return list(session.exec(query).all())


@app.get("/installs/{install_id}/activation", response_model=InstallActivation)
def get_install_activation(install_id: int) -> InstallActivation:
    with Session(engine) as session:
        row = session.exec(select(InstallActivation).where(InstallActivation.install_id == install_id)).first()
        if not row:
            raise HTTPException(status_code=404, detail="activation record not found")
        return row


@app.get("/installs/{install_id}/setup", response_model=InstallSetup)
def get_install_setup(install_id: int) -> InstallSetup:
    with Session(engine) as session:
        install = session.get(Install, install_id)
        if not install:
            raise HTTPException(status_code=404, detail="install not found")
        setup = session.exec(select(InstallSetup).where(InstallSetup.install_id == install_id)).first()
        if setup:
            return setup
        return InstallSetup(install_id=install_id)


@app.put("/installs/{install_id}/setup", response_model=InstallSetup)
def upsert_install_setup(install_id: int, payload: InstallSetupUpdate) -> InstallSetup:
    with Session(engine) as session:
        install = session.get(Install, install_id)
        if not install:
            raise HTTPException(status_code=404, detail="install not found")

        setup = session.exec(select(InstallSetup).where(InstallSetup.install_id == install_id)).first()
        if not setup:
            setup = InstallSetup(install_id=install_id)

        setup.gmail_connected = payload.gmail_connected
        setup.calendar_connected = payload.calendar_connected
        setup.notion_connected = payload.notion_connected
        setup.slack_connected = payload.slack_connected

        session.add(setup)
        session.commit()
        session.refresh(setup)
        return setup


@app.get("/approvals", response_model=list[Approval])
def list_approvals(user_id: Optional[str] = None, status: Optional[ApprovalStatus] = None) -> list[Approval]:
    with Session(engine) as session:
        query = select(Approval)
        if user_id:
            query = query.where(Approval.user_id == user_id)
        if status:
            query = query.where(Approval.status == status)
        return list(session.exec(query).all())


@app.post("/approvals/{approval_id}/decide", response_model=Approval)
def decide_approval(approval_id: int, payload: ApprovalDecision) -> Approval:
    with Session(engine) as session:
        approval = session.get(Approval, approval_id)
        if not approval:
            raise HTTPException(status_code=404, detail="approval not found")
        if approval.status != ApprovalStatus.pending:
            raise HTTPException(status_code=409, detail="approval already decided")

        install = session.get(Install, approval.install_id)
        if not install:
            raise HTTPException(status_code=404, detail="install not found")

        if payload.approve:
            approval.status = ApprovalStatus.approved
            install.status = InstallStatus.installed
        else:
            approval.status = ApprovalStatus.rejected
            install.status = InstallStatus.denied
        approval.decision_note = payload.note

        session.add(approval)
        session.add(install)
        session.commit()

        # Refresh activation status after approval decision.
        binding = _resolve_binding(session, install.user_id)
        _upsert_install_activation(
            session,
            install,
            install.user_id,
            binding.runtime_id if binding else None,
            binding.agent_id if binding else None,
        )

        session.refresh(approval)
        return approval
