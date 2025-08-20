#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models.repayment_status import RepaymentStatus

def test_connection():
    """Test database connection and basic query"""
    try:
        db = SessionLocal()
        print("Database connection successful!")
        
        # Test querying repayment_status table
        statuses = db.query(RepaymentStatus).all()
        print(f"Found {len(statuses)} repayment statuses:")
        for status in statuses:
            print(f"  - {status.id}: {status.repayment_status}")
        
        db.close()
        print("Database connection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
