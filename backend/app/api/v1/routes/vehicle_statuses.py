from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.vehicle_status import VehicleStatus
from app.schemas.vehicle_status import VehicleStatusOut

router = APIRouter()

@router.get("/", response_model=list[VehicleStatusOut])
def get_vehicle_statuses(db: Session = Depends(get_db)):
    return db.query(VehicleStatus).all() 