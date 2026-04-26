"""
Data Loader Module
Handles loading data from CSV files
"""

import pandas as pd
import os


class DataLoader:
    """Loads and processes data from CSV files"""
    
    def __init__(self, csv_path):
        """Initialize data loader"""
        self.csv_path = csv_path
        self.df = None
    
    def load_csv(self):
        """Load CSV file into DataFrame"""
        try:
            if not os.path.exists(self.csv_path):
                print(f"File not found: {self.csv_path}")
                return None
            
            self.df = pd.read_csv(self.csv_path)
            print(f"✅ Loaded {len(self.df)} records from CSV")
            return self.df
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return None
    
    def get_data(self):
        """Get loaded data"""
        return self.df
    
    def get_columns(self):
        """Get column names"""
        if self.df is None:
            return []
        return self.df.columns.tolist()
    
    def get_shape(self):
        """Get data shape (rows, columns)"""
        if self.df is None:
            return (0, 0)
        return self.df.shape
    
    def preview(self, n=5):
        """Get preview of first n rows"""
        if self.df is None:
            return None
        return self.df.head(n)
    
    def clean_data(self):
        """Clean data: remove duplicates and handle missing values"""
        if self.df is None:
            return False
        
        try:
            # Remove duplicate rows
            self.df = self.df.drop_duplicates()
            
            # Handle missing values
            self.df = self.df.fillna('Unknown')
            
            print(f"✅ Data cleaned. Final records: {len(self.df)}")
            return True
        except Exception as e:
            print(f"❌ Error cleaning data: {e}")
            return False
    
    def prepare_for_db(self):
        """
        Prepare data for database insertion
        Maps CSV columns to database columns
        """
        if self.df is None:
            return None
        
        try:
            # Standardize column names (case-insensitive)
            self.df.columns = self.df.columns.str.lower()
            
            # Map and select required columns if they exist
            required_cols = ['crime_type', 'city', 'date', 'time', 'gender', 'weapon']
            
            # Check if required columns exist
            available_cols = [col for col in required_cols if col in self.df.columns]
            
            if len(available_cols) > 0:
                return self.df[available_cols]
            else:
                return self.df
        except Exception as e:
            print(f"❌ Error preparing data: {e}")
            return None
    
    def get_column_mapping(self):
        """Get mapping of CSV columns to database columns"""
        if self.df is None:
            return {}
        
        mapping = {
            'crime_type': 'type',
            'city': 'city',
            'date': 'date',
            'time': 'time',
            'gender': 'gender',
            'weapon': 'weapon'
        }
        
        return mapping
