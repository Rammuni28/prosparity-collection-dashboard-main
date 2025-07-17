from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class LoanDetailsBase(BaseModel):
    loan_application_id: int
    applicant_id: str
    approved_amount: float
    disbursal_amount: float
    approved_rate: float
    disbursal_date: Optional[date] = None
    dollection_relationship_manager_id: Optional[int] = None
    source_relationship_manager_id: Optional[int] = None
    tenure: int

class LoanDetailsCreate(LoanDetailsBase):
    pass

class LoanDetailsOut(LoanDetailsBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 