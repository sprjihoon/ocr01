from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, func

from ..database import Base


class Log(Base):
    """Application activity logs."""

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(120), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    meta = Column(JSON, nullable=True) 