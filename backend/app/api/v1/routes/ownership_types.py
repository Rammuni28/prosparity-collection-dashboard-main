from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.ownership_type import OwnershipType
from app.schemas.ownership_type import OwnershipTypeOut

router = APIRouter()

@router.get("/", response_model=list[OwnershipTypeOut])
def get_ownership_types(db: Session = Depends(get_db)):
    return db.query(OwnershipType).all() 