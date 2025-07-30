from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models.price_history import PriceHistory
from ..schemas.price_history import PriceHistoryRead

router = APIRouter(prefix="/price-history", tags=["price_history"])


@router.get("/", response_model=list[PriceHistoryRead])
def list_price_history(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    query = db.query(PriceHistory)
    if not current_user.is_admin:
        query = query.filter(PriceHistory.user_id == current_user.id)
    return query.order_by(PriceHistory.date.desc()).all() 