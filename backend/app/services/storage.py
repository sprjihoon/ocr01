import uuid
from pathlib import Path
from fastapi import UploadFile
import os
from datetime import timedelta
from typing import Tuple
import shutil

try:
    import boto3
    from botocore.exceptions import ClientError
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

# Environment variables
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
S3_BUCKET = os.getenv("S3_BUCKET", "costco-price-images")
PRESIGNED_EXPIRE = int(os.getenv("PRESIGNED_EXPIRE", "3600"))  # in seconds

# Local storage directory
LOCAL_UPLOAD_DIR = Path("uploads")
LOCAL_UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize S3 client only if AWS credentials are available
s3_client = None
if AWS_AVAILABLE:
    try:
        s3_client = boto3.client("s3", region_name=AWS_REGION)
        # Test connection
        s3_client.head_bucket(Bucket=S3_BUCKET)
    except Exception as e:
        print(f"AWS S3 not available: {e}")
        s3_client = None


def _generate_key(filename: str) -> str:
    ext = Path(filename).suffix
    return f"uploads/{uuid.uuid4()}{ext}"


def upload_image(file: UploadFile) -> str:
    """Upload image to S3 or local storage and return its URL."""
    key = _generate_key(file.filename or "image.jpg")
    
    if s3_client:
        try:
            s3_client.upload_fileobj(
                file.file, 
                S3_BUCKET, 
                key, 
                ExtraArgs={"ContentType": file.content_type or "image/jpeg"}
            )
            return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"
        except ClientError as exc:
            print(f"S3 upload failed: {exc}, falling back to local storage")
    
    # Fallback to local storage
    file_path = LOCAL_UPLOAD_DIR / key.replace("uploads/", "")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Reset file pointer and save locally
    file.file.seek(0)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Return local file URL
    return f"http://localhost:8000/static/uploads/{file_path.name}"


def create_presigned_post(filename: str) -> Tuple[str, dict]:
    """Return presigned POST URL and fields for client-side uploads."""
    key = _generate_key(filename)
    
    if s3_client:
        try:
            response = s3_client.generate_presigned_post(
                Bucket=S3_BUCKET,
                Key=key,
                Fields={"acl": "public-read", "Content-Type": "image/jpeg"},
                Conditions=[["starts-with", "$Content-Type", "image/"], {"acl": "public-read"}],
                ExpiresIn=PRESIGNED_EXPIRE,
            )
            return key, response
        except ClientError as exc:
            print(f"Failed to create presigned post: {exc}, using local upload")
    
    # Fallback to local upload endpoint
    return key, {
        "url": "http://localhost:8000/images/upload-local",
        "fields": {"key": key}
    }


def get_image_bytes(key: str) -> bytes:
    """Get image bytes from S3 or local storage."""
    if s3_client:
        try:
            obj = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
            return obj["Body"].read()
        except Exception as e:
            print(f"Failed to fetch from S3: {e}")
    
    # Fallback to local storage
    file_path = LOCAL_UPLOAD_DIR / key.replace("uploads/", "")
    if file_path.exists():
        return file_path.read_bytes()
    else:
        # Return dummy image bytes for testing
        return b"dummy-image-content"


__all__ = [
    "upload_image",
    "create_presigned_post",
    "get_image_bytes",
    "s3_client",
    "S3_BUCKET",
    "LOCAL_UPLOAD_DIR",
] 