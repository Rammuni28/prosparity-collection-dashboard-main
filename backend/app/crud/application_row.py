from sqlalchemy.orm import Session, aliased
from sqlalchemy import desc, func
from app.models.loan_details import LoanDetails
from app.models.applicant_details import ApplicantDetails
from app.models.payment_details import PaymentDetails
from app.models.branch import Branch
from app.models.dealer import Dealer
from app.models.lenders import Lender
from app.models.comments import Comments
from app.models.user import User
from app.models.repayment_status import RepaymentStatus


def get_filtered_applications(db: Session, emi_month: str = "", offset: int = 0, limit: int = 20):


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
            PaymentDetails.id.label("payment_id"),  
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
        .join(Lender, LoanDetails.lender_id == Lender.id)
        .join(RM, LoanDetails.collection_relationship_manager_id == RM.id)
        .join(TL, LoanDetails.team_lead_id == TL.id)
        .join(RepaymentStatus, PaymentDetails.Repayment_status_id == RepaymentStatus.id)
        .order_by(PaymentDetails.demand_date.desc())
    )

    if emi_month:
        query = query.filter(func.date_format(PaymentDetails.demand_date, '%b-%y') == emi_month)
        
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
