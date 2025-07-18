from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class VehicleStatusEnum(str, Enum):
    Repossessed = "Repossessed"
    Need_to_repossess = "Need to repossess"
    Third_party = "Third party"
    None_ = "none"

class VehicleStatusOut(BaseModel):
    id: int
    vehicle_status: VehicleStatusEnum
    created_at: datetime

    class Config:
        orm_mode = True 