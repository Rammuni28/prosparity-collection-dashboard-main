from pydantic import BaseModel
from typing import List, Optional

class PaidPendingApplication(BaseModel):
    loan_id: str
    applicant_name: str
    emi_amount: Optional[float]
    repayment_id: str  # 🎯 CHANGED! From demand_date to repayment_id
    ptp_date: Optional[str]
    amount_collected: Optional[float]
    branch: str
    rm_name: str
    tl_name: str
    dealer: str
    lender: str
    comments: List[str] = []

class PaidPendingApplicationsResponse(BaseModel):
    total: int
    results: List[PaidPendingApplication]
