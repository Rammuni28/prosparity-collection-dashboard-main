from sqlalchemy import Column, Integer, Enum
from app.db.base import Base
import enum

class RepaymentStatusEnum(str, enum.Enum):
    future = "Future"
    partially_paid = "Partially Paid"
    paid = "Paid"
    overdue = "overdue"
    foreclose = "foreclose"

class RepaymentStatus(Base):
    __tablename__ = "repayment_status"
    id = Column(Integer, primary_key=True, index=True)
    repayment_status = Column(Enum(RepaymentStatusEnum), unique=True) 