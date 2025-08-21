from pydantic import BaseModel
from typing import Optional, Union
from datetime import date
from enum import Enum

class DemandCallingStatusEnum(str, Enum):
    deposited_in_bank = "deposited in bank"
    cash_collected = "cash collected"
    ptp_taken = "PTP taken"
    no_response = "no response"

class ContactCallingStatusEnum(str, Enum):
    answered = "answered"
    not_answered = "not answered"
    not_called = "not called"

class RepaymentStatusEnum(str, Enum):
    future = "Future"
    partially_paid = "Partially Paid"
    paid = "Paid"
    overdue = "Overdue"
    foreclose = "Foreclose"

class StatusManagementUpdate(BaseModel):
    # Status Management Card
    demand_calling_status: Optional[int] = None  # Will be ID from demand_calling table
    repayment_status: Optional[int] = None      # Will be ID from repayment_status table
    ptp_date: Optional[date] = None            # Date format
    amount_collected: Optional[float] = None   # Amount
    
    # Contact Card
    contact_calling_status: Optional[int] = None  # Will be ID from contact_calling table

class StatusManagementResponse(BaseModel):
    application_id: str
    demand_date: str
    demand_calling_status: Optional[int] = None  # ID from demand_calling table
    repayment_status: Optional[str] = None      # Name from repayment_status table
    ptp_date: Optional[str] = None
    amount_collected: Optional[float] = None
    contact_calling_status: Optional[int] = None  # ID from contact_calling table
    message: str
    updated_at: str
