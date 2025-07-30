from sqlalchemy import Column, Integer, String, Float

from ..database import Base


class Store(Base):
    """Represents a Costco store location."""

    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    zone = Column(String(120), nullable=True) 