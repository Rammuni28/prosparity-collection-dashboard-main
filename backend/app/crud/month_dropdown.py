from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from typing import Dict, Any, List
from app.models.payment_details import PaymentDetails
from app.models.loan_details import LoanDetails
from datetime import date

def get_month_dropdown_options(
    db: Session,
    loan_id: str
) -> Dict[str, Any]:
    """Get all available months for a loan application"""
    
    try:
        loan_id_int = int(loan_id)
    except ValueError:
        raise ValueError("loan_id must be a valid integer")
    
    # Get all payment records for this loan, ordered by demand_date
    payment_records = db.query(PaymentDetails).filter(
        PaymentDetails.loan_application_id == loan_id_int
    ).order_by(PaymentDetails.demand_date).all()
    
    if not payment_records:
        raise ValueError(f"No payment records found for loan_id: {loan_id}")
    
    months = []
    current_date = date.today()
    
    for payment in payment_records:
        if payment.demand_date:
            # Format month as "Aug-25"
            month_formatted = payment.demand_date.strftime('%b-%y')
            
            # Check if this is current month (within 30 days)
            days_diff = abs((current_date - payment.demand_date).days)
            is_current = days_diff <= 30
            
            months.append({
                "month": month_formatted,
                "repayment_id": str(payment.id),
                "demand_date": payment.demand_date.strftime('%Y-%m-%d'),
                "is_current": is_current
            })
    
    # Find current month (most recent or closest to today)
    current_month = months[-1]["month"] if months else None
    
    return {
        "loan_id": loan_id,
        "total_months": len(months),
        "current_month": current_month,
        "months": months,
        "message": f"Found {len(months)} months for loan {loan_id}"
    }
