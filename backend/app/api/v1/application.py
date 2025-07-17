from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.models.loan_details import LoanDetails
from app.db.models.applicant_details import ApplicantDetails
from app.db.models.branch import Branch
from app.db.models.dealer import Dealer
from app.db.models.lenders import Lender
from app.db.models.payment_details import PaymentDetails
from app.schemas.application_details import ApplicationDetailsOut, ApplicationDetailsCreate
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=list[ApplicationDetailsOut])
def list_applications(db: Session = Depends(get_db)):
    apps = (
        db.query(LoanDetails)
        .options(
            joinedload(LoanDetails.applicant),
            joinedload(LoanDetails.applicant).joinedload(ApplicantDetails.branch),
            joinedload(LoanDetails.applicant).joinedload(ApplicantDetails.dealer),
            joinedload(LoanDetails.payment_details),
        )
        .all()
    )
    results = []
    for app in apps:
        applicant = app.applicant
        branch = applicant.branch if applicant else None
        dealer = applicant.dealer if applicant else None
        payment = app.payment_details[0] if app.payment_details else None
        results.append(ApplicationDetailsOut(
            id=app.id,
            applicant_id=app.applicant_id,
            applicant_name=f"{applicant.first_name} {applicant.last_name or ''}" if applicant else "",
            branch_name=branch.name if branch else None,
            team_lead=None,
            rm_name=None,
            dealer_name=dealer.name if dealer else None,
            lender_name=None,
            lms_status=None,
            field_status=None,
            emi_amount=payment.demand_amount if payment else None,
            principle_due=payment.principal_amount if payment else None,
            interest_due=payment.interest if payment else None,
            demand_date=str(payment.demand_date) if payment and payment.demand_date else None,
            user_id=None,
            created_at=str(app.created_at) if app.created_at else None,
            updated_at=str(app.updated_at) if app.updated_at else None,
            applicant_mobile=applicant.mobile if applicant else None,
            applicant_address=applicant.address_line1 if applicant else None,
            house_ownership=None,
            co_applicant_name=None,
            co_applicant_mobile=None,
            co_applicant_address=None,
            guarantor_name=None,
            guarantor_mobile=None,
            guarantor_address=None,
            reference_name=None,
            reference_mobile=None,
            reference_address=None,
            fi_location=applicant.fi_location if applicant else None,
            repayment=None,
            last_month_bounce=None,
            collection_rm=None,
            ptp_date=None,
            paid_date=None,
            applicant_calling_status=None,
            co_applicant_calling_status=None,
            guarantor_calling_status=None,
            reference_calling_status=None,
            latest_calling_status=None,
            disbursement_date=str(app.disbursal_date) if app.disbursal_date else None,
            loan_amount=float(app.approved_amount) if app.approved_amount else None,
            vehicle_status=None,
            amount_collected=payment.amount_collected if payment else None
        ))
    return results

