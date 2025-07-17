from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicantDetailsBase(BaseModel):
    applicant_id: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    mobile: int
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[int] = None
    ownership_type_id: Optional[int] = None
    branch_id: Optional[int] = None
    dealer_id: Optional[int] = None
    fi_location: Optional[str] = None

class ApplicantDetailsCreate(ApplicantDetailsBase):
    pass

class ApplicantDetailsOut(ApplicantDetailsBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 