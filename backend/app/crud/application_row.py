from sqlalchemy.orm import Session, aliased
from sqlalchemy import desc, func, or_, and_
from app.models.loan_details import LoanDetails
from app.models.applicant_details import ApplicantDetails
from app.models.payment_details import PaymentDetails
from app.models.branch import Branch
from app.models.dealer import Dealer
from app.models.lenders import Lender
from app.models.comments import Comments
from app.models.user import User
from app.models.repayment_status import RepaymentStatus
from app.models.calling import Calling
from app.models.contact_calling import ContactCalling
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
            ApplicantDetails.applicant_id.label("application_id"),
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
            PaymentDetails.mode.label("payment_mode"),
            PaymentDetails.id.label("payment_id")
        )
        .select_from(LoanDetails)
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
            ApplicantDetails.applicant_id.ilike(f'%{search}%')
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
        # Get comments for this payment (only application details comments, comment_type = 1)
        comments = db.query(Comments).filter(
            and_(
                Comments.repayment_id == row.payment_id,
                Comments.comment_type == 1  # Only application details comments, not paid pending
            )
        ).order_by(Comments.commented_at.desc()).all()
        comment_list = [c.comment for c in comments]

        # Get calling status for ALL 4 contact types (1=applicant, 2=co-applicant, 3=guarantor, 4=reference)
        calling_statuses = {
            "applicant": "Not Called",      # contact_type = 1
            "co_applicant": "Not Called",   # contact_type = 2
            "guarantor": "Not Called",      # contact_type = 3
            "reference": "Not Called"       # contact_type = 4
        }
        
        # Get latest calling records for each contact type for this payment (repayment_id)
        for contact_type in range(1, 5):  # 1 to 4
            latest_calling = db.query(Calling).filter(
                and_(
                    Calling.repayment_id == str(row.payment_id),
                    Calling.Calling_id == 1,  # Only contact calling, not demand calling
                    Calling.contact_type == contact_type
                )
            ).order_by(Calling.created_at.desc()).first()
            
            if latest_calling:
                # Get contact calling status
                contact_status = db.query(ContactCalling).filter(
                    ContactCalling.id == latest_calling.status_id
                ).first()
                if contact_status:
                    # Map contact_type number to string key
                    if contact_type == 1:
                        calling_statuses["applicant"] = contact_status.contact_calling_status
                    elif contact_type == 2:
                        calling_statuses["co_applicant"] = contact_status.contact_calling_status
                    elif contact_type == 3:
                        calling_statuses["guarantor"] = contact_status.contact_calling_status
                    elif contact_type == 4:
                        calling_statuses["reference"] = contact_status.contact_calling_status

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
            "calling_statuses": calling_statuses,  # All 4 contact types calling status
            "payment_mode": row.payment_mode,      # Payment mode separate
            "comments": comment_list
        })

    return {
        "total": total,
        "results": results
    }
