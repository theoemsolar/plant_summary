from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class UfvFspInv_fps02(SQLModel, table=True):
    __tablename__ = "UFV_FSP02_INV01"
    __table_args__ = {"schema": "dbo"}

    E3TimeStamp: datetime = Field(primary_key=True)
    FieldID: Optional[int] = Field(default=None)
    Quality: Optional[int] = Field(default=None)
    FieldValue: Optional[float] = Field(default=None)
