from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    repayment_id: str
    user_id: int
    comment: str
    commented_at: Optional[datetime] = None

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    comment: Optional[str] = None
    commented_at: Optional[datetime] = None

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CommentListResponse(BaseModel):
    total: int
    results: List[CommentResponse]

class CommentWithUserInfo(CommentResponse):
    user_name: Optional[str] = None
    user_email: Optional[str] = None