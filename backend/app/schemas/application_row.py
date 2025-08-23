from pydantic import BaseModel
from typing import Optional, List, Dict

class ApplicationItem(BaseModel):
    application_id: str
    loan_id: int  # Added loan_id field
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
    calling_statuses: Dict[str, str] = {  # All 4 contact types calling status
        "applicant": "Not Called",
        "co_applicant": "Not Called", 
        "guarantor": "Not Called",
        "reference": "Not Called"
    }
    payment_mode: Optional[str] = None  # Payment mode (UPI, Cash, etc.)
    comments: List[str] = []

class ApplicationFilters(BaseModel):
    emi_month: Optional[str] = ""
    search: Optional[str] = ""
    branch: Optional[str] = ""
    dealer: Optional[str] = ""
    lender: Optional[str] = ""
    status: Optional[str] = ""
    rm_name: Optional[str] = ""
    tl_name: Optional[str] = ""
    ptp_date_filter: Optional[str] = ""
    offset: Optional[int] = 0
    limit: Optional[int] = 20

class AppplicationFilterResponse(BaseModel):
    total: int
    results: List[ApplicationItem]
    