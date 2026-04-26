#!/usr/bin/env python
"""
Database Schema Fix Script
Fixes the crimes table to include recorded_by column
"""

import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG, DATABASE_NAME, TABLE_NAME, POLICE_TABLE

def fix_database():
    """Fix database schema issues"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("="*60)
        print("  DATABASE SCHEMA FIX - Crime Record Management System")
        print("="*60)
        print()
        
        # Check if recorded_by column exists
        print("🔍 Checking crimes table structure...")
        cursor.execute(f"DESC {TABLE_NAME}")
        columns = [row[0] for row in cursor.fetchall()]
        
        if 'recorded_by' in columns:
            print("✅ Column 'recorded_by' already exists")
        else:
            print("❌ Column 'recorded_by' missing - adding it...")
            # Add the missing column
            cursor.execute(f"""
                ALTER TABLE {TABLE_NAME}
                ADD COLUMN recorded_by INT AFTER weapon
            """)
            print("✅ Column 'recorded_by' added")
        
        # Check for foreign key
        print()
        print("🔍 Checking foreign key constraint...")
        cursor.execute(f"""
            SELECT CONSTRAINT_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = '{TABLE_NAME}' 
            AND COLUMN_NAME = 'recorded_by' 
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        fk_result = cursor.fetchone()
        
        if fk_result:
            print("✅ Foreign key constraint exists")
        else:
            print("❌ Foreign key constraint missing - adding it...")
            # Try to drop existing FK if it exists
            try:
                cursor.execute(f"""
                    ALTER TABLE {TABLE_NAME}
                    DROP FOREIGN KEY {TABLE_NAME}_ibfk_1
                """)
            except:
                pass
            
            # Add foreign key
            cursor.execute(f"""
                ALTER TABLE {TABLE_NAME}
                ADD CONSTRAINT fk_recorded_by
                FOREIGN KEY (recorded_by) REFERENCES {POLICE_TABLE}(id)
            """)
            print("✅ Foreign key constraint added")
        
        connection.commit()
        
        print()
        print("✅ Database schema fixed successfully!")
        print()
        print("Current crimes table structure:")
        cursor.execute(f"DESC {TABLE_NAME}")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as err:
        print(f"❌ Database fix failed: {err}")
        return False

if __name__ == "__main__":
    success = fix_database()
    print()
    print("="*60)
    if success:
        print("✅ You can now add crime records successfully!")
    else:
        print("❌ Please check your MySQL connection")
    print("="*60)
