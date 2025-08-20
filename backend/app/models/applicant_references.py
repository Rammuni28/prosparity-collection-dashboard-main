from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from app.db.base import Base

class ApplicantReferences(Base):
    __tablename__ = "reference"  # Fixed to match database table name
    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_application_id = Column(Integer, ForeignKey("loan_details.loan_application_id"))
    first_name = Column(String(55))
    middle_name = Column(String(55))
    last_name = Column(String(55))
    mobile = Column(String(15))
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    address_line3 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 