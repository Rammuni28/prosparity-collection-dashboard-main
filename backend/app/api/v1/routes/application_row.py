from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.application_row import AppplicationFilterResponse
from app.crud.application_row import get_filtered_applications

router = APIRouter()

@router.get("/", response_model=AppplicationFilterResponse)
def filter_applications(
    loan_id: str = Query("", description="Filter by specific loan ID"),  # 🎯 ADDED! Filter by loan_id
    emi_month: str = Query("", description="EMI month in format 'Jul-25'"),
    search: str = Query("", description="Search in applicant name or application ID"),
    branch: str = Query("", description="Filter by branch name"),
    dealer: str = Query("", description="Filter by dealer name"),
    lender: str = Query("", description="Filter by lender name"),
    status: str = Query("", description="Filter by repayment status"),
    rm_name: str = Query("", description="Filter by RM name"),
    tl_name: str = Query("", description="Filter by Team Lead name"),
    ptp_date_filter: str = Query("", description="Filter by PTP date: 'overdue', 'today', 'tomorrow', 'future', 'no_ptp'"),
    repayment_id: str = Query("", description="Filter by repayment ID (payment details ID)"),  # 🎯 ADDED! Filter by repayment_id
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get filtered applications with essential filtering options.
    
    Supports filtering by:
    - EMI month
    - Search in applicant name/ID
    - Branch, Dealer, Lender
    - Status, RM, Team Lead
    - PTP date categories
    """
    return get_filtered_applications(
        db=db,
        loan_id=loan_id,  # 🎯 ADDED! Pass loan_id parameter
        emi_month=emi_month,
        search=search,
        branch=branch,
        dealer=dealer,
        lender=lender,
        status=status,
        rm_name=rm_name,
        tl_name=tl_name,
        ptp_date_filter=ptp_date_filter,
        repayment_id=repayment_id,  # 🎯 ADDED! Pass repayment_id parameter
        offset=offset,
        limit=limit
    )