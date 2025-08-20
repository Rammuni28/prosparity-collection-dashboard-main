from sqlalchemy import create_engine
from app.core.config import DATABASE_URL
from app.db.base import Base
from app.models import (
    user, applicant_details, applicant_references, audit_applicant_details,
    audit_payment_details, branch, calling_status, calling, co_applicant,
    comments, dealer, guarantor, lenders, loan_details, ownership_type,
    payment_details, repayment_status, vehicle_status
)

def init_db():
    """Initialize the database by creating all tables"""
    engine = create_engine(DATABASE_URL)
    
    # Import all models to ensure they're registered with Base
    # This is necessary for create_all() to work properly
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
