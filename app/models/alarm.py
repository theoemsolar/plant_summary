from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Alarm(SQLModel, table=True):
    __tablename__ = "Alarms"
    __table_args__ = {"schema": "dbo"}

    E3TimeStamp: datetime = Field(primary_key=True)
    Acked: int
    ActiveSource: int
    ActorID: Optional[str] = None
    AlarmSourceName: Optional[str] = None
    Area: Optional[str] = None
    ConditionActive: int
    ConditionName: Optional[str] = None
    CurrentValue: float
    EventCLSID: Optional[str] = None
    EventTimeDbl: float
    EventType: Optional[str] = None
    FormattedValue: Optional[str] = None
    FullAlarmSourceName: Optional[str] = None
    InTime: Optional[datetime] = None
    Message: Optional[str] = None
    OutTime: Optional[datetime] = None
    Quality: Optional[str] = None
    Severity: Optional[str] = None
    Source: Optional[str] = None
