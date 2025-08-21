from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Calling(Base):
    __tablename__ = "calling"
    id = Column(Integer, primary_key=True, index=True)
    repayment_id = Column(Text)
    caller_user_id = Column(Integer, ForeignKey("users.id"))
    Calling_id = Column(Integer, nullable=False)
    status_id = Column(Integer, ForeignKey("repayment_status.id"))
    call_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    caller = relationship("User", back_populates="calls")
    status = relationship("RepaymentStatus", back_populates="calls") 