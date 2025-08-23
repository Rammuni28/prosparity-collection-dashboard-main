from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class RepaymentStatusEnum(str, enum.Enum):
    Future = "Future"
    Partially_Paid = "Partially Paid"
    Paid = "Paid"
    Overdue = "Overdue"
    Foreclose = "Foreclose"
    Paid_Pending_Approval = "Paid(Pending Approval)"
    paidpending = "paidpending"
    Paid_Rejected = "Paid Rejected"

class RepaymentStatus(Base):
    __tablename__ = "repayment_status"
    id = Column(Integer, primary_key=True, index=True)
    repayment_status = Column(
        Enum(RepaymentStatusEnum, values_callable=lambda x: [e.value for e in x]), unique=True
    )
    
    # Relationships
    payment_details = relationship("PaymentDetails", back_populates="repayment_status")
    # Note: No direct relationship to Calling table - they're linked via payment_details.id 