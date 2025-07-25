from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.application_row import AppplicationFilterResponse
from app.crud.application_row import get_filtered_applications

router = APIRouter()

@router.get("/", response_model=AppplicationFilterResponse)
def filter_applications(
    emi_month: str = Query("", description="EMI month in format 'Jul-25'"),
    offset: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return get_filtered_applications(db, emi_month, offset, limit)