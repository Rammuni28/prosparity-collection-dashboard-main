from sqlalchemy.orm import Session, aliased
from sqlalchemy import desc, func, or_
from app.models.loan_details import LoanDetails
from app.models.applicant_details import ApplicantDetails
from app.models.payment_details import PaymentDetails
from app.models.branch import Branch
from app.models.dealer import Dealer
from app.models.lenders import Lender
from app.models.comments import Comments
from app.models.user import User
from app.models.repayment_status import RepaymentStatus
from datetime import date, timedelta

def get_filtered_applications(
    db: Session, 
    emi_month: str = "", 
    search: str = "",
    branch: str = "",
    dealer: str = "",
    lender: str = "",
    status: str = "",
    rm_name: str = "",
    tl_name: str = "",
    ptp_date_filter: str = "",
    offset: int = 0, 
    limit: int = 20
):
    RM = aliased(User)
    TL = aliased(User)

    latest_payment_subq = (
        db.query(
            PaymentDetails.loan_application_id,
            func.max(PaymentDetails.demand_date).label("max_demand_date")
        )
        .group_by(PaymentDetails.loan_application_id)
        .subquery()
    )

    query = (
        db.query(
            LoanDetails.loan_application_id.label("application_id"),
            ApplicantDetails.first_name,
            ApplicantDetails.last_name,
            PaymentDetails.demand_amount.label("emi_amount"),
            RepaymentStatus.repayment_status.label("status"),
            PaymentDetails.demand_date.label('emi_month'),
            Branch.name.label("branch"),
            RM.name.label("rm_name"),
            TL.name.label("tl_name"),
            Dealer.name.label("dealer"),
            Lender.name.label("lender"),
            PaymentDetails.ptp_date.label("ptp_date"),
            PaymentDetails.mode.label("calling_status"),
            PaymentDetails.id.label("payment_id")
        )
        .join(ApplicantDetails, LoanDetails.applicant_id == ApplicantDetails.applicant_id)
        .join(
            latest_payment_subq,
            LoanDetails.loan_application_id == latest_payment_subq.c.loan_application_id
        )
        .join(
            PaymentDetails,
            (PaymentDetails.loan_application_id == latest_payment_subq.c.loan_application_id) &
            (PaymentDetails.demand_date == latest_payment_subq.c.max_demand_date)
        )
        .join(Branch, ApplicantDetails.branch_id == Branch.id)
        .join(Dealer, ApplicantDetails.dealer_id == Dealer.id)
        .join(Lender, LoanDetails.lenders_id == Lender.id)
        .join(RM, LoanDetails.Collection_relationship_manager_id == RM.id)
        .join(TL, LoanDetails.source_relationship_manager_id == TL.id)
        .join(RepaymentStatus, PaymentDetails.repayment_status_id == RepaymentStatus.id)
    )

    # Apply essential filters only
    if emi_month:
        query = query.filter(func.date_format(PaymentDetails.demand_date, '%b-%y') == emi_month)
    
    if search:
        search_filter = or_(
            func.concat(ApplicantDetails.first_name, ' ', ApplicantDetails.last_name).ilike(f'%{search}%'),
            ApplicantDetails.first_name.ilike(f'%{search}%'),
            ApplicantDetails.last_name.ilike(f'%{search}%'),
            LoanDetails.loan_application_id.ilike(f'%{search}%')
        )
        query = query.filter(search_filter)
    
    if branch:
        query = query.filter(Branch.name == branch)
    
    if dealer:
        query = query.filter(Dealer.name == dealer)
    
    if lender:
        query = query.filter(Lender.name == lender)
    
    if status:
        query = query.filter(RepaymentStatus.repayment_status == status)
    
    if rm_name:
        query = query.filter(RM.name == rm_name)
    
    if tl_name:
        query = query.filter(TL.name == tl_name)
    
    # PTP date filtering
    if ptp_date_filter:
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        if ptp_date_filter == "overdue":
            query = query.filter(PaymentDetails.ptp_date < today)
        elif ptp_date_filter == "today":
            query = query.filter(func.date(PaymentDetails.ptp_date) == today)
        elif ptp_date_filter == "tomorrow":
            query = query.filter(func.date(PaymentDetails.ptp_date) == tomorrow)
        elif ptp_date_filter == "future":
            query = query.filter(PaymentDetails.ptp_date > tomorrow)
        elif ptp_date_filter == "no_ptp":
            query = query.filter(PaymentDetails.ptp_date.is_(None))
    
    total = query.count()
    results = []

    for row in query.offset(offset).limit(limit).all():
        # Get comments for this payment
        comments = db.query(Comments).filter(Comments.repayment_id == row.payment_id).order_by(Comments.commented_at.desc()).all()
        comment_list = [c.comment for c in comments]

        results.append({
            "application_id": str(row.application_id),
            "applicant_name": f"{row.first_name or ''} {row.last_name or ''}".strip(),
            "emi_amount": float(row.emi_amount) if row.emi_amount else None,
            "status": row.status,
            "emi_month": row.emi_month.strftime('%b-%y') if row.emi_month else None,
            "branch": row.branch,
            "rm_name": row.rm_name,
            "tl_name": row.tl_name,
            "dealer": row.dealer,
            "lender": row.lender,
            "ptp_date": row.ptp_date.strftime('%y-%m-%d') if row.ptp_date else None,
            "calling_status": row.calling_status,
            "comments": comment_list
        })

    return {
        "total": total,
        "results": results
    }
