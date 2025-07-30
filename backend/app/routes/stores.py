from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_admin
from ..database import get_db
from ..models.store import Store
from ..schemas.store import StoreCreate, StoreRead

router = APIRouter(prefix="/stores", tags=["stores"])


@router.post("/", response_model=StoreRead)
def create_store(
    store_in: StoreCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    store = Store(**store_in.dict())
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


@router.get("/", response_model=list[StoreRead])
def list_stores(db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    return db.query(Store).all()


@router.get("/{store_id}", response_model=StoreRead)
def get_store(store_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    store = db.query(Store).get(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.put("/{store_id}", response_model=StoreRead)
def update_store(
    store_id: int,
    store_in: StoreCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    store = db.query(Store).get(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    for field, value in store_in.dict(exclude_unset=True).items():
        setattr(store, field, value)
    db.commit()
    db.refresh(store)
    return store


@router.delete("/{store_id}")
def delete_store(store_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    store = db.query(Store).get(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    db.delete(store)
    db.commit()
    return {"detail": "Deleted"} 