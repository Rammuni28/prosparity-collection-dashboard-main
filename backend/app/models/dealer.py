from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from app.db.base import Base

class Dealer(Base):
    __tablename__ = "dealer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    location = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now()) 