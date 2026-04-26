#!/usr/bin/env python
"""
Database Recreation Script
Drops and recreates the database with correct schema
"""

import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG

def recreate_database():
    """Recreate database with correct schema"""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        
        print("="*60)
        print("  DATABASE RECREATION - Crime Management System")
        print("="*60)
        print()
        
        # Drop existing database
        print("🗑️  Dropping existing database...")
        cursor.execute("DROP DATABASE IF EXISTS crime_db")
        print("✅ Database dropped")
        
        # Create new database
        print("📁 Creating new database...")
        cursor.execute("CREATE DATABASE crime_db")
        print("✅ Database created")
        
        # Use the database
        cursor.execute("USE crime_db")
        
        # Create police_officers table
        print("👮 Creating police_officers table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS police_officers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(100) NOT NULL,
                badge_number VARCHAR(20) UNIQUE NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_username (username),
                INDEX idx_badge (badge_number)
            )
        """)
        print("✅ police_officers table created")
        
        # Create crimes table
        print("🚨 Creating crimes table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crimes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(100) NOT NULL,
                city VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                gender VARCHAR(20),
                weapon VARCHAR(100),
                recorded_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recorded_by) REFERENCES police_officers(id),
                INDEX idx_city (city),
                INDEX idx_type (type),
                INDEX idx_date (date),
                INDEX idx_gender (gender)
            )
        """)
        print("✅ crimes table created")
        
        # Insert sample police officers
        print()
        print("👮 Inserting sample police officers...")
        cursor.execute("""
            INSERT INTO police_officers (username, password, name, badge_number, email) VALUES
            ('officer_01', 'pass123', 'Raj Kumar', 'PB001', 'raj.kumar@police.gov.in'),
            ('officer_02', 'pass123', 'Priya Singh', 'PB002', 'priya.singh@police.gov.in'),
            ('officer_03', 'pass123', 'Amit Patel', 'PB003', 'amit.patel@police.gov.in')
        """)
        print(f"✅ 3 police officers inserted")
        
        # Insert sample crime records
        print("🚨 Inserting sample crime records...")
        crimes_data = [
            ('Theft', 'Mumbai', '2024-01-15', '14:30:00', 'Male', 'Knife', 1),
            ('Robbery', 'Delhi', '2024-01-14', '22:45:00', 'Female', 'Gun', 2),
            ('Assault', 'Bangalore', '2024-01-13', '10:15:00', 'Male', 'Baseball Bat', 3),
            ('Murder', 'Chennai', '2024-01-12', '23:30:00', 'Female', 'Knife', 1),
            ('Fraud', 'Hyderabad', '2024-01-11', '09:00:00', 'Other', 'Poison', 2),
            ('Burglary', 'Pune', '2024-01-10', '03:00:00', 'Male', 'Stone', 3),
            ('Drug Trafficking', 'Kolkata', '2024-01-09', '18:20:00', 'Male', 'Gun', 1),
            ('Assault', 'Mumbai', '2024-01-08', '16:45:00', 'Female', 'Hammer', 2),
            ('Theft', 'Delhi', '2024-01-07', '12:00:00', 'Female', 'Knife', 3),
            ('Robbery', 'Bangalore', '2024-01-06', '20:30:00', 'Male', 'Sword', 1)
        ]
        
        for crime in crimes_data:
            cursor.execute("""
                INSERT INTO crimes (type, city, date, time, gender, weapon, recorded_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, crime)
        
        print(f"✅ 10 crime records inserted")
        
        connection.commit()
        
        print()
        print("="*60)
        print("✅ Database recreation completed successfully!")
        print()
        print("📊 Database Summary:")
        print("   - Police Officers: 3")
        print("   - Crime Records: 10")
        print()
        print("🔐 Login Credentials:")
        print("   - Username: officer_01, officer_02, or officer_03")
        print("   - Password: pass123")
        print()
        print("="*60)
        
        cursor.close()
        connection.close()
        return True
        
    except Error as err:
        print(f"❌ Database recreation failed: {err}")
        return False

if __name__ == "__main__":
    recreate_database()
