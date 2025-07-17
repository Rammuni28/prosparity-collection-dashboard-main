from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LenderBase(BaseModel):
    name: str
    address: str
    nodel_officer_name: str
    Grievance_officer_name: str

class LenderCreate(LenderBase):
    pass

class LenderOut(LenderBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True 