from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    hash = Column(String, nullable=False)
    previous_hash = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())