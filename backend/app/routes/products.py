from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, asc, desc
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.product import Product
from ..models.price_history import PriceHistory
from ..schemas.product import ProductRead

router = APIRouter(prefix="/products", tags=["products"])


def _recent_price_subquery(db: Session):
    subq = (
        db.query(
            PriceHistory.product_id.label("pid"),
            func.max(PriceHistory.date).label("latest_date"),
        )
        .group_by(PriceHistory.product_id)
        .subquery()
    )
    return subq


@router.get("/", response_model=List[ProductRead])
def list_products(
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None),
):
    subq = _recent_price_subquery(db)
    q = db.query(Product).join(subq, Product.id == subq.c.pid, isouter=True)
    if category_id:
        q = q.filter(Product.category_id == category_id)
    return q.order_by(Product.name).all()


@router.get("/{product_id}")
def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        return {"detail": "Not found"}
    histories = (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.date.desc())
        .all()
    )
    return {
        "product": ProductRead.from_orm(product),
        "histories": histories,
    } 