"""
Filters Module
Handles data filtering operations
"""

import pandas as pd
from modules.db_operations import DatabaseManager


class DataFilter:
    """Filters crime data based on various criteria"""
    
    def __init__(self):
        """Initialize filter"""
        self.db = DatabaseManager()
        self.df = None
    
    def load_data(self):
        """Load all data from database"""
        try:
            columns, results = self.db.fetch_all_crimes()
            if results is None:
                return False
            
            self.df = pd.DataFrame(results, columns=columns)
            self.df['date'] = pd.to_datetime(self.df['date'])
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_unique_cities(self):
        """Get unique cities from data"""
        if self.df is None:
            return []
        return sorted(self.df['city'].unique().tolist())
    
    def get_unique_crime_types(self):
        """Get unique crime types from data"""
        if self.df is None:
            return []
        return sorted(self.df['type'].unique().tolist())
    
    def get_unique_genders(self):
        """Get unique gender values from data"""
        if self.df is None:
            return []
        return sorted(self.df['gender'].dropna().unique().tolist())
    
    def get_unique_weapons(self):
        """Get unique weapons from data"""
        if self.df is None:
            return []
        return sorted(self.df['weapon'].dropna().unique().tolist())
    
    def filter_by_city(self, city):
        """Filter crimes by city"""
        if self.df is None or len(self.df) == 0:
            return None
        
        return self.df[self.df['city'] == city]
    
    def filter_by_crime_type(self, crime_type):
        """Filter crimes by type"""
        if self.df is None or len(self.df) == 0:
            return None
        
        return self.df[self.df['type'] == crime_type]
    
    def filter_by_gender(self, gender):
        """Filter crimes by victim gender"""
        if self.df is None or len(self.df) == 0:
            return None
        
        return self.df[self.df['gender'] == gender]
    
    def filter_multiple(self, city=None, crime_type=None, gender=None):
        """
        Filter by multiple criteria
        Returns filtered dataframe
        """
        if self.df is None or len(self.df) == 0:
            return None
        
        result = self.df.copy()
        
        if city and city != "All":
            result = result[result['city'] == city]
        
        if crime_type and crime_type != "All":
            result = result[result['type'] == crime_type]
        
        if gender and gender != "All":
            result = result[result['gender'] == gender]
        
        return result
    
    def filter_by_date_range(self, start_date, end_date):
        """Filter crimes by date range"""
        if self.df is None or len(self.df) == 0:
            return None
        
        return self.df[(self.df['date'] >= start_date) & (self.df['date'] <= end_date)]
    
    def get_summary_stats(self, filtered_df=None):
        """Get summary statistics"""
        df = filtered_df if filtered_df is not None else self.df
        
        if df is None or len(df) == 0:
            return {
                'total_crimes': 0,
                'unique_cities': 0,
                'unique_types': 0,
                'most_common_weapon': 'N/A'
            }
        
        return {
            'total_crimes': len(df),
            'unique_cities': df['city'].nunique(),
            'unique_types': df['type'].nunique(),
            'most_common_weapon': df['weapon'].mode().values[0] if len(df) > 0 else 'N/A'
        }
