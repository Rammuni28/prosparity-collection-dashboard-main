from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.repayment_status import RepaymentStatus

def populate_repayment_status():
    """Populate the repayment_status table with initial data"""
    db = SessionLocal()
    
    try:
        # Check if table already has data
        existing_count = db.query(RepaymentStatus).count()
        if existing_count > 0:
            print(f"Repayment status table already has {existing_count} records")
            return
        
        # Define repayment statuses that match the existing database enum
        statuses = [
            "Future",
            "Partially Paid",
            "Paid",
            "Overdue",
            "Foreclose"
        ]
        
        # Create and add statuses
        for status in statuses:
            repayment_status = RepaymentStatus(repayment_status=status)
            db.add(repayment_status)
        
        # Commit the changes
        db.commit()
        print(f"Successfully added {len(statuses)} repayment statuses")
        
    except Exception as e:
        print(f"Error populating repayment status: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_repayment_status()
