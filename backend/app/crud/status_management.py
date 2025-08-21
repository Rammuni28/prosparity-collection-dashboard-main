from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from app.models.payment_details import PaymentDetails
from app.models.demand_calling import DemandCalling
from app.models.contact_calling import ContactCalling
from app.models.repayment_status import RepaymentStatus
from app.models.calling import Calling
from app.schemas.status_management import StatusManagementUpdate
from datetime import date

def update_status_management(
    db: Session,
    application_id: str,
    demand_date: date,
    status_data: StatusManagementUpdate,
    user_id: int
) -> dict:
    """Update multiple status fields in a single API call"""
    
    updates_made = []
    calling_records_created = []
    
    # First, get the payment_details record for this application and demand_date
    payment_record = db.query(PaymentDetails).filter(
        and_(
            PaymentDetails.loan_application_id == application_id,
            PaymentDetails.demand_date == demand_date
        )
    ).first()
    
    if not payment_record:
        raise ValueError(f"No payment record found for application {application_id} and demand date {demand_date}")
    
    # Use payment_details.id as repayment_id for calling table
    repayment_id = str(payment_record.id)
    
    # 1. Update PTP Date and Amount Collected in payment_details table
    if status_data.ptp_date is not None:
        payment_record.ptp_date = status_data.ptp_date
        updates_made.append("ptp_date")
    
    if status_data.amount_collected is not None:
        payment_record.amount_collected = status_data.amount_collected
        updates_made.append("amount_collected")
    
    # 2. Update Repayment Status in payment_details table
    if status_data.repayment_status is not None:
        # Directly use the ID - no need to search
        payment_record.repayment_status_id = status_data.repayment_status
        updates_made.append("repayment_status")
    
    # 3. Handle Demand Calling Status - Create calling record
    if status_data.demand_calling_status is not None:
        # Directly use the ID - no need to search
        # Create calling record with calling_id = 2 (demand calling)
        # repayment_id = payment_details.id (exact payment record ID)
        new_calling = Calling(
            repayment_id=repayment_id,  # payment_details.id
            caller_user_id=user_id,
            Calling_id=2,  # Demand calling
            status_id=status_data.demand_calling_status  # Direct ID
        )
        db.add(new_calling)
        calling_records_created.append("demand_calling")
        updates_made.append("demand_calling_status")
    
    # 4. Handle Contact Calling Status - Create calling record
    if status_data.contact_calling_status is not None:
        # Directly use the ID - no need to search
        # Create calling record with calling_id = 1 (contact calling)
        # repayment_id = payment_details.id (exact payment record ID)
        new_calling = Calling(
            repayment_id=repayment_id,  # payment_details.id
            caller_user_id=user_id,
            Calling_id=1,  # Contact calling
            status_id=status_data.contact_calling_status  # Direct ID
        )
        db.add(new_calling)
        calling_records_created.append("contact_calling")
        updates_made.append("contact_calling_status")
    
    # Commit all changes
    db.commit()
    
    # Get updated values for response
    db.refresh(payment_record)
    
    # Get repayment status name
    repayment_status_name = None
    if payment_record.repayment_status_id:
        repayment_status_record = db.query(RepaymentStatus).filter(
            RepaymentStatus.id == payment_record.repayment_status_id
        ).first()
        if repayment_status_record:
            repayment_status_name = repayment_status_record.repayment_status
    
    # Get existing calling statuses for fields that weren't updated
    existing_demand_calling_status = None
    existing_contact_calling_status = None
    
    if status_data.demand_calling_status is None:
        # Get latest demand calling status from calling table
        latest_demand_calling = db.query(Calling).filter(
            and_(
                Calling.repayment_id == repayment_id,
                Calling.Calling_id == 2  # Demand calling
            )
        ).order_by(Calling.created_at.desc()).first()
        
        if latest_demand_calling:
            existing_demand_calling_status = latest_demand_calling.status_id
    
    if status_data.contact_calling_status is None:
        # Get latest contact calling status from calling table
        latest_contact_calling = db.query(Calling).filter(
            and_(
                Calling.repayment_id == repayment_id,
                Calling.Calling_id == 1  # Contact calling
            )
        ).order_by(Calling.created_at.desc()).first()
        
        if latest_contact_calling:
            existing_contact_calling_status = latest_contact_calling.status_id
    
    return {
        "application_id": str(application_id),
        "demand_date": demand_date.isoformat(),
        "demand_calling_status": status_data.demand_calling_status if status_data.demand_calling_status is not None else existing_demand_calling_status,
        "repayment_status": repayment_status_name,
        "ptp_date": payment_record.ptp_date.isoformat() if payment_record.ptp_date else None,
        "amount_collected": float(payment_record.amount_collected) if payment_record.amount_collected else None,
        "contact_calling_status": status_data.contact_calling_status if status_data.contact_calling_status is not None else existing_contact_calling_status,
        "message": f"Updated: {', '.join(updates_made)}. Calling records created: {', '.join(calling_records_created)}. Repayment ID: {repayment_id}",
        "updated_at": payment_record.updated_at.isoformat() if payment_record.updated_at else None
    }
