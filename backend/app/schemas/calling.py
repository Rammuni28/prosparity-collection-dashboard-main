from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CallingBase(BaseModel):
    repayment_id: str
    caller_user_id: int
    status_id: int
    call_date: Optional[datetime] = None

class CallingCreate(CallingBase):
    pass

class CallingOut(CallingBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 