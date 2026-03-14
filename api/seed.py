import json
from pathlib import Path

from sqlmodel import SQLModel, Session, select

from app.main import Creator, Pack, PackType, VerificationStatus, engine

SQLModel.metadata.create_all(engine)

with Session(engine) as s:
    creators = {
        "Epic Labs": Creator(name="Epic Labs", verification=VerificationStatus.verified, trust_score=0.93),
        "Ops Foundry": Creator(name="Ops Foundry", verification=VerificationStatus.verified, trust_score=0.89),
        "Scholar Guild": Creator(name="Scholar Guild", verification=VerificationStatus.unverified, trust_score=0.74),
    }

    for name, creator in creators.items():
        existing = s.exec(select(Creator).where(Creator.name == name)).first()
        if not existing:
            s.add(creator)
    s.commit()

    creator_map = {c.name: c for c in s.exec(select(Creator)).all()}

    seed = [
        Pack(
            slug="gilgamesh-king",
            title="King Gilgamesh",
            type=PackType.personality,
            description="Regal mythic advisor persona",
            risk_level="low",
            scopes_csv="memory.read,memory.write",
            is_featured=True,
            creator_id=creator_map["Epic Labs"].id,
        ),
        Pack(
            slug="inbox-calendar-ops",
            title="Inbox & Calendar Operator",
            type=PackType.skill,
            description="Email/calendar triage and scheduling workflows",
            risk_level="medium",
            scopes_csv="calendar.read,calendar.write,email.read,email.send",
            is_featured=True,
            creator_id=creator_map["Ops Foundry"].id,
        ),
        Pack(
            slug="research-analyst",
            title="Research Analyst",
            type=PackType.skill,
            description="Search/summarize/citation workflow",
            risk_level="low",
            scopes_csv="web.search,web.fetch,files.read",
            creator_id=creator_map["Scholar Guild"].id,
        ),
        Pack(
            slug="founder-command-bundle",
            title="Founder Command Bundle",
            type=PackType.bundle,
            description="One-click starter stack: chief-of-staff behavior + inbox/calendar + research",
            risk_level="medium",
            scopes_csv="calendar.read,calendar.write,email.read,email.send,web.search,web.fetch",
            is_featured=True,
            creator_id=creator_map["Ops Foundry"].id,
        ),
        Pack(
            slug="capability-discovery-engine",
            title="Capability Discovery Engine",
            type=PackType.skill,
            description="Detect missing capabilities and suggest/install matching packs.",
            risk_level="low",
            scopes_csv="memory.read,memory.write,web.search",
            creator_id=creator_map["Ops Foundry"].id,
        ),
        Pack(
            slug="universal-connector-auth",
            title="Universal Connector Auth",
            type=PackType.skill,
            description="OAuth/session lifecycle and connector health checks across core services.",
            risk_level="medium",
            scopes_csv="files.read,files.write,email.read,calendar.read",
            creator_id=creator_map["Ops Foundry"].id,
        ),
        Pack(
            slug="browser-operator-pro",
            title="Browser Operator Pro",
            type=PackType.skill,
            description="Resilient browser automation with retries and human-handoff fallbacks.",
            risk_level="medium",
            scopes_csv="web.fetch,web.search,files.write",
            creator_id=creator_map["Ops Foundry"].id,
        ),
        Pack(
            slug="memory-architect",
            title="Memory Architect",
            type=PackType.skill,
            description="Structured long-term memory schemas, summarization, and retrieval policies.",
            risk_level="low",
            scopes_csv="memory.read,memory.write,files.read,files.write",
            creator_id=creator_map["Scholar Guild"].id,
        ),
        Pack(
            slug="approval-policy-brain",
            title="Approval & Policy Brain",
            type=PackType.skill,
            description="Risk evaluation and human-approval routing for sensitive actions.",
            risk_level="high",
            scopes_csv="payment.charge,social.post,files.delete,message.send",
            creator_id=creator_map["Ops Foundry"].id,
        ),
        Pack(
            slug="task-decomposer",
            title="Task Decomposer",
            type=PackType.skill,
            description="Breaks complex requests into executable steps with checkpointed state.",
            risk_level="low",
            scopes_csv="memory.read,memory.write,files.write",
            creator_id=creator_map["Scholar Guild"].id,
        ),
        Pack(
            slug="error-recovery-self-heal",
            title="Error Recovery Self-Heal",
            type=PackType.skill,
            description="Classifies failures and applies targeted retry/recovery strategies.",
            risk_level="low",
            scopes_csv="files.read,files.write,memory.write",
            creator_id=creator_map["Ops Foundry"].id,
        ),
        Pack(
            slug="quality-eval-gate",
            title="Quality Eval Gate",
            type=PackType.skill,
            description="Validates output quality and source trust before final delivery.",
            risk_level="low",
            scopes_csv="web.search,web.fetch,files.read",
            creator_id=creator_map["Scholar Guild"].id,
        ),
        Pack(
            slug="multi-agent-orchestrator",
            title="Multi-Agent Orchestrator",
            type=PackType.skill,
            description="Coordinates specialist sub-agents and merges outputs safely.",
            risk_level="medium",
            scopes_csv="memory.read,memory.write,message.send,files.write",
            creator_id=creator_map["Ops Foundry"].id,
        ),
        Pack(
            slug="service-ops-verticals",
            title="Service Ops Vertical Starter",
            type=PackType.skill,
            description="Starter workflows for sales ops, legal intake, research, and finance admin.",
            risk_level="medium",
            scopes_csv="email.read,email.send,calendar.read,calendar.write,files.read,files.write",
            creator_id=creator_map["Ops Foundry"].id,
        ),
    ]

    for p in seed:
        existing = s.exec(select(Pack).where(Pack.slug == p.slug)).first()
        if not existing:
            s.add(p)
    s.commit()

    by_slug = {p.slug: p for p in s.exec(select(Pack)).all()}
    bundle = by_slug.get("founder-command-bundle")
    gil = by_slug.get("gilgamesh-king")
    inbox = by_slug.get("inbox-calendar-ops")
    research = by_slug.get("research-analyst")
    if bundle and gil and inbox and research:
        bundle.bundle_pack_ids_csv = f"{gil.id},{inbox.id},{research.id}"
        s.add(bundle)
        s.commit()

    candidates_path = Path(__file__).resolve().parents[1] / "research" / "candidate-packs-v1.json"
    simulation_result_path = Path(__file__).resolve().parents[1] / "research" / "runtime-simulation-result.json"
    if candidates_path.exists():
        payload = json.loads(candidates_path.read_text())
        candidates = payload.get("candidates", [])

        verified_slugs = None
        if simulation_result_path.exists():
            sim = json.loads(simulation_result_path.read_text())
            verified_slugs = set(sim.get("verified_slugs", []))

        for c in candidates:
            slug = c["slug"]
            if verified_slugs is not None and slug not in verified_slugs:
                continue

            existing = s.exec(select(Pack).where(Pack.slug == slug)).first()
            if existing:
                continue

            ptype = PackType(c["type"])
            creator_id = creator_map["Ops Foundry"].id if ptype == PackType.skill else creator_map["Epic Labs"].id
            pack = Pack(
                slug=slug,
                title=c["title"],
                type=ptype,
                description=c["problem"],
                risk_level=c.get("risk_level", "low"),
                scopes_csv=",".join(c.get("scopes", [])),
                is_featured=False,
                creator_id=creator_id,
            )
            s.add(pack)
        s.commit()

print("Seed complete")
