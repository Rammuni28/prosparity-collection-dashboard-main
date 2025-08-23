#!/usr/bin/env python3
"""
Debug script to check what's in the contact tables
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

# Use the database URL from config
DATABASE_URL = "mysql+pymysql://root:rammuni@localhost:3306/prosparity_collection_database"
engine = create_engine(DATABASE_URL)

def debug_contacts():
    """Debug what's in the contact tables"""
    with engine.connect() as conn:
        print("🔍 DEBUGGING CONTACTS DATABASE...")
        print("=" * 50)
        
        # Check loan_details table
        print("\n📋 1. LOAN_DETAILS TABLE:")
        result = conn.execute(text("SELECT * FROM loan_details LIMIT 5"))
        for row in result:
            print(f"   loan_application_id: {row[0]}, applicant_id: {row[1]}")
        
        # Check applicant_details table
        print("\n👤 2. APPLICANT_DETAILS TABLE:")
        result = conn.execute(text("SELECT * FROM applicant_details LIMIT 5"))
        for row in result:
            print(f"   applicant_id: {row[0]}, first_name: {row[1]}, last_name: {row[2]}")
        
        # Check co_applicant table
        print("\n👥 3. CO_APPLICANT TABLE:")
        result = conn.execute(text("SELECT * FROM co_applicant LIMIT 5"))
        for row in result:
            print(f"   id: {row[0]}, loan_application_id: {row[1]}, first_name: {row[2]}, last_name: {row[3]}")
        
        # Check guarantor table
        print("\n🤝 4. GUARANTOR TABLE:")
        result = conn.execute(text("SELECT * FROM guarantor LIMIT 5"))
        for row in result:
            print(f"   id: {row[0]}, loan_application_id: {row[1]}, first_name: {row[2]}, last_name: {row[3]}")
        
        # Check applicant_references table
        print("\n📞 5. APPLICANT_REFERENCES TABLE:")
        result = conn.execute(text("SELECT * FROM applicant_references LIMIT 5"))
        for row in result:
            print(f"   id: {row[0]}, loan_application_id: {row[1]}, first_name: {row[2]}, last_name: {row[3]}")
        
        # Check specific loan_id = 1
        print("\n🎯 6. SPECIFIC LOAN_ID = 1:")
        result = conn.execute(text("SELECT * FROM loan_details WHERE loan_application_id = 1"))
        loan_row = result.fetchone()
        if loan_row:
            print(f"   Found loan: {loan_row}")
            
            # Check if there are any contacts for this loan
            print("\n   🔍 Checking contacts for loan_id = 1:")
            
            # Check co-applicants
            result = conn.execute(text("SELECT * FROM co_applicant WHERE loan_application_id = 1"))
            co_apps = result.fetchall()
            print(f"   Co-applicants: {len(co_apps)} found")
            for co in co_apps:
                print(f"     - {co}")
            
            # Check guarantors
            result = conn.execute(text("SELECT * FROM guarantor WHERE loan_application_id = 1"))
            guars = result.fetchall()
            print(f"   Guarantors: {len(guars)} found")
            for gu in guars:
                print(f"     - {gu}")
            
            # Check references
            result = conn.execute(text("SELECT * FROM applicant_references WHERE loan_application_id = 1"))
            refs = result.fetchall()
            print(f"   References: {len(refs)} found")
            for ref in refs:
                print(f"     - {ref}")
        else:
            print("   ❌ No loan found with loan_application_id = 1")
        
        # Check table structure
        print("\n🏗️ 7. TABLE STRUCTURES:")
        tables = ['co_applicant', 'guarantor', 'applicant_references']
        for table in tables:
            try:
                result = conn.execute(text(f"DESCRIBE {table}"))
                print(f"\n   {table.upper()} structure:")
                for row in result:
                    print(f"     {row[0]}: {row[1]} {row[2]} {row[3]}")
            except Exception as e:
                print(f"   ❌ Error describing {table}: {e}")

if __name__ == "__main__":
    debug_contacts()
