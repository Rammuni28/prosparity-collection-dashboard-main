from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from app.db.base import Base

class Branch(Base):
    __tablename__ = "branch"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    address = Column(Text)
    region = Column(String(100))
    state = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now()) 