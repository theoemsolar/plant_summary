from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, Path

from sqlmodel import Session
from app.models.tracker import Tracker
from app.database import get_session_ufv
from app.crud import (
    get_all_tracker_last_position,
    get_all_tracker_historical_position,
    get_all_tracker_alarms,
)


router = APIRouter(prefix="/tracker", tags=["tracker"])


@router.get("/all", response_model=List[Tracker], response_model_exclude_none=True)
def read_last_alarms(*, db: Session = Depends(get_session_ufv)):
    return get_all_tracker_last_position(db)


@router.get("/all/alarm")
def read_last_alarms(*, db: Session = Depends(get_session_ufv)):
    return get_all_tracker_alarms(db)


@router.get(
    "/{tcu}/historical", response_model=List[Tracker], response_model_exclude_none=True
)
def read_last_alarms(
    *,
    db: Session = Depends(get_session_ufv),
    tcu: int = Path(..., ge=1, le=80),
):
    return get_all_tracker_historical_position(db, tcu)
