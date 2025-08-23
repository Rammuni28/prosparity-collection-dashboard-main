from pydantic import BaseModel
from typing import Optional, Union
from datetime import date
from enum import Enum
from app.schemas.contact_types import ContactTypeEnum

class RepaymentStatusEnum(str, Enum):
    Future = "Future"
    Partially_Paid = "Partially Paid"
    Paid = "Paid"
    Overdue = "Overdue"
    Foreclose = "Foreclose"
    Paid_Pending_Approval = "Paid(Pending Approval)"
    paidpending = "paidpending"
    Paid_Rejected = "Paid Rejected"

class StatusManagementUpdate(BaseModel):
    loan_id: str
    demand_date: Optional[date] = None
    demand_calling_status: Optional[int] = None  # ID from demand_calling table
    repayment_status: Optional[int] = None  # ID from repayment_status table
    ptp_date: Optional[date] = None
    amount_collected: Optional[float] = None
    contact_calling_status: Optional[int] = None  # ID from contact_calling table
    contact_type: Optional[ContactTypeEnum] = ContactTypeEnum.applicant  # Default to applicant

class StatusManagementResponse(BaseModel):
    loan_id: str
    demand_date: Optional[date] = None
    demand_calling_status: Optional[int] = None
    repayment_status: Optional[int] = None
    ptp_date: Optional[date] = None
    amount_collected: Optional[float] = None
    contact_calling_status: Optional[int] = None
    contact_type: Optional[int] = None
    message: str
    updated_at: str
