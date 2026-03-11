from sqlmodel import Session
from app.main import engine, Pack, PackType

SEED = [
    Pack(slug="gilgamesh-king", title="King Gilgamesh", type=PackType.personality, description="Regal mythic advisor persona", risk_level="low"),
    Pack(slug="inbox-calendar-ops", title="Inbox & Calendar Operator", type=PackType.skill, description="Email/calendar triage and scheduling workflows", risk_level="medium"),
    Pack(slug="research-analyst", title="Research Analyst", type=PackType.skill, description="Search/summarize/citation workflow", risk_level="low"),
]

with Session(engine) as s:
    for p in SEED:
        s.add(p)
    s.commit()

print("Seeded packs")
