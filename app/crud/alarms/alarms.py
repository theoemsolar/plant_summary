from sqlalchemy import text
from sqlmodel import Session
from datetime import datetime
from app.models.alarm import Alarm


def get_alarms(
    db: Session,
    fsp: int,
    inv_number: int,
    initial_date: datetime,
    final_date: datetime,
    skip: int = 0,
    limit: int = 100,
) -> list[Alarm]:

    query = text(
        f"""
    SELECT TOP (:limit) *,
        CASE 
            WHEN OutTime = '1899-12-30 00:00:00.000' THEN NULL
            ELSE OutTime
        END AS OutTimeAdjusted  FROM GRL_BancoDados.dbo.Alarms
    WHERE AREA LIKE '%FSP{fsp:02d}.INV{inv_number:02d}' 
    AND InTime  BETWEEN '{initial_date}' AND '{final_date}'
    ORDER BY E3TimeStamp DESC;
    """
    )

    result = db.execute(query, {"skip": skip, "limit": limit})
    return [dict(row._mapping) for row in result]
