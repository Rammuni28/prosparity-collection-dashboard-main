from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.filters_main import FiltersOptionsResponse
from app.crud.filter_main import filter_options

router = APIRouter()

@router.get("/options", response_model=FiltersOptionsResponse)
def get_filter_options(db: Session = Depends(get_db)):
    return filter_options(db)