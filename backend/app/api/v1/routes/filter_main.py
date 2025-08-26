from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.filters_main import FiltersOptionsResponse
from app.crud.filter_main import filter_options

router = APIRouter()

@router.get("/options", response_model=FiltersOptionsResponse)
def get_filter_options(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return filter_options(db)