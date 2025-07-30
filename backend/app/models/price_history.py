from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class PriceHistory(Base):
    """Tracks price information extracted from images (OCR results)."""

    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    date = Column(Date, nullable=False)
    product_code = Column(String(60), nullable=True)
    product_name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    event_info = Column(Text, nullable=True)
    badge7 = Column(Boolean, default=False)
    badge30 = Column(Boolean, default=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    image = relationship("Image", back_populates="price_histories")
    user = relationship("User")
    store = relationship("Store")
    product = relationship("Product") 