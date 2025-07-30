# Backend (FastAPI)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows use .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and adjust the values as needed.

## Environment variables (.env)

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/costco_ocr
SECRET_KEY=supersecret
AWS_REGION=ap-northeast-2
S3_BUCKET=your_bucket_name
PRESIGNED_EXPIRE=3600
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/vision.json
```

## Run development server

```bash
uvicorn app.main:app --reload
```

## Sample API Usage

### Upload image

```
POST /images
Headers: Authorization: Bearer <JWT>
Form-Data:
  store_id: 1
  zone: A12
  file: <image/jpeg>
```

Response 201
```
{
  "id": 123,
  "store_id": 1,
  "zone": "A12",
  "user_id": 3,
  "upload_time": "2025-07-30T15:00:00Z",
  "image_url": "https://<bucket>.s3.ap-northeast-2.amazonaws.com/uploads/uuid.jpg"
}
```

### Price History list
```
GET /price-history
Headers: Authorization: Bearer <JWT>
```

Response
```
[
  {
    "id": 55,
    "image_id": 123,
    "user_id": 3,
    "store_id": 1,
    "date": "2025-07-30",
    "product_code": null,
    "product_name": "APPLE",
    "price": "1000.00",
    "event_info": "1+1",
    "badge7": true,
    "badge30": true
  }
]
```

### Presigned 업로드 흐름
1. 클라이언트가 `/images/presigned` (JSON `{filename}`) 호출 → presigned URL/fields + key 응답
2. 응답값으로 S3에 직접 `multipart/form-data` POST
3. 업로드 성공 후 `/images/complete` 에 `{store_id, zone, key, image_url}` JSON POST
4. 백엔드는 OCR → 가격이력 생성 후 Image 레코드와 응답(JSON) 반환 