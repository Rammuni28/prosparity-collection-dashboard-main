from sqlalchemy import Column, Integer, Text, Enum, TIMESTAMP, ForeignKey, JSON, func
from app.db.base import Base
import enum

class AuditActionEnum(str, enum.Enum):
    insert = "INSERT"
    update = "UPDATE"
    delete = "DELETE"

class AuditPaymentDetails(Base):
    __tablename__ = "audit_payment_details"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Text)
    changed_by_user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(Enum(AuditActionEnum))
    old_data = Column(JSON)
    new_data = Column(JSON)
    changed_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 