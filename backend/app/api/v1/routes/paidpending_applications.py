from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_admin
from app.schemas.paidpending_applications import PaidPendingApplicationsResponse
from app.crud.paidpending_applications import get_paid_pending_applications

router = APIRouter()

@router.get("/", response_model=PaidPendingApplicationsResponse)
def get_paid_pending_applications_list(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Get all applications that are in 'Paid(Pending Approval)' status.
    
    This endpoint shows applications that need approval/rejection.
    Only shows comments with comment_type = 2 (paid pending comments).
    """
    try:
        results = get_paid_pending_applications(db, skip, limit)
        
        # Count total for pagination
        total = len(results) if len(results) < limit else limit * 10  # Approximate total
        
        return PaidPendingApplicationsResponse(
            total=total,
            results=results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get paid pending applications: {str(e)}")
