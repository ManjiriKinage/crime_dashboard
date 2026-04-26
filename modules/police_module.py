"""
Police Module
Handles police officer operations: login, register, CRUD operations
"""

import streamlit as st
from datetime import datetime, time
from modules.db_operations import DatabaseManager


class PoliceOfficer:
    """Manages police officer operations"""
    
    def __init__(self):
        """Initialize police officer module"""
        self.db = DatabaseManager()
    
    # ==================== AUTHENTICATION ====================
    
    def register_officer(self, username, password, confirm_password, name, badge_number, email):
        """Register a new police officer"""
        
        # Validation
        if not username or not password or not name or not badge_number:
            return False, "❌ All fields are required"
        
        if len(username) < 4:
            return False, "❌ Username must be at least 4 characters"
        
        if len(password) < 6:
            return False, "❌ Password must be at least 6 characters"
        
        if password != confirm_password:
            return False, "❌ Passwords do not match"
        
        if self.db.police_exists(username):
            return False, "❌ Username already exists"
        
        # Register
        success, message = self.db.register_police(username, password, name, badge_number, email)
        return success, message
    
    def login_officer(self, username, password):
        """Authenticate police officer"""
        
        if not username or not password:
            return False, None, "❌ Please enter both username and password"
        
        success, officer_data, message = self.db.authenticate_police(username, password)
        return success, officer_data, message
    
    # ==================== CRIME RECORD OPERATIONS ====================
    
    def add_crime_record(self, crime_type, city, date, time_val, gender, weapon, officer_id, officer_name):
        """Add a new crime record with validation"""
        
        # Input validation
        errors = self.validate_crime_input(crime_type, city, date, time_val, gender, weapon)
        if errors:
            return False, ", ".join(errors)
        
        try:
            crime_data = (
                crime_type.strip(),
                city.strip(),
                date,
                time_val,
                gender if gender != "Select" else None,
                weapon.strip(),
                officer_id
            )
            
            if self.db.add_crime(crime_data):
                # Log the operation
                self.db.log_operation(officer_id, officer_name, "ADD", None, crime_type, city, f"Added by {officer_name}")
                return True, f"✅ Crime record added successfully!"
            else:
                return False, "❌ Failed to add crime record"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def update_crime_record(self, record_id, crime_type, city, date, time_val, gender, weapon, officer_id, officer_name):
        """Update existing crime record"""
        
        # Input validation
        errors = self.validate_crime_input(crime_type, city, date, time_val, gender, weapon)
        if errors:
            return False, ", ".join(errors)
        
        try:
            crime_data = (
                crime_type.strip(),
                city.strip(),
                date,
                time_val,
                gender if gender != "Select" else None,
                weapon.strip()
            )
            
            if self.db.update_crime(record_id, crime_data):
                # Log the operation
                self.db.log_operation(officer_id, officer_name, "UPDATE", record_id, crime_type, city, f"Updated by {officer_name}")
                return True, f"✅ Crime record updated successfully!"
            else:
                return False, "❌ Failed to update crime record"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def delete_crime_record(self, record_id, officer_id, officer_name, crime_type=None, city=None):
        """Delete a crime record"""
        try:
            if self.db.delete_crime(record_id):
                # Log the operation
                self.db.log_operation(officer_id, officer_name, "DELETE", record_id, crime_type, city, f"Deleted by {officer_name}")
                return True, f"✅ Crime record deleted successfully!"
            else:
                return False, "❌ Failed to delete crime record"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def get_all_records(self):
        """Get all crime records"""
        try:
            columns, results = self.db.fetch_all_crimes()
            return columns, results
        except Exception as e:
            return None, None
    
    def get_record_by_id(self, record_id):
        """Get specific crime record by ID"""
        try:
            result = self.db.fetch_crime_by_id(record_id)
            return result
        except Exception as e:
            return None
    
    # ==================== VALIDATION ====================
    
    def validate_crime_input(self, crime_type, city, date, time_val, gender, weapon):
        """Validate crime record input"""
        errors = []
        
        if not crime_type or crime_type.strip() == "":
            errors.append("Crime type is required")
        
        if not city or city.strip() == "":
            errors.append("City is required")
        
        if date is None:
            errors.append("Date is required")
        
        if time_val is None:
            errors.append("Time is required")
        
        if not weapon or weapon.strip() == "":
            errors.append("Weapon is required")
        
        # Check if date is not in future
        if date and date > datetime.now().date():
            errors.append("Date cannot be in the future")
        
        return errors
    
    # ==================== UI HELPERS ====================
    
    @staticmethod
    def get_crime_types():
        """Get list of common crime types"""
        return [
            "Theft",
            "Robbery",
            "Assault",
            "Murder",
            "Rape",
            "Burglary",
            "Fraud",
            "Cybercrime",
            "Drug Trafficking",
            "Homicide",
            "Kidnapping",
            "Vandalism",
            "Vehicle Theft",
            "Counterfeiting",
            "Extortion",
            "Public Intoxication",
            "Sexual Assault",
            "Arson",
            "Identity Theft",
            "Other"
        ]
    
    @staticmethod
    def get_indian_cities():
        """Get list of major Indian cities"""
        return [
            "Ahmedabad", "Bangalore", "Bhopal", "Chandigarh", "Chennai",
            "Coimbatore", "Delhi", "Ghaziabad", "Goa", "Gurgaon",
            "Hyderabad", "Indore", "Jaipur", "Kolkata", "Kochi",
            "Lucknow", "Ludhiana", "Mumbai", "Nagpur", "Noida",
            "Pune", "Rajkot", "Surat", "Visakhapatnam", "Vadodara",
            "Amritsar", "Aurangabad", "Bikaner", "Cuttack", "Durgapur",
            "Ernakulam", "Faridabad", "Guwahati", "Hubballi", "Jabalpur",
            "Jamshedpur", "Jodhpur", "Kanpur", "Kota", "Madurai",
            "Meerut", "Nashik", "Patna", "Puducherry", "Ranchi",
            "Shillong", "Srinagar", "Thrissur", "Udaipur", "Varanasi",
            "Other"
        ]
    
    @staticmethod
    def get_indian_states():
        """Get list of Indian states and territories"""
        return [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
            "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
            "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
            "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
            "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
            "Uttar Pradesh", "Uttarakhand", "West Bengal"
        ]
    
    @staticmethod
    def get_weapons():
        """Get list of common weapons"""
        return [
            "Gun", "Knife", "Sword", "Baseball Bat", "Hammer",
            "Stone", "Fire", "Acid", "Poison", "Blunt Object",
            "Firearm", "Explosives", "Rope", "Club", "Axe",
            "Crowbar", "Bottle", "Syringe", "Torch", "Other"
        ]
    
    @staticmethod
    def get_genders():
        """Get gender options"""
        return ["Male", "Female", "Other"]
