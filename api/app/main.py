from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException
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
    creator_id: Optional[int] = Field(default=None, foreign_key="creator.id")


class PackCreate(SQLModel):
    slug: str
    title: str
    type: PackType
    version: str = "0.1.0"
    description: str
    risk_level: str = "low"
    scopes: list[str] = []
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
    requires_approval: bool
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


def _scopes_to_csv(scopes: list[str]) -> str:
    return ",".join(sorted({s.strip() for s in scopes if s.strip()}))


def _csv_to_scopes(scopes_csv: str) -> list[str]:
    if not scopes_csv:
        return []
    return [s.strip() for s in scopes_csv.split(",") if s.strip()]


def _requires_approval(pack: Pack) -> bool:
    scopes = set(_csv_to_scopes(pack.scopes_csv))
    return pack.risk_level.lower() == "high" or bool(scopes.intersection(SENSITIVE_SCOPES))


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
        pack = Pack(
            slug=payload.slug,
            title=payload.title,
            type=payload.type,
            version=payload.version,
            description=payload.description,
            risk_level=payload.risk_level,
            scopes_csv=_scopes_to_csv(payload.scopes),
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
def catalog(type: Optional[PackType] = None) -> list[CatalogPack]:
    with Session(engine) as session:
        query = select(Pack)
        if type:
            query = query.where(Pack.type == type)
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
                    requires_approval=_requires_approval(p),
                    creator_id=p.creator_id,
                    creator_name=creator.name if creator else None,
                    creator_verification=creator.verification if creator else None,
                    creator_trust_score=creator.trust_score if creator else None,
                )
            )
        return out


@app.post("/installs", response_model=InstallResult)
def install_pack(payload: InstallCreate) -> InstallResult:
    with Session(engine) as session:
        pack = session.get(Pack, payload.pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")
        needs_approval = _requires_approval(pack)
        status = InstallStatus.pending_approval if needs_approval else InstallStatus.installed
        install = Install(
            user_id=payload.user_id,
            pack_id=payload.pack_id,
            version=pack.version,
            status=status,
            approval_required=needs_approval,
        )
        session.add(install)
        session.commit()
        session.refresh(install)

        approval_id = None
        if needs_approval:
            approval = Approval(install_id=install.id or 0, user_id=payload.user_id, pack_id=pack.id or 0)
            session.add(approval)
            session.commit()
            session.refresh(approval)
            approval_id = approval.id
        return InstallResult(install=install, approval_id=approval_id)


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
