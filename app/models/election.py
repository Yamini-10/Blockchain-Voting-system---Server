from sqlalchemy import Column, Integer, Boolean
from app.db.base import Base

class Election(Base):
    __tablename__ = "election_status"

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)