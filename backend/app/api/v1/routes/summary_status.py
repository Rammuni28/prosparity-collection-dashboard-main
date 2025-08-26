from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.crud.summary_status import get_summary_status, get_summary_status_with_filters
from app.schemas.summary_status import SummaryStatusResponse

router = APIRouter()

@router.get('/summary', response_model=SummaryStatusResponse)
def summary_status_route(
    emi_month: str = Query(..., description="EMI month in format 'Jul-25'"),
    branch: str = Query(None, description="Filter by branch name"),
    dealer: str = Query(None, description="Filter by dealer name"),
    lender: str = Query(None, description="Filter by lender name"),
    status: str = Query(None, description="Filter by repayment status"),
    rm_name: str = Query(None, description="Filter by RM name"),
    tl_name: str = Query(None, description="Filter by TL name"),
    ptp_date_filter: str = Query(None, description="Filter by PTP date category"),
    repayment_id: str = Query(None, description="Filter by repayment ID"),
    demand_num: str = Query(None, description="Filter by demand number"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get summary status with optional filters applied
    """
    return get_summary_status_with_filters(
        db=db,
        emi_month=emi_month,
        branch=branch,
        dealer=dealer,
        lender=lender,
        status=status,
        rm_name=rm_name,
        tl_name=tl_name,
        ptp_date_filter=ptp_date_filter,
        repayment_id=repayment_id,
        demand_num=demand_num
    ) 