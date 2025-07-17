from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class PaymentDetailsBase(BaseModel):
    loan_application_id: int
    demand_amount: float
    principal_amount: float
    interest: float
    demand_date: Optional[date] = None
    demand_month: Optional[int] = None
    demand_year: Optional[int] = None
    demand_num: Optional[int] = None
    amount_collected: Optional[float] = None
    fees: Optional[float] = None
    fees_status: Optional[str] = None
    payment_date: Optional[date] = None
    Repayment_status_id: Optional[int] = None
    mode: Optional[str] = None
    payment_information: Optional[str] = None

class PaymentDetailsCreate(PaymentDetailsBase):
    pass

class PaymentDetailsOut(PaymentDetailsBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 