# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session, joinedload, aliased
# from sqlalchemy import or_, func, cast, String
# from datetime import datetime
# from app.models.loan_details import LoanDetails
# from app.models.applicant_details import ApplicantDetails
# from app.models.branch import Branch
# from app.models.dealer import Dealer
# from app.models.lenders import Lender
# from app.models.payment_details import PaymentDetails
# from app.models.repayment_status import RepaymentStatus
# from app.schemas.application_details import ApplicationDetailsOut, ApplicationDetailsCreate, ApplicationListResponse, ApplicationListItem
# from app.api.deps import get_db
# from app.models.user import User
# from app.models.calling import Calling
# from app.models.calling_status import CallingStatus
# from app.models.comments import Comments

# router = APIRouter()

# @router.get("/filtered", response_model=ApplicationListResponse)
# def get_filtered_applications(
#     emi_month: str,
#     search: str = "",
#     offset: int = 0,
#     limit: int = 20,
#     db: Session = Depends(get_db)
# ):
#     # Parse emi_month
#     try:
#         dt = datetime.strptime(emi_month, '%b-%y')
#         month, year = dt.month, dt.year
#     except Exception:
#         raise HTTPException(status_code=400, detail='Invalid emi_month format. Use e.g. Jul-25')

#     RM = aliased(User)
#     TL = aliased(User)

#     # Subquery for latest calling status per payment
#     latest_calling = (
#         db.query(
#             Calling.repayment_id,
#             func.max(Calling.call_date).label("max_call_date")
#         )
#         .group_by(Calling.repayment_id)
#         .subquery()
#     )

#     query = (
#         db.query(
#             cast(LoanDetails.loan_application_id, String).label("application_id"),
#             (ApplicantDetails.first_name + " " + (ApplicantDetails.last_name or "")).label("applicant_name"),
#             PaymentDetails.demand_amount.label("emi_amount"),
#             RepaymentStatus.repayment_status.label("status"),
#             PaymentDetails.demand_month,
#             PaymentDetails.demand_year,
#             Branch.name.label("branch"),
#             RM.name.label("rm_name"),
#             TL.name.label("tl_name"),
#             Dealer.name.label("dealer"),
#             Lender.name.label("lender"),
#             PaymentDetails.payment_date.label("ptp_date"),
#             CallingStatus.calling_status.label("calling_status"),
#             PaymentDetails.id.label("payment_id")
#         )
#         .join(LoanDetails, PaymentDetails.loan_application_id == LoanDetails.loan_application_id)
#         .join(ApplicantDetails, LoanDetails.applicant_id == ApplicantDetails.applicant_id)
#         .join(Branch, ApplicantDetails.branch_id == Branch.id)
#         .join(Dealer, ApplicantDetails.dealer_id == Dealer.id)
#         .join(RM, LoanDetails.dollection_relationship_manager_id == RM.id)
#         .join(TL, LoanDetails.source_relationship_manager_id == TL.id)
#         .join(RepaymentStatus, PaymentDetails.Repayment_status_id == RepaymentStatus.id)
#         .outerjoin(Lender, Dealer.id == Lender.id)  # This is a placeholder; adjust join logic as needed
#         .outerjoin(Calling, (Calling.repayment_id == PaymentDetails.id))
#         .outerjoin(latest_calling, (latest_calling.c.repayment_id == Calling.repayment_id) & (latest_calling.c.max_call_date == Calling.call_date))
#         .outerjoin(CallingStatus, Calling.status_id == CallingStatus.id)
#         .filter(PaymentDetails.demand_month == month)
#         .filter(PaymentDetails.demand_year == year)
#     )

#     if search:
#         query = query.filter(
#             or_(
#                 ApplicantDetails.first_name.ilike(f"%{search}%"),
#                 ApplicantDetails.last_name.ilike(f"%{search}%"),
#                 LoanDetails.loan_application_id.ilike(f"%{search}%")
#             )
#         )

#     total = query.count()
#     results = query.offset(offset).limit(limit).all()

#     # Fetch comments for all payment_ids in results
#     payment_ids = [r.payment_id for r in results]
#     comments_map = {pid: [] for pid in payment_ids}
#     if payment_ids:
#         comments = db.query(Comments).filter(Comments.repayment_id.in_(payment_ids)).all()
#         for c in comments:
#             comments_map[c.repayment_id].append(c.comment)

#     results_list = [
#         ApplicationListItem(
#             application_id=r.application_id,
#             applicant_name=r.applicant_name,
#             emi_amount=r.emi_amount,
#             status=r.status,
#             emi_month=f'{datetime(year=r.demand_year, month=r.demand_month, day=1):%b-%y}',
#             branch=r.branch,
#             rm_name=r.rm_name,
#             tl_name=r.tl_name,
#             dealer=r.dealer,
#             lender=r.lender,
#             ptp_date=str(r.ptp_date) if r.ptp_date else None,
#             calling_status=r.calling_status,
#             comments=comments_map.get(r.payment_id, [])
#         )
#         for r in results
#     ]

#     return ApplicationListResponse(
#         total=total,
#         results=results_list
#     ) 