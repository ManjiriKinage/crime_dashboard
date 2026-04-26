"""
Quick Start Guide - Crime Record Management System
Run this file to test all components
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from modules.db_operations import DatabaseManager
from modules.police_module import PoliceOfficer
from modules.analysis import CrimeAnalyzer


def print_section(title):
    """Print formatted section title"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_database_connection():
    """Test database connection"""
    print_section("Testing Database Connection")
    
    db = DatabaseManager()
    if db.connect():
        print("✅ Successfully connected to MySQL database")
        db.close()
        return True
    else:
        print("❌ Failed to connect to database")
        print("\nTroubleshooting Steps:")
        print("1. Ensure MySQL server is running")
        print("2. Check db_config.py for correct credentials")
        print("3. Verify database name in db_config.py")
        return False


def show_database_info():
    """Show database information"""
    print_section("Database Information")
    
    from db_config import DB_CONFIG, DATABASE_NAME, TABLE_NAME, POLICE_TABLE
    
    print(f"Host: {DB_CONFIG['host']}")
    print(f"User: {DB_CONFIG['user']}")
    print(f"Database: {DATABASE_NAME}")
    print(f"Crime Table: {TABLE_NAME}")
    print(f"Police Table: {POLICE_TABLE}")


def show_police_options():
    """Display police officer features"""
    print_section("Police Officer Module Features")
    
    police = PoliceOfficer()
    
    print("\n📋 Crime Types:")
    for i, crime in enumerate(police.get_crime_types(), 1):
        print(f"  {i}. {crime}")
    
    print("\n📍 Available States/Cities (Sample):")
    cities = police.get_indian_states()
    for i, city in enumerate(cities[:10], 1):
        print(f"  {i}. {city}")
    print(f"  ... and {len(cities)-10} more")
    
    print("\n🔫 Weapons:")
    for i, weapon in enumerate(police.get_weapons(), 1):
        print(f"  {i}. {weapon}")
    
    print("\n👥 Gender Options:")
    for i, gender in enumerate(police.get_genders(), 1):
        print(f"  {i}. {gender}")


def show_data_info():
    """Show data analysis information"""
    print_section("Crime Analysis Dashboard Features")
    
    db = DatabaseManager()
    if not db.connect():
        print("❌ Cannot connect to database")
        return
    
    columns, results = db.fetch_all_crimes()
    db.close()
    
    if results is None:
        print("❌ Cannot fetch data")
        return
    
    print(f"Total Crime Records: {len(results)}")
    
    if len(results) > 0:
        print("\nAnalysis Capabilities:")
        print("  ✓ Crime count by city")
        print("  ✓ Crime distribution by type")
        print("  ✓ Victim gender analysis")
        print("  ✓ Weapon usage statistics")
        print("  ✓ Monthly crime trends")
        print("  ✓ Safety level assessment")
        
        print("\nVisualization Options:")
        print("  ✓ Bar charts (by city, by type)")
        print("  ✓ Line charts (monthly trends)")
        print("  ✓ Pie charts (gender, weapons)")
        print("  ✓ Interactive Plotly charts")
    else:
        print("⚠️  No crime records found in database")
        print("Add some records using Police Panel to see analytics")


def show_test_credentials():
    """Show test credentials"""
    print_section("Test Credentials (After Setting Up Database)")
    
    print("\nSample Police Officers:")
    print("  Username: officer_01 | Password: pass123")
    print("  Username: officer_02 | Password: pass123")
    print("  Username: officer_03 | Password: pass123")
    
    print("\n⚠️  Note: These credentials are available after running setup_database.sql")


def show_next_steps():
    """Show next steps"""
    print_section("Next Steps")
    
    print("\n1. Database Setup:")
    print("   python setup_database.sql (or use MySQL CLI)")
    print("   mysql -u root -p < setup_database.sql")
    
    print("\n2. Install Dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n3. Run Application:")
    print("   streamlit run app.py")
    
    print("\n4. Open in Browser:")
    print("   http://localhost:8501")
    
    print("\n5. First Time:")
    print("   - Go to Setup tab → Create Database Tables")
    print("   - Register as Police Officer")
    print("   - Add crime records")
    print("   - View analytics in Dashboard")


def main():
    """Main test function"""
    
    print("\n" + "🚨"*30)
    print("  CRIME RECORD MANAGEMENT SYSTEM - QUICK START")
    print("🚨"*30)
    
    # Show information
    show_database_info()
    
    # Test connection
    if not test_database_connection():
        print("\n⚠️  Database connection failed. Please set up MySQL first.")
        print("\nDatabase Setup Instructions:")
        print("1. Install MySQL Server")
        print("2. Update db_config.py with your credentials")
        print("3. Run: mysql -u root -p < setup_database.sql")
        return
    
    # Show options
    show_police_options()
    show_data_info()
    show_test_credentials()
    
    # Next steps
    show_next_steps()
    
    print("\n" + "="*60)
    print("✅ Quick start guide complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
