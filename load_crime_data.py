"""
Load crime records from CSV file into the database
"""
import pandas as pd
import mysql.connector
from db_config import DB_CONFIG

def load_csv_to_database():
    """Load crime records from CSV file"""
    try:
        # Read CSV file
        csv_file = '../crime_dataset_india.csv'
        df = pd.read_csv(csv_file)
        
        print(f"📊 Loaded {len(df)} records from CSV file")
        print(f"Columns: {list(df.columns)}")
        
        # Connect to database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Get officer ID (use first officer or default to 1)
        cursor.execute("SELECT id FROM police_officers LIMIT 1")
        result = cursor.fetchone()
        default_officer_id = result[0] if result else 1
        
        inserted_count = 0
        skipped_count = 0
        
        # Insert records from CSV
        for index, row in df.iterrows():
            try:
                # Extract data from CSV
                crime_type = row['Crime Description'].strip() if pd.notna(row['Crime Description']) else 'Unknown'
                city = row['City'].strip() if pd.notna(row['City']) else 'Unknown'
                date_of_occurrence = row['Date of Occurrence']
                time_of_occurrence = row['Time of Occurrence']
                victim_gender = row['Victim Gender'].strip() if pd.notna(row['Victim Gender']) else 'Unknown'
                weapon_used = row['Weapon Used'].strip() if pd.notna(row['Weapon Used']) else 'Unknown'
                
                # Parse date and time
                if pd.notna(date_of_occurrence):
                    date_obj = pd.to_datetime(date_of_occurrence)
                    date_str = date_obj.strftime('%Y-%m-%d')
                else:
                    continue
                
                if pd.notna(time_of_occurrence):
                    time_obj = pd.to_datetime(time_of_occurrence)
                    time_str = time_obj.strftime('%H:%M:%S')
                else:
                    time_str = '00:00:00'
                
                # Normalize gender to Male/Female/Other
                gender_map = {'M': 'Male', 'F': 'Female', 'X': 'Other', 'Male': 'Male', 'Female': 'Female'}
                victim_gender = gender_map.get(victim_gender, 'Other')
                
                # Insert into database
                query = """
                INSERT INTO crimes (type, city, date, time, gender, weapon, recorded_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(query, (crime_type, city, date_str, time_str, victim_gender, weapon_used, default_officer_id))
                inserted_count += 1
                
            except Exception as e:
                skipped_count += 1
                print(f"⚠️ Skipped row {index + 1}: {str(e)}")
                continue
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"\n✅ CSV Data Loading Complete!")
        print(f"   ✓ Inserted: {inserted_count} records")
        print(f"   ⚠️ Skipped: {skipped_count} records")
        
    except Exception as e:
        print(f"❌ Error loading CSV: {str(e)}")

if __name__ == "__main__":
    load_csv_to_database()
