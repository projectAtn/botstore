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
    installed = "installed"
    rolled_back = "rolled_back"


class Pack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    title: str
    type: PackType
    version: str = "0.1.0"
    description: str
    risk_level: str = "low"


class PackCreate(SQLModel):
    slug: str
    title: str
    type: PackType
    version: str = "0.1.0"
    description: str
    risk_level: str = "low"


class Install(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    pack_id: int = Field(foreign_key="pack.id")
    version: str
    status: InstallStatus = InstallStatus.installed


class InstallCreate(SQLModel):
    user_id: str
    pack_id: int


sqlite_file_name = "./botstore.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=False)

app = FastAPI(title="BotStore API", version="0.1.0")
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


@app.get("/")
def root() -> FileResponse:
    return FileResponse("../web/index.html")


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/packs", response_model=Pack)
def create_pack(payload: PackCreate) -> Pack:
    with Session(engine) as session:
        existing = session.exec(select(Pack).where(Pack.slug == payload.slug)).first()
        if existing:
            raise HTTPException(status_code=409, detail="slug already exists")
        pack = Pack.model_validate(payload)
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


@app.post("/installs", response_model=Install)
def install_pack(payload: InstallCreate) -> Install:
    with Session(engine) as session:
        pack = session.get(Pack, payload.pack_id)
        if not pack:
            raise HTTPException(status_code=404, detail="pack not found")
        install = Install(user_id=payload.user_id, pack_id=payload.pack_id, version=pack.version)
        session.add(install)
        session.commit()
        session.refresh(install)
        return install


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
