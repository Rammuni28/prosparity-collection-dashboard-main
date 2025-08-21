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

class ApplicationFilters(BaseModel):
    """Schema for essential filter parameters"""
    emi_month: Optional[str] = None
    search: Optional[str] = None
    branch: Optional[str] = None
    dealer: Optional[str] = None
    lender: Optional[str] = None
    status: Optional[str] = None
    rm_name: Optional[str] = None
    tl_name: Optional[str] = None
    ptp_date_filter: Optional[str] = None
    offset: Optional[int] = 0
    limit: Optional[int] = 20

class AppplicationFilterResponse(BaseModel):
    total: int
    results: List[ApplicationItem]
    