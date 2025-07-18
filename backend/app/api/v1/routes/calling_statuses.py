from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.calling_status import CallingStatus
from app.schemas.calling_status import CallingStatusOut

router = APIRouter()

@router.get("/", response_model=list[CallingStatusOut])
def get_calling_statuses(db: Session = Depends(get_db)):
    return db.query(CallingStatus).all() 