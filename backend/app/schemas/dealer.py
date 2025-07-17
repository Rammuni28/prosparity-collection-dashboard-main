from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DealerBase(BaseModel):
    name: str
    location: str

class DealerCreate(DealerBase):
    pass

class DealerOut(DealerBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True 