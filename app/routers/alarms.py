from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlmodel import Session
from app.models.alarm import Alarm
from app.database import get_session_grl
from app.crud import get_alarms, get_all_alarms


router = APIRouter(prefix="/alarms", tags=["alarms"])


@router.get("/{fsp}/{inv}", response_model=List[Alarm])
def read_alarms(
    *,
    fsp: int,
    inv: int,
    db: Session = Depends(get_session_grl),
    initial_time: Optional[datetime] = Query(
        None, description="ISO 8601 timestamp for the start of the interval"
    ),
    final_time: Optional[datetime] = Query(
        None, description="ISO 8601 timestamp for the end of the interval"
    ),
    skip: int = Query(0, ge=0, description="Number of rows to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max rows to return"),
):

    try:
        if initial_time is None:
            initial_time = (datetime.now() - timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
        if final_time is None:
            final_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        return get_alarms(
            db,
            fsp=fsp,
            inv_number=inv,
            initial_date=initial_time,
            final_date=final_time,
            skip=skip,
            limit=limit,
        )
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get("/all", response_model=List[Alarm], response_model_exclude_none=True)
def read_last_alarms(*, db: Session = Depends(get_session_grl)):
    return get_all_alarms(db)
