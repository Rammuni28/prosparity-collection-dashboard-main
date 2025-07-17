from sqlalchemy import Column, Integer, Enum
from app.db.base import Base
import enum

class OwnershipTypeEnum(str, enum.Enum):
    owned = "Owned"
    rented = "Rented"
    company_provided = "Company Provided"
    parental = "Parental"
    other = "Other"

class OwnershipType(Base):
    __tablename__ = "ownership_type"
    id = Column(Integer, primary_key=True, index=True)
    ownership_type_name = Column(Enum(OwnershipTypeEnum), unique=True) 