from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryRead)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existing = db.query(Category).filter(Category.name == category_in.name).first()
    if existing:
        raise HTTPException(400, detail="Category already exists")
    cat = Category(name=category_in.name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name).all()


@router.put("/{cat_id}", response_model=CategoryRead)
def update_category(cat_id: int, category_in: CategoryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    cat = db.query(Category).get(cat_id)
    if not cat:
        raise HTTPException(404, detail="Not found")
    cat.name = category_in.name
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{cat_id}")
def delete_category(cat_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    cat = db.query(Category).get(cat_id)
    if not cat:
        raise HTTPException(404, detail="Not found")
    db.delete(cat)
    db.commit()
    return {"detail": "deleted"} 