"""
Setup audit log table for tracking operations
"""
import mysql.connector
from db_config import DB_CONFIG

def setup_audit_table():
    """Create audit_log table if it doesn't exist"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create audit_log table
        create_audit = """
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
            FOREIGN KEY (officer_id) REFERENCES police_officers(id)
        )
        """
        
        cursor.execute(create_audit)
        connection.commit()
        
        print("✅ Audit log table created successfully!")
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error creating audit table: {e}")

if __name__ == "__main__":
    setup_audit_table()
