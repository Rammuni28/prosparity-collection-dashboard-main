from pydantic import BaseModel
from typing import Optional, List

class ApplicationItem(BaseModel):
    application_id: str
    applicant_name: str
    emi_amount: Optional[float]
    status: Optional[str]
    emi_month: Optional[str]
    branch: Optional[str]
    rm_name: Optional[str]
    tl_name: Optional[str]
    dealer: Optional[str]
    lender: Optional[str]
    ptp_date: Optional[str]
    calling_status: Optional[str] = None 
    comments: List[str] = [] 

class AppplicationFilterResponse(BaseModel):
    total: int
    results: List[ApplicationItem]
    