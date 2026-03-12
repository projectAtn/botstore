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
    ]

    for p in seed:
        existing = s.exec(select(Pack).where(Pack.slug == p.slug)).first()
        if not existing:
            s.add(p)
    s.commit()

print("Seed complete")
