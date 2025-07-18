from sqlalchemy import Column, Integer, String
from app.db.base import Base

class RepaymentStatus(Base):
    __tablename__ = "repayment_status"
    id = Column(Integer, primary_key=True, index=True)
    repayment_status = Column(String(50), unique=True) 