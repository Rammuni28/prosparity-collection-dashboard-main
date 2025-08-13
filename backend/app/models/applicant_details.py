from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class ApplicantDetails(Base):
    __tablename__ = "applicant_details"
    applicant_id = Column(String(100), primary_key=True, index=True)
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
    mobile = Column(String(15))
    address_line1 = Column(Text)
    address_line2 = Column(Text)
    address_line3 = Column(Text)
    city = Column(Text)
    state = Column(Text)
    pincode = Column(Integer)
    ownership_type_id = Column(Integer)
    branch_id = Column(Integer)
    dealer_id = Column(Integer)
    fi_location = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    loan_details = relationship("LoanDetails", 
                             back_populates="applicant",
                             primaryjoin="ApplicantDetails.applicant_id == LoanDetails.applicant_id")
    branch = relationship("Branch")
    dealer = relationship("Dealer")
    ownership_type = relationship("OwnershipType") 