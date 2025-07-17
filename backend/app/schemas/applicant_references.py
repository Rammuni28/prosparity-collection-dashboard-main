from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicantReferencesBase(BaseModel):
    loan_application_id: int
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    mobile: str
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[int] = None

class ApplicantReferencesCreate(ApplicantReferencesBase):
    pass

class ApplicantReferencesOut(ApplicantReferencesBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 