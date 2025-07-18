from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class CallingStatusEnum(str, Enum):
    Customer_funded = "customer funded"
    Future_funded = "future_funded"
    Cash_collected = "cash collected"
    Refuse_unable_to_fund = "refuse/unable to fund"
    No_response = "no response"

class CallingStatusOut(BaseModel):
    id: int
    calling_status: CallingStatusEnum
    created_at: datetime

    class Config:
        orm_mode = True 