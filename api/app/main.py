import os
from enum import Enum
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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


SENSITIVE_SCOPES = {
    "email.send",
    "message.send",
    "social.post",
    "payment.charge",
    "files.delete",
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
    user_id: str
    runtime: str
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


class AgentOutcome(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    task_id: str = Field(index=True)
    runtime: str = Field(index=True)
    pack_id: int = Field(foreign_key="pack.id", index=True)
    success: bool
    latency_ms: Optional[float] = None
    error_class: Optional[str] = None


sqlite_file_name = "./botstore.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=False)

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
        raise HTTPException(status_code=401, detail="unauthorized bot key")


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


def _ints_to_csv(values: list[int]) -> str:
    uniq = sorted({int(v) for v in values if int(v) > 0})
    return ",".join(str(v) for v in uniq)


def _requires_approval(pack: Pack) -> bool:
    scopes = set(_csv_to_scopes(pack.scopes_csv))
    return pack.risk_level.lower() == "high" or bool(scopes.intersection(SENSITIVE_SCOPES))


SEARCH_SYNONYMS = {
    "schedule": ["calendar", "meeting", "timezone"],
    "email": ["inbox", "mail", "reply", "triage"],
    "research": ["source", "citation", "web", "verify"],
    "compliance": ["policy", "audit", "risk", "governance"],
    "coding": ["code", "repo", "pr", "debug"],
    "support": ["ticket", "helpdesk", "customer"],
    "cost": ["budget", "spend", "finops"],
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


def _pack_text_blob(pack: Pack) -> str:
    scopes = " ".join(_csv_to_scopes(pack.scopes_csv))
    return f"{pack.slug} {pack.title} {pack.description} {scopes}"


@app.get("/")
def root() -> FileResponse:
    return FileResponse("../web/index.html")


@app.get("/health")
def health() -> dict:
    return {"ok": True, "version": app.version}


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
        return pack


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
        out: list[CatalogPack] = []
        for p in packs:
            creator = session.get(Creator, p.creator_id) if p.creator_id else None
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
    required = [c.strip() for c in payload.missing_capabilities if c.strip()]
    constraints = payload.constraints or AgentSearchConstraints()

    with Session(engine) as session:
        packs = list(session.exec(select(Pack)).all())
        ranked: list[dict] = []

        for p in packs:
            capability_score = _pack_score_for_capabilities(p, required) if required else 0.0
            pack_tokens = _tokenize(_pack_text_blob(p))
            overlap = len(query_tokens.intersection(pack_tokens))
            text_score = overlap / max(len(query_tokens), 1) if query_tokens else 0.0

            total = capability_score + (0.45 * text_score)

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

        ranked.sort(key=lambda x: x["score"], reverse=True)

        return {
            "query": payload.query,
            "parsed_terms": sorted(query_tokens),
            "required_capabilities": required,
            "constraints": constraints.model_dump(),
            "results": ranked[: max(1, min(payload.limit, 50))],
        }


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
        return BotCommandResponse(message=f"Installed {parts[1]}", action="installed", data={"install_id": res.install.id})

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

    return BotCommandResponse(ok=False, message="Unknown command. Use /store, /install <slug>, /bundle <slug>, /approvals, /approve <id>, /reject <id>, /installs", action="help")


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


def _create_install(session: Session, user_id: str, pack: Pack) -> InstallResult:
    needs_approval = _requires_approval(pack)
    status = InstallStatus.pending_approval if needs_approval else InstallStatus.installed
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

    approval_id = None
    if needs_approval:
        approval = Approval(install_id=install.id or 0, user_id=user_id, pack_id=pack.id or 0)
        session.add(approval)
        session.commit()
        session.refresh(approval)
        approval_id = approval.id
    return InstallResult(install=install, approval_id=approval_id)


@app.post("/installs", response_model=InstallResult)
def install_pack(payload: InstallCreate) -> InstallResult:
    with Session(engine) as session:
        pack = session.get(Pack, payload.pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")
        return _create_install(session, payload.user_id, pack)


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


@app.get("/installs/{install_id}/setup", response_model=InstallSetup)
def get_install_setup(install_id: int) -> InstallSetup:
    with Session(engine) as session:
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
        session.refresh(approval)
        return approval
