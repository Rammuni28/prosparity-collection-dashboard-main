from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentsBase(BaseModel):
    repayment_id: str
    user_id: int
    comment: str
    commented_at: Optional[datetime] = None

class CommentsCreate(CommentsBase):
    pass

class CommentsOut(CommentsBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 