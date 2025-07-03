from sqlalchemy import text
from sqlmodel import Session


def get_all_tracker_historical_position(db: Session, tcu: int):
    query = text(
        f"""
                SELECT  
                    tracker.E3TimeStamp, 
                    tracker.FieldValue, 
                    fields.FieldName, 
                    '{tcu:02d}' AS TCU
                FROM UFV_BancoDados.dbo.UFV_FSP_TCU{tcu:02d} AS tracker
                INNER JOIN UFV_BancoDados.dbo.UFV_FSP_TCU{tcu:02d}_Fields AS fields
                    ON tracker.FieldID = fields.FieldID 
                WHERE 
                    fields.FieldName LIKE '%FSP-C%-WAA%GJ%XQ77%'
                    AND CAST(DATEADD(DAY, tracker.E3TimeStamp, '1899-12-30') AS DATE) = CAST(GETDATE() AS DATE)
            """
    )
    result = db.execute(query)
    return [dict(row._mapping) for row in result]
