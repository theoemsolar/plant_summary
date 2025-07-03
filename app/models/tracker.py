from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Tracker(SQLModel, table=True):
    __tablename__ = "UFV_FSP_TCU01"
    __table_args__ = {"schema": "dbo"}

    E3TimeStamp: datetime = Field(primary_key=True)
    FieldValue: Optional[float] = Field(default=None)
    FieldName: Optional[str] = Field(default=None)
    UTC: Optional[int] = Field(default=None)
