from sqlalchemy import text
from sqlmodel import Session


def get_all_last_inverter_data_fsp01(db: Session):
    query = text(generate_query(1))
    result = db.execute(query)
    return [dict(row._mapping) for row in result]


def get_all_last_inverter_data_fsp02(db: Session):
    query = text(generate_query(2))
    result = db.execute(query)
    return [dict(row._mapping) for row in result]


def generate_query(fsp):
    query = ""

    for inverter in range(1, 21):
        base_query = f"""
        SELECT * FROM (
            SELECT TOP(1)
                inv.E3TimeStamp AS time,
                inv.FieldValue,
                filds.FieldDescription,
                filds.FieldName,
                '{fsp}.{inverter:02d}' AS Inversor
            FROM UFV_FSP{fsp:02d}_BancoDados.dbo.UFV_FSP{fsp:02d}_INV{inverter:02d} AS inv
            INNER JOIN UFV_FSP{fsp:02d}_BancoDados.dbo.UFV_FSP{fsp:02d}_INV{inverter:02d}_Fields AS filds
                ON filds.FieldID = inv.FieldID
            WHERE filds.FieldName LIKE '%FSP-C%-WAA%GW%XQ40%'
            ORDER BY inv.E3TimeStamp DESC
        ) AS sub{fsp}{inverter}

        UNION ALL
        """

        query += base_query

    return query[:-22]
