from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BranchBase(BaseModel):
    name: str
    address: str
    region: str
    state: str

class BranchCreate(BranchBase):
    pass

class BranchOut(BranchBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True 