@router.get("/{application_id}", response_model=ApplicationDetailsOut)
def get_application_details(application_id: int, db: Session = Depends(get_db)):
    app = (
        db.query(LoanDetails)
        .options(
            joinedload(LoanDetails.applicant),
            joinedload(LoanDetails.applicant).joinedload(ApplicantDetails.branch),
            joinedload(LoanDetails.applicant).joinedload(ApplicantDetails.dealer),
            joinedload(LoanDetails.payment_details),
            # Add more joinedload as needed
        )
        .filter(LoanDetails.id == application_id)
        .first()
    )
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    applicant = app.applicant
    branch = applicant.branch if applicant else None
    dealer = applicant.dealer if applicant else None
    payment = app.payment_details[0] if app.payment_details else None

    return ApplicationDetailsOut(
        id=app.id,
        applicant_id=app.applicant_id,
        applicant_name=f"{applicant.first_name} {applicant.last_name or ''}" if applicant else "",
        branch_name=branch.name if branch else None,
        team_lead=None,  # Add logic if you have this field
        rm_name=None,    # Add logic if you have this field
        dealer_name=dealer.name if dealer else None,
        lender_name=None,  # Add logic if you have lender relationship
        lms_status=None,   # Add logic if you have this field
        field_status=None, # Add logic if you have this field
        emi_amount=payment.demand_amount if payment else None,
        principle_due=payment.principal_amount if payment else None,
        interest_due=payment.interest if payment else None,
        demand_date=str(payment.demand_date) if payment and payment.demand_date else None,
        user_id=None,
        created_at=str(app.created_at) if app.created_at else None,
        updated_at=str(app.updated_at) if app.updated_at else None,
        applicant_mobile=applicant.mobile if applicant else None,
        applicant_address=applicant.address_line1 if applicant else None,
        house_ownership=None,  # Add logic if you have this field
        co_applicant_name=None,  # Add logic if you have this field
        co_applicant_mobile=None,
        co_applicant_address=None,
        guarantor_name=None,
        guarantor_mobile=None,
        guarantor_address=None,
        reference_name=None,
        reference_mobile=None,
        reference_address=None,
        fi_location=applicant.fi_location if applicant else None,
        repayment=None,  # Add logic if you have this field
        last_month_bounce=None,
        collection_rm=None,
        ptp_date=None,
        paid_date=None,
        applicant_calling_status=None,
        co_applicant_calling_status=None,
        guarantor_calling_status=None,
        reference_calling_status=None,
        latest_calling_status=None,
        disbursement_date=str(app.disbursal_date) if app.disbursal_date else None,
        loan_amount=float(app.approved_amount) if app.approved_amount else None,
        vehicle_status=None,
        amount_collected=payment.amount_collected if payment else None
    )

@router.post("/", response_model=ApplicationDetailsOut)
def create_application_details(application: ApplicationDetailsCreate, db: Session = Depends(get_db)):
    # 1. Create ApplicantDetails
    applicant = ApplicantDetails(
        applicant_id=application.applicant_id,
        first_name=application.applicant_first_name,
        middle_name=application.applicant_middle_name,
        last_name=application.applicant_last_name,
        mobile=application.applicant_mobile,
        address_line1=application.applicant_address_line1,
        address_line2=application.applicant_address_line2,
        address_line3=application.applicant_address_line3,
        city=application.applicant_city,
        state=application.applicant_state,
        pincode=application.applicant_pincode,
        ownership_type_id=application.ownership_type_id,
        branch_id=application.branch_id,
        dealer_id=application.dealer_id,
        fi_location=application.fi_location
    )
    db.add(applicant)
    db.commit()
    db.refresh(applicant)

    # 2. Create LoanDetails
    loan = LoanDetails(
        applicant_id=applicant.applicant_id,
        approved_amount=application.approved_amount,
        disbursal_amount=application.disbursal_amount,
        approved_rate=application.approved_rate,
        disbursal_date=application.disbursal_date,
        dollection_relationship_manager_id=application.dollection_relationship_manager_id,
        source_relationship_manager_id=application.source_relationship_manager_id,
        tenure=application.tenure
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)

    # 3. Create PaymentDetails
    payment = PaymentDetails(
        loan_application_id=loan.loan_application_id if hasattr(loan, 'loan_application_id') else loan.id,
        demand_amount=application.demand_amount,
        principal_amount=application.principal_amount,
        interest=application.interest,
        demand_date=application.demand_date,
        demand_month=application.demand_month,
        demand_year=application.demand_year,
        demand_num=application.demand_num,
        amount_collected=application.amount_collected,
        fees=application.fees,
        fees_status=application.fees_status,
        payment_date=application.payment_date,
        Repayment_status_id=application.Repayment_status_id,
        mode=application.mode,
        payment_information=application.payment_information
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    # 4. Return the created application details (reuse GET logic)
    return get_application_details(loan.id, db) 