from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.status_management import StatusManagementUpdate, StatusManagementResponse
from app.crud.status_management import update_status_management
from app.models.payment_details import PaymentDetails
from app.models.repayment_status import RepaymentStatus
from app.models.demand_calling import DemandCalling
from app.models.contact_calling import ContactCalling
from app.models.calling import Calling
from sqlalchemy import and_
from typing import Optional
from datetime import date

router = APIRouter()

@router.put("/{application_id}", response_model=StatusManagementResponse)
def update_application_status(
    application_id: str,
    status_update: StatusManagementUpdate,
    demand_date: str = Query(..., description="Demand date in YYYY-MM-DD format"),
    user_id: int = Query(1, description="User ID who is updating (temporary)"),
    db: Session = Depends(get_db)
):
    """
    Update multiple status fields for an application in a single API call.
    
    Updates can include:
    - Demand Calling Status (creates calling record with calling_id=2)
    - Contact Calling Status (creates calling record with calling_id=1)
    - Repayment Status (payment_details.Repayment_status_id)
    - PTP Date (payment_details.ptp_date)
    - Amount Collected (payment_details.amount_collected)
    
    Only the fields provided will be updated.
    """
    try:
        # Parse demand date
        parsed_demand_date = date.fromisoformat(demand_date)
        
        # Update status management
        result = update_status_management(
            db=db,
            application_id=application_id,
            demand_date=parsed_demand_date,
            status_data=status_update,
            user_id=user_id
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update status: {str(e)}")

@router.get("/{application_id}")
def get_application_status(
    application_id: str,
    demand_date: str = Query(..., description="Demand date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """Get current status for an application"""
    try:
        parsed_demand_date = date.fromisoformat(demand_date)
        
        # Get payment details
        payment_details = db.query(PaymentDetails).filter(
            and_(
                PaymentDetails.loan_application_id == application_id,
                PaymentDetails.demand_date == parsed_demand_date
            )
        ).first()
        
        if not payment_details:
            raise HTTPException(status_code=404, detail="Payment details not found")
        
        # Get repayment status name
        repayment_status_name = None
        if payment_details.repayment_status_id:
            repayment_status_record = db.query(RepaymentStatus).filter(
                RepaymentStatus.id == payment_details.repayment_status_id
            ).first()
            if repayment_status_record:
                repayment_status_name = repayment_status_record.repayment_status
        
        # Get latest calling records for this application
        latest_demand_calling = db.query(Calling).filter(
            and_(
                Calling.repayment_id == str(payment_details.id),
                Calling.Calling_id == 2  # Demand calling
            )
        ).order_by(Calling.created_at.desc()).first()
        
        latest_contact_calling = db.query(Calling).filter(
            and_(
                Calling.repayment_id == str(payment_details.id),
                Calling.Calling_id == 1  # Contact calling
            )
        ).order_by(Calling.created_at.desc()).first()
        
        # Get status names from calling records
        demand_calling_status = None
        if latest_demand_calling:
            demand_calling_record = db.query(DemandCalling).filter(
                DemandCalling.id == latest_demand_calling.status_id
            ).first()
            if demand_calling_record:
                demand_calling_status = demand_calling_record.demand_calling_status
        
        contact_calling_status = None
        if latest_contact_calling:
            contact_calling_record = db.query(ContactCalling).filter(
                ContactCalling.id == latest_contact_calling.status_id
            ).first()
            if contact_calling_record:
                contact_calling_status = contact_calling_record.contact_calling_status
        
        return {
            "application_id": application_id,
            "demand_date": demand_date,
            "demand_calling_status": demand_calling_status,
            "repayment_status": repayment_status_name,
            "ptp_date": payment_details.ptp_date.isoformat() if payment_details.ptp_date else None,
            "amount_collected": float(payment_details.amount_collected) if payment_details.amount_collected else None,
            "contact_calling_status": contact_calling_status
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get status: {str(e)}")
