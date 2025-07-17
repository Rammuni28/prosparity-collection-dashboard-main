from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VehicleStatusBase(BaseModel):
    vehicle_status: str

class VehicleStatusCreate(VehicleStatusBase):
    pass

class VehicleStatusOut(VehicleStatusBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True 