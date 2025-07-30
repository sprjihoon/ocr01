from datetime import date, timedelta

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, Form
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..services.storage import upload_image as _upload_image, create_presigned_post, s3_client, S3_BUCKET
from ..services.ocr import run_ocr
from ..services.logger import create_log
from ..models.image import Image
from ..models.price_history import PriceHistory
from ..schemas.image import ImageRead, PresignedRequest, PresignedResponse, ImageComplete
from ..models.product import Product

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
async def upload_image_endpoint(
    store_id: int = Form(...),
    zone: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    # Upload to storage
    image_url = _upload_image(file)

    # Persist image record
    image = Image(
        user_id=current_user.id,
        store_id=store_id,
        image_url=image_url,
        zone=zone,
    )
    db.add(image)
    db.commit()
    db.refresh(image)

    # OCR processing
    try:
        ocr_results = run_ocr(await file.read())
    except Exception as exc:
        create_log(db, current_user.id, "ocr_failure", {"error": str(exc)})
        raise HTTPException(status_code=500, detail="OCR processing failed")

    for item in ocr_results:
        ph = PriceHistory(
            image_id=image.id,
            user_id=current_user.id,
            store_id=store_id,
            date=date.today(),
            product_code=item.get("product_code"),
            product_name=item["product_name"],
            price=item["price"],
            event_info=item.get("event_info"),
        )
        db.add(ph)
        db.flush()  # assigned id

        # Compute badges
        last7 = db.query(PriceHistory).filter(
            PriceHistory.product_name == ph.product_name,
            PriceHistory.date >= date.today() - timedelta(days=7),
            PriceHistory.store_id == store_id,
        ).order_by(PriceHistory.price).first()
        last30 = db.query(PriceHistory).filter(
            PriceHistory.product_name == ph.product_name,
            PriceHistory.date >= date.today() - timedelta(days=30),
            PriceHistory.store_id == store_id,
        ).order_by(PriceHistory.price).first()
        ph_badge7 = last7 is None or ph.price <= last7.price
        ph_badge30 = last30 is None or ph.price <= last30.price
        ph.badge7 = ph_badge7  # type: ignore
        ph.badge30 = ph_badge30  # type: ignore
    db.commit()

    create_log(db, current_user.id, "image_upload", {"image_id": image.id})
    return image


@router.post("/presigned", response_model=PresignedResponse)
def generate_presigned(
    req: PresignedRequest,
    current_user=Depends(get_current_user),
):
    key, presigned = create_presigned_post(req.filename)
    return {
        "key": key,
        "url": presigned["url"],
        "fields": presigned["fields"],
    }


@router.post("/complete", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
def complete_upload(
    payload: ImageComplete,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Fetch image bytes from S3 to run OCR
    try:
        obj = s3_client.get_object(Bucket=S3_BUCKET, Key=payload.key)
        image_bytes = obj["Body"].read()
    except Exception as exc:
        raise HTTPException(500, detail="Failed to fetch uploaded image") from exc

    # Run OCR
    try:
        ocr_results = run_ocr(image_bytes)
    except Exception as exc:
        create_log(db, current_user.id, "ocr_failure", {"error": str(exc)})
        raise HTTPException(status_code=500, detail="OCR processing failed")

    image = Image(
        user_id=current_user.id,
        store_id=payload.store_id,
        image_url=payload.image_url,
        zone=payload.zone,
    )
    db.add(image)
    db.flush()

    from datetime import date, timedelta

    for item in ocr_results:
        # Ensure product exists
        product = db.query(Product).filter(Product.name == item["product_name"]).first()
        if not product:
            product = Product(name=item["product_name"])  # category unknown
            db.add(product)
            db.flush()

        ph = PriceHistory(
            image_id=image.id,
            user_id=current_user.id,
            store_id=payload.store_id,
            date=date.today(),
            product_id=product.id,
            product_code=item.get("product_code"),
            product_name=item["product_name"],
            price=item["price"],
            event_info=item.get("event_info"),
        )
        db.add(ph)
        db.flush()
        last7 = db.query(PriceHistory).filter(
            PriceHistory.product_name == ph.product_name,
            PriceHistory.date >= date.today() - timedelta(days=7),
            PriceHistory.store_id == payload.store_id,
        ).order_by(PriceHistory.price).first()
        last30 = db.query(PriceHistory).filter(
            PriceHistory.product_name == ph.product_name,
            PriceHistory.date >= date.today() - timedelta(days=30),
            PriceHistory.store_id == payload.store_id,
        ).order_by(PriceHistory.price).first()
        ph.badge7 = last7 is None or ph.price <= last7.price
        ph.badge30 = last30 is None or ph.price <= last30.price
    db.commit()
    create_log(db, current_user.id, "image_upload", {"image_id": image.id})
    db.refresh(image)
    return image


@router.get("/", response_model=list[ImageRead])
def list_images(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    query = db.query(Image)
    if not current_user.is_admin:
        query = query.filter(Image.user_id == current_user.id)
    return query.order_by(Image.upload_time.desc()).all()


@router.get("/{image_id}", response_model=ImageRead)
def get_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    image = db.query(Image).get(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if not current_user.is_admin and image.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return image 