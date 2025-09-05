from sqlalchemy import Column, Integer, Enum, TIMESTAMP, func
from app.db.base import Base
import enum

class ContactCallingStatusEnum(str, enum.Enum):
    answered = "answered"
    not_answered = "not answered"
    not_called = "not called"

class ContactCalling(Base):
    __tablename__ = "contact_calling"
    id = Column(Integer, primary_key=True, index=True)
    contact_calling_status = Column(
        Enum(ContactCallingStatusEnum, values_callable=lambda x: [e.value for e in x]), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now()) 