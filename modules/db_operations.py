"""
Database Operations Module
Handles all database operations: create, read, update, delete
"""

import mysql.connector
from mysql.connector import Error
import streamlit as st
from db_config import DB_CONFIG, DATABASE_NAME, TABLE_NAME, POLICE_TABLE


class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self):
        """Initialize database manager"""
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            return True
        except Error as e:
            st.error(f"❌ Database Connection Error: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
    
    def create_tables(self):
        """Create necessary database tables"""
        try:
            if not self.connect():
                return False
            
            # Create police_officers table for authentication
            create_police_table = f"""
            CREATE TABLE IF NOT EXISTS {POLICE_TABLE} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(100) NOT NULL,
                badge_number VARCHAR(20) UNIQUE NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Create crimes table for crime records
            create_crimes_table = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(100) NOT NULL,
                city VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                gender VARCHAR(20),
                weapon VARCHAR(100),
                recorded_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recorded_by) REFERENCES {POLICE_TABLE}(id)
            )
            """
            
            # Create audit_log table for tracking operations
            create_audit_table = f"""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                officer_id INT NOT NULL,
                officer_name VARCHAR(100) NOT NULL,
                operation VARCHAR(20) NOT NULL,
                record_id INT,
                crime_type VARCHAR(100),
                city VARCHAR(100),
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (officer_id) REFERENCES {POLICE_TABLE}(id)
            )
            """
            
            self.cursor.execute(create_police_table)
            self.cursor.execute(create_crimes_table)
            self.cursor.execute(create_audit_table)
            self.connection.commit()
            st.success("✅ Tables created successfully!")
            return True
        except Error as e:
            st.error(f"❌ Error creating tables: {e}")
            return False
        finally:
            self.close()
    
    # ==================== CRIME OPERATIONS ====================
    
    def add_crime(self, crime_data):
        """Add a new crime record to database"""
        try:
            if not self.connect():
                return False
            
            query = f"""
            INSERT INTO {TABLE_NAME} 
            (type, city, date, time, gender, weapon, recorded_by) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(query, crime_data)
            self.connection.commit()
            return True
        except Error as e:
            st.error(f"❌ Error adding crime record: {e}")
            return False
        finally:
            self.close()
    
    def update_crime(self, crime_id, crime_data):
        """Update an existing crime record"""
        try:
            if not self.connect():
                return False
            
            query = f"""
            UPDATE {TABLE_NAME} 
            SET type=%s, city=%s, date=%s, time=%s, gender=%s, weapon=%s 
            WHERE id=%s
            """
            
            self.cursor.execute(query, crime_data + (crime_id,))
            self.connection.commit()
            return True
        except Error as e:
            st.error(f"❌ Error updating crime record: {e}")
            return False
        finally:
            self.close()
    
    def delete_crime(self, crime_id):
        """Delete a crime record"""
        try:
            if not self.connect():
                return False
            
            query = f"DELETE FROM {TABLE_NAME} WHERE id=%s"
            self.cursor.execute(query, (crime_id,))
            self.connection.commit()
            return True
        except Error as e:
            st.error(f"❌ Error deleting crime record: {e}")
            return False
        finally:
            self.close()
    
    def fetch_all_crimes(self):
        """Fetch all crime records"""
        try:
            if not self.connect():
                return None
            
            query = f"SELECT * FROM {TABLE_NAME} ORDER BY created_at DESC"
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            results = self.cursor.fetchall()
            
            return columns, results
        except Error as e:
            st.error(f"❌ Error fetching records: {e}")
            return None, None
        finally:
            self.close()
    
    def fetch_crime_by_id(self, crime_id):
        """Fetch a specific crime record by ID"""
        try:
            if not self.connect():
                return None
            
            query = f"SELECT * FROM {TABLE_NAME} WHERE id=%s"
            self.cursor.execute(query, (crime_id,))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            st.error(f"❌ Error fetching record: {e}")
            return None
        finally:
            self.close()
    
    # ==================== POLICE OFFICER OPERATIONS ====================
    
    def register_police(self, username, password, name, badge_number, email):
        """Register a new police officer"""
        try:
            if not self.connect():
                return False, "Database connection failed"
            
            query = f"""
            INSERT INTO {POLICE_TABLE} 
            (username, password, name, badge_number, email) 
            VALUES (%s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(query, (username, password, name, badge_number, email))
            self.connection.commit()
            return True, "✅ Registration successful!"
        except mysql.connector.errors.IntegrityError as e:
            if "Duplicate entry" in str(e):
                return False, "❌ Username or Badge number already exists"
            return False, f"❌ Registration error: {e}"
        except Error as e:
            return False, f"❌ Error registering officer: {e}"
        finally:
            self.close()
    
    def authenticate_police(self, username, password):
        """Authenticate police officer"""
        try:
            if not self.connect():
                return False, None, "Database connection failed"
            
            query = f"SELECT id, name, badge_number FROM {POLICE_TABLE} WHERE username=%s AND password=%s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            
            if result:
                return True, result, "✅ Login successful!"
            else:
                return False, None, "❌ Invalid credentials"
        except Error as e:
            return False, None, f"❌ Login error: {e}"
        finally:
            self.close()
    
    def police_exists(self, username):
        """Check if police officer exists"""
        try:
            if not self.connect():
                return False
            
            query = f"SELECT id FROM {POLICE_TABLE} WHERE username=%s"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            return result is not None
        except Error as e:
            return False
        finally:
            self.close()
    
    # ==================== AUDIT LOG OPERATIONS ====================
    
    def log_operation(self, officer_id, officer_name, operation, record_id, crime_type, city, details):
        """Log an operation (add, update, delete) to audit trail"""
        try:
            if not self.connect():
                return False
            
            query = """
            INSERT INTO audit_log 
            (officer_id, officer_name, operation, record_id, crime_type, city, details) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(query, (officer_id, officer_name, operation, record_id, crime_type, city, details))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Audit log error: {e}")
            return False
        finally:
            self.close()
    
    def get_recent_operations(self, limit=20):
        """Get recent operations from audit log"""
        try:
            if not self.connect():
                return None, None
            
            query = """
            SELECT officer_name, operation, record_id, crime_type, city, timestamp
            FROM audit_log
            ORDER BY timestamp DESC
            LIMIT %s
            """
            
            self.cursor.execute(query, (limit,))
            results = self.cursor.fetchall()
            columns = ['Officer', 'Operation', 'Record ID', 'Crime Type', 'City', 'Timestamp']
            return columns, results
        except Error as e:
            print(f"Error fetching audit logs: {e}")
            return None, None
        finally:
            self.close()
    
    def get_officer_operations(self, officer_name, limit=20):
        """Get operations by a specific officer"""
        try:
            if not self.connect():
                return None, None
            
            query = """
            SELECT officer_name, operation, record_id, crime_type, city, timestamp
            FROM audit_log
            WHERE officer_name=%s
            ORDER BY timestamp DESC
            LIMIT %s
            """
            
            self.cursor.execute(query, (officer_name, limit))
            results = self.cursor.fetchall()
            columns = ['Officer', 'Operation', 'Record ID', 'Crime Type', 'City', 'Timestamp']
            return columns, results
        except Error as e:
            print(f"Error fetching officer operations: {e}")
            return None, None
        finally:
            self.close()
