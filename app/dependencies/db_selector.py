from fastapi import HTTPException, Path
from sqlmodel import Session
from app.database import get_session_ufv_fsp01, get_session_ufv_fsp02


def get_db(system: str = Path(...)) -> Session:
    if system == "fsp01":
        return next(get_session_ufv_fsp01())
    elif system == "fsp02":
        return next(get_session_ufv_fsp02())
    else:
        raise HTTPException(status_code=400, detail="Invalid system type")


def get_db_fsp01() -> Session:
    yield from get_session_ufv_fsp01()


def get_db_fsp02() -> Session:
    yield from get_session_ufv_fsp02()
