from sqlalchemy import Column, Integer, Enum, TIMESTAMP, func
from app.db.base import Base
import enum

class DemandCallingStatusEnum(str, enum.Enum):
    deposited_in_bank = "deposited in bank"
    cash_collected = "cash collected"
    ptp_taken = "PTP taken"
    no_response = "no response"

class DemandCalling(Base):
    __tablename__ = "demand_calling"
    id = Column(Integer, primary_key=True, index=True)
    demand_calling_status = Column(
        Enum(DemandCallingStatusEnum, values_callable=lambda x: [e.value for e in x]), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
