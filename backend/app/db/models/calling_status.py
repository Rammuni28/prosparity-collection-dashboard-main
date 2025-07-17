from sqlalchemy import Column, Integer, Enum, TIMESTAMP, func
from app.db.base import Base
import enum

class CallingStatusEnum(str, enum.Enum):
    customer_funded = "customer funded"
    future_funded = "future_funded"
    cash_collected = "cash collected"
    refuse_unable_to_fund = "refuse/unable to fund"
    no_response = "no response"

class CallingStatus(Base):
    __tablename__ = "calling_status"
    id = Column(Integer, primary_key=True, index=True)
    calling_status = Column(Enum(CallingStatusEnum), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now()) 