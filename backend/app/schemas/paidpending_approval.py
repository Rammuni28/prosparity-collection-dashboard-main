from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class ApprovalActionEnum(str, Enum):
    accept = "accept"
    reject = "reject"

class PaidPendingApprovalRequest(BaseModel):
    loan_id: str
    demand_date: date
    action: ApprovalActionEnum  # accept or reject
    user_id: int  # Who is approving/rejecting
    comments: Optional[str] = None  # Optional comments for rejection

class PaidPendingApprovalResponse(BaseModel):
    loan_id: str
    demand_date: str
    action: str
    previous_status: str
    new_status: str
    message: str
    updated_at: str
    comments: Optional[str] = None
