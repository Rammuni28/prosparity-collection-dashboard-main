from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import Dict, Any
from app.models.payment_details import PaymentDetails
from app.models.loan_details import LoanDetails
from app.models.calling import Calling
from app.models.contact_calling import ContactCalling
from app.models.repayment_status import RepaymentStatus
from app.schemas.status_management import StatusManagementUpdate
from app.schemas.contact_types import ContactTypeEnum

def update_status_management(
    db: Session, 
    loan_id: str, 
    status_data: StatusManagementUpdate
) -> Dict[str, Any]:
    """Update status management for a loan application"""
    
    # Find the payment record for this loan
    payment_record = db.query(PaymentDetails).join(
        LoanDetails, PaymentDetails.loan_application_id == LoanDetails.loan_application_id
    ).filter(
        LoanDetails.loan_application_id == loan_id
    ).first()
    
    if not payment_record:
        raise ValueError(f"No payment record found for loan ID: {loan_id}")
    
    repayment_id = str(payment_record.id)
    updated_fields = []
    calling_records_created = []
    
    # Update payment_details fields
    if status_data.demand_date is not None:
        payment_record.demand_date = status_data.demand_date
        updated_fields.append("demand_date")
    
    if status_data.repayment_status is not None:
        payment_record.repayment_status_id = status_data.repayment_status
        updated_fields.append("repayment_status")
    
    if status_data.ptp_date is not None:
        payment_record.ptp_date = status_data.ptp_date
        updated_fields.append("ptp_date")
    
    if status_data.amount_collected is not None:
        payment_record.amount_collected = status_data.amount_collected
        updated_fields.append("amount_collected")
    
    # Handle demand calling status
    if status_data.demand_calling_status is not None:
        # Create calling record for demand calling
        calling_record = Calling(
            repayment_id=repayment_id,
            caller_user_id=1,  # Default caller, can be updated later
            Calling_id=2,  # 2 for demand calling
            status_id=status_data.demand_calling_status,
            contact_type=ContactTypeEnum.applicant.value,  # Extract integer value from enum
            call_date=func.now()
        )
        db.add(calling_record)
        calling_records_created.append("demand_calling")
    
    # Handle contact calling status
    if status_data.contact_calling_status is not None:
        # Create calling record for contact calling
        contact_type_value = (status_data.contact_type or ContactTypeEnum.applicant).value  # Extract integer value
        calling_record = Calling(
            repayment_id=repayment_id,
            caller_user_id=1,  # Default caller, can be updated later
            Calling_id=1,  # 1 for contact calling
            status_id=status_data.contact_calling_status,
            contact_type=contact_type_value,  # Use extracted integer value
            call_date=func.now()
        )
        db.add(calling_record)
        calling_records_created.append("contact_calling")
    
    # Commit all changes
    db.commit()
    
    # Get existing calling statuses for response
    existing_demand_calling = db.query(Calling).filter(
        and_(
            Calling.repayment_id == repayment_id,
            Calling.Calling_id == 2  # Demand calling
        )
    ).first()
    
    existing_contact_calling = db.query(Calling).filter(
        and_(
            Calling.repayment_id == repayment_id,
            Calling.Calling_id == 1,  # Contact calling
            Calling.contact_type == (status_data.contact_type or ContactTypeEnum.applicant).value  # Extract integer value
        )
    ).first()
    
    return {
        "loan_id": loan_id,
        "demand_date": status_data.demand_date,
        "demand_calling_status": status_data.demand_calling_status or (existing_demand_calling.status_id if existing_demand_calling else None),
        "repayment_status": status_data.repayment_status,
        "ptp_date": status_data.ptp_date,
        "amount_collected": status_data.amount_collected,
        "contact_calling_status": status_data.contact_calling_status or (existing_contact_calling.status_id if existing_contact_calling else None),
        "contact_type": (status_data.contact_type or ContactTypeEnum.applicant).value,  # Extract integer value for response
        "message": f"Updated: {', '.join(updated_fields)}. Calling records created: {', '.join(calling_records_created)}. Repayment ID: {repayment_id}",
        "updated_at": payment_record.updated_at.isoformat() if payment_record.updated_at else None
    }
