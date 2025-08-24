from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.month_dropdown import MonthDropdownResponse
from app.crud.month_dropdown import get_month_dropdown_options

router = APIRouter()

@router.get("/{loan_id}/months", response_model=MonthDropdownResponse)
def get_month_dropdown_route(
    loan_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all available months for a loan application.
    
    Returns:
    - loan_id: The loan application ID
    - total_months: Total number of months available
    - current_month: Current month in "Aug-25" format
    - months: List of all months with repayment_id and demand_date
    - message: Success message
    """
    try:
        result = get_month_dropdown_options(
            db=db,
            loan_id=loan_id
        )
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get month options: {str(e)}")
