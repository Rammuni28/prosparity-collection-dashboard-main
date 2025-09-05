#!/usr/bin/env python3
"""
Script to create initial admin user for the Prosparity Collection Dashboard
Run this script once to set up the first admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate
from app.core.config import settings

def create_initial_admin():
    """Create initial admin user if it doesn't exist"""
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin_email = "admin@prosparity.com"
        existing_admin = get_user_by_email(db, admin_email)
        
        if existing_admin:
            print(f"✅ Admin user already exists: {existing_admin.email}")
            return
        
        # Create admin user
        admin_user = UserCreate(
            name="System Administrator",
            email=admin_email,
            password="Admin@123",  # Change this password after first login!
            role="admin"
        )
        
        created_admin = create_user(db, admin_user)
        print(f"✅ Admin user created successfully!")
        print(f"   Email: {created_admin.email}")
        print(f"   Password: Admin@123")
        print(f"   Role: {created_admin.role}")
        print(f"   ⚠️  IMPORTANT: Change password after first login!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Creating initial admin user...")
    create_initial_admin()
    print("✨ Done!")
