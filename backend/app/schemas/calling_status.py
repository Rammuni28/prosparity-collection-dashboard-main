from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CallingStatusBase(BaseModel):
    calling_status: str

class CallingStatusCreate(CallingStatusBase):
    pass

class CallingStatusOut(CallingStatusBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True 