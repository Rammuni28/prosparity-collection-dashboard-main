from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class AuditPaymentDetailsBase(BaseModel):
    application_id: str
    changed_by_user_id: int
    action: str
    old_data: Any
    new_data: Any
    changed_at: Optional[datetime] = None

class AuditPaymentDetailsCreate(AuditPaymentDetailsBase):
    pass

class AuditPaymentDetailsOut(AuditPaymentDetailsBase):
    id: int

    class Config:
        orm_mode = True 