from sqlalchemy.orm import Session
from app.models.payment_details import PaymentDetails
from sqlalchemy import func, text
from fastapi import HTTPException
from datetime import datetime

def emi_month_to_month_year(emi_month: str):
    try:
        dt = datetime.strptime(emi_month, '%b-%y')
        return dt.month, dt.year
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid emi_month format. Use e.g. Jul-25')

def get_summary_status(db: Session, emi_month: str) -> dict:
    month, year = emi_month_to_month_year(emi_month)
    results = (
        db.query(PaymentDetails.repayment_status_id, func.count(PaymentDetails.id))
        .filter(PaymentDetails.demand_month == month)
        .filter(PaymentDetails.demand_year == year)
        .group_by(PaymentDetails.repayment_status_id)
        .all()
    )
    status_lookup = {}
    for row in db.execute(text("SELECT id, repayment_status FROM repayment_status")).fetchall():
        status_lookup[row[0]] = row[1]
    status_map = {
        'Paid': 'paid',
        'Partially Paid': 'partially_paid',
        'Future': 'unpaid',
        'Overdue': 'unpaid',
        'Foreclose': 'foreclose',
    }
    summary = {
        'total': 0,
        'paid': 0,
        'unpaid': 0,
        'partially_paid': 0,
        'cash_collected': 0,
        'customer_deposited': 0,
        'paid_pending_approval': 0,
        'foreclose': 0
    }
    for status_id, count in results:
        status_str = status_lookup.get(status_id)
        if status_str not in status_map:
            print(f"Unknown status in DB: {status_str}")
        key = status_map.get(status_str, None)
        if key and key in summary:
            summary[key] += count
        summary['total'] += count
    return summary 