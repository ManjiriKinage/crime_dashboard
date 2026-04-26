#!/usr/bin/env python
"""
Database Setup Script - Creates tables and loads sample data
"""

import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG, DATABASE_NAME

def setup_database():
    """Setup database tables and load sample data"""
    try:
        # Read SQL setup file
        with open('setup_database.sql', 'r') as f:
            sql_content = f.read()
        
        # Connect to MySQL (use_pure=True for better compatibility)
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            autocommit=False,
            use_pure=True
        )
        
        cursor = connection.cursor()
        
        # Process SQL file - remove comments and split
        lines = []
        for line in sql_content.split('\n'):
            # Remove comment part
            line = line.split('--')[0]
            if line.strip():
                lines.append(line)
        
        sql_content = '\n'.join(lines)
        
        # Split by semicolon to get individual statements
        statements = []
        current = ''
        for char in sql_content:
            if char == ';':
                if current.strip():
                    statements.append(current.strip())
                current = ''
            else:
                current += char
        
        if current.strip():
            statements.append(current.strip())
        
        # Execute statements
        for i, statement in enumerate(statements, 1):
            if not statement:
                continue
            
            try:
                # Clear any pending results
                while cursor.nextset():
                    pass
                
                # Determine statement type for better handling
                stmt_upper = statement.upper()
                
                cursor.execute(statement)
                
                # Fetch results if needed for SELECT statements
                if 'SELECT' in stmt_upper:
                    cursor.fetchall()
                
                # Log progress
                if 'CREATE DATABASE' in stmt_upper:
                    print(f"✅ Database created/selected")
                elif 'CREATE TABLE' in stmt_upper:
                    table_name = statement.split('IF NOT EXISTS')[1].strip().split()[0] if 'IF NOT EXISTS' in stmt_upper else 'Table'
                    print(f"✅ Table created: {table_name}")
                elif 'INSERT' in stmt_upper:
                    print(f"✅ Data inserted ({cursor.rowcount} rows)")
                    
            except Error as err:
                error_msg = str(err)
                if "already exists" in error_msg or ("1050" in error_msg):
                    print(f"⚠️  Already exists (OK)")
                elif cursor.rowcount > 0:
                    print(f"✅ Executed (affected {cursor.rowcount} rows)")
                else:
                    print(f"❌ Error: {err}")
        
        connection.commit()
        print("\n✅ Database setup completed!")
        print(f"📊 Database: {DATABASE_NAME}")
        print("📋 Tables created: police_officers, crimes")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as err:
        print(f"❌ Setup failed: {err}")
        try:
            connection.rollback()
            connection.close()
        except:
            pass
        return False

if __name__ == "__main__":
    print("="*60)
    print("  DATABASE SETUP - Crime Record Management System")
    print("="*60)
    print()
    
    success = setup_database()
    
    print()
    if success:
        print("✅ Now you can login with:")
        print("   Username: officer_01")
        print("   Password: pass123")
    else:
        print("❌ Please check your MySQL connection settings in db_config.py")
    
    print()
    print("="*60)
