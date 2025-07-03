from sqlalchemy import text
from sqlmodel import Session


def get_all_tracker_alarms(db: Session):
    query = text(
        """
WITH UltimosAlarmes AS (
    SELECT 
        Area,
        ConditionActive,
        Message,
        E3TimeStamp,
        
        SUBSTRING(Area, CHARINDEX('TCU', Area), 6) AS TCU,

        ROW_NUMBER() OVER (PARTITION BY Area, AlarmSourceName ORDER BY E3TimeStamp DESC) AS rn
    FROM 
        GRL_BancoDados.dbo.Alarms WITH (NOLOCK)
    WHERE 
    	AREA LIKE '%TCU%' AND 
        (AlarmSourceName LIKE '%M11%'
        OR AlarmSourceName LIKE '%M92%'
        OR AlarmSourceName LIKE '%M06%'
        OR AlarmSourceName LIKE '%M04%')
)

SELECT 
    TCU,
    Area,
    ConditionActive,
    Message,
    E3TimeStamp
FROM 
    UltimosAlarmes
WHERE 
    rn = 1
    AND ConditionActive = 1
ORDER BY 
    TCU, Area;
            """
    )
    result = db.exec(query)
    return [dict(row._mapping) for row in result]
