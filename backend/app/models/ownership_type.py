from sqlalchemy import Column, Integer, Enum
from app.db.base import Base
import enum

class OwnershipTypeEnum(str, enum.Enum):
    Owned = "Owned"
    Rented = "Rented"
    Company_Provided = "Company Provided"
    Parental = "Parental"
    Other = "Other"

class OwnershipType(Base):
    __tablename__ = "ownership_type"
    id = Column(Integer, primary_key=True, index=True)
    ownership_type_name = Column(
        Enum(OwnershipTypeEnum, values_callable=lambda x: [e.value for e in x]), unique=True
    ) 