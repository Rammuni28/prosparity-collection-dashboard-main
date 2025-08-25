from sqlalchemy.orm import Session, aliased
from app.models.branch import Branch
from app.models.dealer import Dealer
from app.models.lenders import Lender
from app.models.repayment_status import RepaymentStatus
from app.models.vehicle_status import VehicleStatus
from app.models.payment_details import PaymentDetails
from app.models.user import User
from datetime import date, timedelta



def filter_options(db: Session):
    today = date.today()
    tomorrow = today + timedelta(days=1)


    emi_months = sorted(list(set([
    row[0].strftime("%Y-%m") 
    for row in db.query(PaymentDetails.demand_date.distinct()).all() 
    if row[0]
])))
    raw_dates = [
    row[0] for row in db.query(PaymentDetails.payment_date)
    .filter(PaymentDetails.payment_date != None)
    .all()
]
    ptp_categories = {
        "Overdue PTP": 0,
        "Today's PTP": 0,
        "Tomorrow's PTP": 0,
        "Future PTP": 0,
        "No PTP": 0
    }

    for ptp_date in raw_dates:
        if hasattr(ptp_date, 'date'):
            ptp_date = ptp_date.date()
        if ptp_date < today:
            ptp_categories["Overdue PTP"] += 1
        elif ptp_date == today:
            ptp_categories["Today's PTP"] += 1
        elif ptp_date == tomorrow:
            ptp_categories["Tomorrow's PTP"] += 1
        elif ptp_date > tomorrow:
            ptp_categories["Future PTP"] += 1

    no_ptp_count = db.query(PaymentDetails).filter(PaymentDetails.payment_date == None).count()
    ptp_categories["No PTP"] = no_ptp_count

    



    branches =  [b.name for b in db.query(Branch).all()]
    dealers = [d.name for d in db.query(Dealer).all()]
    lenders = [l.name for l in db.query(Lender).all()]
    statuses = [r.repayment_status for r in db.query(RepaymentStatus).all()]
    vehicle_statuses = [v.vehicle_status for v in db.query(VehicleStatus).all()]
    team_leads = [u.name for u in db.query(User).filter(User.role == "TL")]
    rms = [u.name for u in db.query(User).filter(User.role == "RM")]
    demand_num = [str(row[0]) for row in db.query(PaymentDetails.demand_num.distinct()).filter(PaymentDetails.demand_num != None).all()]  # 🎯 ADDED! Unique demand numbers

    return {
        "emi_months": emi_months,
        "branches": branches,
        "dealers": dealers,
        "lenders": lenders,
        "statuses": statuses,
        "ptpDateOptions": list(ptp_categories.keys()), 
        "vehicle_statuses": vehicle_statuses,
        "team_leads": team_leads,
        "rms": rms,
        "demand_num": demand_num,  # 🎯 ADDED! Demand numbers for filtering
    }
    


