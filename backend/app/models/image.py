from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from ..database import Base


class Image(Base):
    """Stores uploaded image metadata."""

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())
    image_url = Column(String(512), nullable=False)
    zone = Column(String(120), nullable=True)

    user = relationship("User")
    store = relationship("Store")
    price_histories = relationship(
        "PriceHistory", back_populates="image", cascade="all, delete-orphan"
    ) 