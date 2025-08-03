from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime

class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    final_url = Column(String)
    status_code = Column(Integer)
    response_time = Column(Float)
    checked_at = Column(DateTime, default=datetime.utcnow)
    error = Column(String, nullable=True)
