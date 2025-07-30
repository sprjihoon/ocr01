from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_admin
from ..models.log import Log
from ..schemas.log import LogRead

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/", response_model=list[LogRead])
def list_logs(db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    return db.query(Log).order_by(Log.timestamp.desc()).limit(1000).all() 