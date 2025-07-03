from sqlalchemy import text
from sqlmodel import Session


def get_last_inerter_metric_fsp01(db: Session, inv_number: int):
    if inv_number < 1 or inv_number > 20:
        raise ValueError("Invalid inverter number")

    query = text(
        f"""
        WITH Metrics AS (
          SELECT * FROM (VALUES
            ('POTÊNCIA ATIVA NOMINAL',    '%POTÊNCIA ATIVA NOMINAL%'),
            ('ENERGIA DIÁRIA GERADA',      '%ENERGIA DIÁRIA GERADA%'),
            ('POTÊNCIA REATIVA TOTAL',     '%POTÊNCIA REATIVA TOTAL%'),
            ('TEMPERATURA INTERNA',        '%TEMPERATURA INTERNA%'),
            ('POTÊNCIA REATIVA NOMINAL',   '%POTÊNCIA REATIVA NOMINAL%'),
            ('POTÊNCIA ATIVA TOTAL',       '%POTÊNCIA ATIVA TOTAL%'),
            ('TEMPO DE OPERAÇÃO DIÁRIA',   '%TEMPO DE OPERAÇÃO DIÁRIA%')
          ) AS m(Metric, Pattern)
        )
        SELECT
          m.Metric,
          x.TimeStamp,
          x.Value
        FROM Metrics AS m
        CROSS APPLY (
          SELECT TOP(1)
            inv.E3TimeStamp AS TimeStamp,
            inv.FieldValue  AS Value
          FROM UFV_FSP01_BancoDados.dbo.UFV_FSP01_INV{inv_number:02d} AS inv
          INNER JOIN UFV_FSP01_BancoDados.dbo.UFV_FSP01_INV{inv_number:02d}_Fields AS f
            ON f.FieldID = inv.FieldID
          WHERE f.FieldDescription LIKE m.Pattern
          ORDER BY inv.E3TimeStamp DESC
        ) AS x
        ORDER BY m.Metric
    """
    )

    result = db.execute(
        query,
    )
    return [dict(row._mapping) for row in result]


def get_last_inerter_metric_fsp02(db: Session, inv_number: int):
    if inv_number < 1 or inv_number > 20:
        raise ValueError("Invalid inverter number")

    query = text(
        f"""
        WITH Metrics AS (
          SELECT * FROM (VALUES
            ('POTÊNCIA ATIVA NOMINAL',    '%POTÊNCIA ATIVA NOMINAL%'),
            ('ENERGIA DIÁRIA GERADA',      '%ENERGIA DIÁRIA GERADA%'),
            ('POTÊNCIA REATIVA TOTAL',     '%POTÊNCIA REATIVA TOTAL%'),
            ('TEMPERATURA INTERNA',        '%TEMPERATURA INTERNA%'),
            ('POTÊNCIA REATIVA NOMINAL',   '%POTÊNCIA REATIVA NOMINAL%'),
            ('POTÊNCIA ATIVA TOTAL',       '%POTÊNCIA ATIVA TOTAL%'),
            ('TEMPO DE OPERAÇÃO DIÁRIA',   '%TEMPO DE OPERAÇÃO DIÁRIA%')
          ) AS m(Metric, Pattern)
        )
        SELECT
          m.Metric,
          x.TimeStamp,
          x.Value
        FROM Metrics AS m
        CROSS APPLY (
          SELECT TOP(1)
            inv.E3TimeStamp AS TimeStamp,
            inv.FieldValue  AS Value
          FROM UFV_FSP02_BancoDados.dbo.UFV_FSP02_INV{inv_number:02d} AS inv
          INNER JOIN UFV_FSP02_BancoDados.dbo.UFV_FSP02_INV{inv_number:02d}_Fields AS f
            ON f.FieldID = inv.FieldID
          WHERE f.FieldDescription LIKE m.Pattern
          ORDER BY inv.E3TimeStamp DESC
        ) AS x
        ORDER BY m.Metric
    """
    )

    result = db.execute(
        query,
    )
    return [dict(row._mapping) for row in result]
