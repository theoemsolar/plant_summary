from sqlalchemy import text
from sqlmodel import Session


def get_ufv_inv_dynamic(db: Session, inv_number: int, skip: int = 0, limit: int = 100):
    if inv_number < 1 or inv_number > 99:
        raise ValueError("Invalid inverter number")

    table_name = f"UFV_FSP01_INV{inv_number:02d}"
    query = text(
        f"""
        SELECT TOP (:limit) inv.E3TimeStamp, inv.FieldValue
        FROM UFV_FSP01_INV{inv_number:02d}_Fields as fields
        INNER JOIN UFV_FSP01_INV{inv_number:02d} as inv ON fields.FieldID = inv.FieldID
        WHERE fields.FieldName = 'UFV_FSP01_Comunicacao.CLP1.INV{inv_number:02d}.[FSP-C01-WAA01GW{inv_number:03d}XQ13]'
        ORDER BY inv.E3TimeStamp DESC
    """
    )

    result = db.execute(query, {"skip": skip, "limit": limit})
    return [dict(row._mapping) for row in result]
