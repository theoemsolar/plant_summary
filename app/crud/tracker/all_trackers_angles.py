from sqlalchemy import text
from sqlmodel import Session


def get_all_tracker_last_position(db: Session):
    query = text(generate_query(1))
    result = db.execute(query)
    return [dict(row._mapping) for row in result]


def generate_query(fsp):
    query = ""

    for tcu in range(1, 81):
        base_query = f"""
            SELECT * FROM (
            SELECT TOP(1) tracker.E3TimeStamp, tracker.FieldValue, fields.FieldName, '{tcu:02d}' as UTC
            FROM UFV_BancoDados.dbo.UFV_FSP_TCU{tcu:02d} AS tracker
            INNER JOIN UFV_BancoDados.dbo.UFV_FSP_TCU{tcu:02d}_Fields as fields
            ON tracker.FieldID = fields.FieldID 
            WHERE fields.FieldName like '%FSP-C%-WAA%GJ%XQ77%'
            ORDER BY tracker.E3TimeStamp DESC
            ) AS TCU{tcu:02d}
            UNION ALL
        """

        query += base_query

    return query[:-22]
