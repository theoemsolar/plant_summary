from sqlmodel import Session
from datetime import datetime
from app.models.alarm import Alarm


def get_alarm(db: Session, ts: datetime) -> Alarm | None:
    return db.get(Alarm, ts)
