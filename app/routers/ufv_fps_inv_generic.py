from typing import List
from sqlmodel import Session
from app.dependencies.db_selector import get_db, get_db_fsp01, get_db_fsp02
from fastapi import APIRouter, Depends, HTTPException, Query, Path

from app.crud import (
    get_ufv_inv_dynamic,
    get_ufv_inv_dynamic_fps02,
    get_all_last_inverter_data_fsp01,
    get_all_last_inverter_data_fsp02,
    get_last_inerter_metric_fsp01,
    get_last_inerter_metric_fsp02,
)

router = APIRouter(prefix="/ufv", tags=["ufv"])


@router.get("/{system}/inverter/{inv_number}", response_model=List[dict])
def read_inverter_dynamic(
    *,
    system: str,
    inv_number: int = Path(..., ge=1, le=99),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    try:
        if system == "fsp01":
            return get_ufv_inv_dynamic(db, inv_number, skip=skip, limit=limit)
        elif system == "fsp02":
            return get_ufv_inv_dynamic_fps02(db, inv_number, skip=skip, limit=limit)
        else:
            raise HTTPException(status_code=400, detail="Invalid system type")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metric/generation/all", response_model=List[dict])
def read_all_inverter(
    *, db1: Session = Depends(get_db_fsp01), db2: Session = Depends(get_db_fsp02)
):

    try:
        data_fsp01 = get_all_last_inverter_data_fsp01(db1)
        data_fsp02 = get_all_last_inverter_data_fsp02(db2)
        return data_fsp01 + data_fsp02
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metric/{system}/{inv_number}", response_model=List[dict])
def read_inverter_dynamic(
    *,
    system: str,
    inv_number: int = Path(..., ge=1, le=99),
    db1: Session = Depends(get_db_fsp01),
    db2: Session = Depends(get_db_fsp02),
):
    try:
        if system == "fsp01":
            return get_last_inerter_metric_fsp01(db1, inv_number)
        elif system == "fsp02":
            return get_last_inerter_metric_fsp02(db2, inv_number)
        else:
            raise HTTPException(status_code=400, detail="Invalid system type")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
