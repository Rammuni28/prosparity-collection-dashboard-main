from pydantic import BaseModel
from datetime import datetime

class LenderOut(BaseModel):
    id: int
    name: str
    address: str
    nodel_officer_name: str
    Grievance_officer_name: str
    created_at: datetime

    class Config:
        orm_mode = True 