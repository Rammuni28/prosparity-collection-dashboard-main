from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.repayment_status import RepaymentStatus
from app.schemas.repayment_status import RepaymentStatusOut

router = APIRouter()

@router.get("/", response_model=list[RepaymentStatusOut])
def get_repayment_statuses(db: Session = Depends(get_db)):
    return db.query(RepaymentStatus).all() 