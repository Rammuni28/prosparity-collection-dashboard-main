from sqlalchemy import Column, Integer, String, DECIMAL, DATE, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class LoanDetails(Base):
    __tablename__ = "loan_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_application_id = Column(Integer, unique=True)
    applicant_id = Column(String(55), ForeignKey("applicant_details.applicant_id"))
    approved_amount = Column(DECIMAL(12,2))
    disbursal_amount = Column(DECIMAL(12,2))
    approved_rate = Column(DECIMAL(12,2))
    disbursal_date = Column(DATE)
    Collection_relationship_manager_id = Column(Integer)  # Fixed to match database
    source_relationship_manager_id = Column(Integer)
    lenders_id = Column(Integer, ForeignKey("lenders.id"))
    tenure = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 

    # Relationships - now properly defined with foreign keys
    applicant = relationship("ApplicantDetails", back_populates="loan_details")
    lender = relationship("Lender", back_populates="loan_details")
    payment_details = relationship("PaymentDetails", back_populates="loan_details")