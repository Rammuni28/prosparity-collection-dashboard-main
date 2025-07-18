from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.dealer import Dealer
from app.schemas.dealer import DealerOut

router = APIRouter()

@router.get("/", response_model=list[DealerOut])
def get_dealers(db: Session = Depends(get_db)):
    return db.query(Dealer).all() 