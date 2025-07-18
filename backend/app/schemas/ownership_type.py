from pydantic import BaseModel
from enum import Enum

class OwnershipTypeEnum(str, Enum):
    Owned = "Owned"
    Rented = "Rented"
    Company_Provided = "Company Provided"
    Parental = "Parental"
    Other = "Other"

class OwnershipTypeOut(BaseModel):
    id: int
    ownership_type_name: OwnershipTypeEnum

    class Config:
        orm_mode = True 