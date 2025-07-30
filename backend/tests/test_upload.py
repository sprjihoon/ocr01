import io
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import storage as storage_srv, ocr as ocr_srv

client = TestClient(app)


@pytest.fixture
def token(db_session):
    # Create user and return token (simplified stub)
    from app.models.user import User
    from app.core.security import get_password_hash, create_access_token

    user = User(username="test", hashed_password=get_password_hash("password"))
    db_session.add(user)
    db_session.commit()
    return create_access_token({"sub": user.username, "is_admin": "false"})


@pytest.fixture(autouse=True)
def patch_services(monkeypatch):
    monkeypatch.setattr(storage_srv, "upload_image", lambda file: "https://example.com/test.jpg")
    monkeypatch.setattr(ocr_srv, "run_ocr", lambda _: [{"product_name": "APPLE", "price": 1000}])


def test_upload_image(token):
    headers = {"Authorization": f"Bearer {token}"}
    file_bytes = io.BytesIO(b"fake image data")
    response = client.post(
        "/images",
        headers=headers,
        files={"file": ("label.jpg", file_bytes, "image/jpeg")},
        data={"store_id": 1, "zone": "A01"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["image_url"].startswith("http") 