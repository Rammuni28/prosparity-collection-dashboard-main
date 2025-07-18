from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.lenders import Lender
from app.schemas.lenders import LenderOut

router = APIRouter()

@router.get("/", response_model=list[LenderOut])
def get_lenders(db: Session = Depends(get_db)):
    return db.query(Lender).all() 