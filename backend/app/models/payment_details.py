from sqlalchemy import Column, Integer, DECIMAL, DATE, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class PaymentDetails(Base):
    __tablename__ = "payment_details"
    id = Column(Integer, primary_key=True, index=True)
    loan_application_id = Column(Integer, ForeignKey("loan_details.loan_application_id"))
    demand_amount = Column(DECIMAL(12,2))
    principal_amount = Column(DECIMAL(12,2))
    interest = Column(DECIMAL(12,2))
    demand_date = Column(DATE)
    demand_month = Column(Integer)
    demand_year = Column(Integer)
    demand_num = Column(Integer)
    amount_collected = Column(DECIMAL(12,2))
    fees = Column(DECIMAL(12,2))
    fees_status = Column(String(55))
    payment_date = Column(DATE)
    ptp_date = Column(DATE)
    Repayment_status_id = Column(Integer, ForeignKey("repayment_status.id"))
    mode = Column(String(50))
    payment_information = Column(String(55))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 

    # Relationship
    loan_details = relationship("LoanDetails", back_populates="payment_details") 