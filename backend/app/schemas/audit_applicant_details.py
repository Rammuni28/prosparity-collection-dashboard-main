from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class AuditApplicantDetailsBase(BaseModel):
    applicant_id: str
    changed_by_user_id: int
    action: str
    old_data: Any
    new_data: Any
    changed_at: Optional[datetime] = None

class AuditApplicantDetailsCreate(AuditApplicantDetailsBase):
    pass

class AuditApplicantDetailsOut(AuditApplicantDetailsBase):
    id: int

    class Config:
        orm_mode = True 