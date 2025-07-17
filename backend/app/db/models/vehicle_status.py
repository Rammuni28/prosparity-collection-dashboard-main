from sqlalchemy import Column, Integer, Enum, TIMESTAMP, func
from app.db.base import Base
import enum

class VehicleStatusEnum(str, enum.Enum):
    repossessed = "Repossessed"
    need_to_repossess = "Need to repossess"
    third_party = "Third party"
    none = "none"

class VehicleStatus(Base):
    __tablename__ = "vehicle_status"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_status = Column(Enum(VehicleStatusEnum), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now()) 