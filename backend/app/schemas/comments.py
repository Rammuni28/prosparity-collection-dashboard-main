from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class CommentTypeEnum(int, Enum):
    application_details = 1      # Comments from application details section
    paid_pending = 2            # Comments from paid pending section

class CommentCreate(BaseModel):
    repayment_id: str  # This is payment_details.id
    comment: str
    user_id: int
    comment_type: CommentTypeEnum  # 1 or 2

class CommentResponse(BaseModel):
    id: int
    repayment_id: str
    user_id: int
    comment: str
    comment_type: int
    commented_at: datetime

class CommentListResponse(BaseModel):
    total: int
    results: List[CommentResponse]