from pydantic import BaseModel
from typing import Optional

class RepaymentStatusBase(BaseModel):
    repayment_status: str

class RepaymentStatusCreate(RepaymentStatusBase):
    pass

class RepaymentStatusOut(RepaymentStatusBase):
    id: int

    class Config:
        orm_mode = True 