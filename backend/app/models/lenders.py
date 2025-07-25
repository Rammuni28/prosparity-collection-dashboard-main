from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from app.db.base import Base
from sqlalchemy.orm import relationship

class Lender(Base):
    __tablename__ = "lenders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    address = Column(Text)
    nodel_officer_name = Column(String(100))
    Grievance_officer_name = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())


    loan_details = relationship("LoanDetails", back_populates="lender") 