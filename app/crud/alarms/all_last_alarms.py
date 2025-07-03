from sqlalchemy import text
from sqlmodel import Session


def get_all_alarms(db: Session):

    query = text(
        f"""
SELECT
  a.Area,
  la.Message,
  la.E3TimeStamp,
  la.InTime
FROM (
  SELECT DISTINCT Area
  FROM GRL_BancoDados.dbo.Alarms
  WHERE AREA LIKE '%FSP02.INV%'
     OR AREA LIKE '%FSP01.INV%'
) AS a
CROSS APPLY (
  SELECT TOP 1
    al.Message,
    al.E3TimeStamp,
    al.InTime
  FROM GRL_BancoDados.dbo.Alarms AS al
  WHERE al.Area = a.Area
    AND al.OutTime = '1899-12-30 00:00:00.000'
    AND (
         al.Message LIKE '%RODANDO'
      OR al.Message LIKE '%INICIANDO'
      OR al.Message LIKE '%FALHA'
      OR al.Message LIKE '%ESPERA'
    )
    AND al.Message NOT LIKE '%PARADO%'
  ORDER BY al.E3TimeStamp DESC
) AS la
ORDER BY a.Area;
    """
    )
    result = db.execute(query)
    return [dict(row._mapping) for row in result]
