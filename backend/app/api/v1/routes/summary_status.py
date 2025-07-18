from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.summary_status import get_summary_status
from app.schemas.summary_status import SummaryStatusResponse

router = APIRouter()

@router.get('/summary', response_model=SummaryStatusResponse)
def summary_status_route(
    emi_month: str = Query(..., description="EMI month in format 'Jul-25'"),
    db: Session = Depends(get_db)
):
    return get_summary_status(db, emi_month) 