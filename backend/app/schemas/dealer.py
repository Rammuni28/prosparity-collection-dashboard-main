from pydantic import BaseModel
from datetime import datetime

class DealerOut(BaseModel):
    id: int
    name: str
    location: str
    created_at: datetime

    class Config:
        orm_mode = True 