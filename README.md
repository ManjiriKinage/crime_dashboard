# 🚨 Crime Record Management & Analysis System

A complete full-stack Python application for managing and analyzing crime records. Features police officer authentication, CRUD operations, and comprehensive crime analytics with visualizations.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Module Descriptions](#module-descriptions)

---

## ✨ Features

### 👮 Police Officer Module
- **User Authentication**
  - Login for existing officers
  - Self-registration for new officers
  - Secure password storage

- **Crime Record Management (CRUD)**
  - Add new crime records
  - Update existing records
  - Delete records with confirmation
  - View all records in tabular format

- **Input Validation**
  - Automatic data validation
  - Error messages for invalid inputs
  - Future date prevention

### 📊 Crime Analysis Dashboard
- **Advanced Filtering**
  - Filter by City
  - Filter by Crime Type
  - Filter by Victim Gender
  - Real-time data filtering

- **Analytics & Insights**
  - Crime count by city
  - Monthly trend analysis
  - Gender distribution analysis
  - Weapon usage statistics

- **Visualizations**
  - Bar charts for crime distribution
  - Line charts for trends
  - Pie charts for gender & weapon usage
  - Interactive Plotly charts

- **Safety Assessment**
  - Safety Level indicators (Safe/Moderate/High Risk)
  - Real-time crime statistics
  - Emergency contact information

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Backend** | Python |
| **Database** | MySQL |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly |
| **DB Connector** | mysql-connector-python |
| **Navigation** | streamlit-option-menu |

---

## 📁 Project Structure

```
crime_dashboard/
│
├── app.py                          # Main application entry point
├── db_config.py                    # Database configuration
├── requirements.txt                # Python dependencies
├── setup_database.sql              # Database initialization script
│
├── modules/
│   ├── db_operations.py           # Database CRUD operations
│   ├── police_module.py            # Police officer operations
│   ├── analysis.py                 # Crime data analysis
│   ├── filters.py                  # Data filtering utilities
│   ├── dashboard.py                # Dashboard UI components
│   └── data_loader.py              # CSV data loading
│
└── data/
    └── crime_data.csv              # Sample crime data (if available)
```

---

## 📦 Prerequisites

- **Python 3.8+**
- **MySQL Server** (running locally or remote)
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### System Requirements
- RAM: 2GB minimum
- Disk Space: 500MB
- Internet Connection: For package installation

---

## 🚀 Installation

### Step 1: Clone or Download Project

```bash
# If using git
git clone <repository-url>
cd crime_dashboard

# Or navigate to the project directory
cd D:\projects\crime_record\crime_dashboard
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues, install packages individually:

```bash
pip install streamlit==1.28.0
pip install pandas==2.0.3
pip install mysql-connector-python==8.2.0
pip install plotly==5.17.0
pip install numpy==1.24.3
pip install streamlit-option-menu==0.3.6
```

---

## 🗄️ Database Setup

### Step 1: Start MySQL Server

**Windows:**
```bash
# If MySQL is installed as a service
net start MySQL80

# Or start MySQL manually from installation directory
```

**macOS:**
```bash
mysql.server start
```

**Linux:**
```bash
sudo systemctl start mysql
```

### Step 2: Update Database Configuration

Edit `db_config.py` and update the credentials:

```python
DB_CONFIG = {
    'host': 'localhost',        # Your MySQL host
    'user': 'root',             # Your MySQL username
    'password': 'your_password', # Your MySQL password ⚠️ CHANGE THIS
    'database': 'crime_db'
}
```

### Step 3: Create Database and Tables

**Option A: Using MySQL CLI**

```bash
# Open MySQL command line
mysql -u root -p

# Execute SQL script
source setup_database.sql;

# Or paste the contents of setup_database.sql
```

**Option B: Using Python (In-App)**

1. Run the application: `streamlit run app.py`
2. Go to **⚙️ Setup** → Click "Create Database Tables"
3. Tables will be created automatically

**Option C: Manual SQL Execution**

```bash
# Copy contents from setup_database.sql and execute in MySQL Workbench or CLI
```

### Step 4: Verify Database Creation

```sql
-- Check if database exists
SHOW DATABASES;

-- Check tables
USE crime_db;
SHOW TABLES;

-- View table structure
DESC police_officers;
DESC crimes;
```

---

## ⚙️ Configuration

### Database Connection

The application uses settings from `db_config.py`. Key settings:

```python
DB_CONFIG = {
    'host': 'localhost',        # MySQL server address
    'user': 'root',             # MySQL username
    'password': 'password',     # MySQL password
    'database': 'crime_db'      # Database name
}

DATABASE_NAME = 'crime_db'      # Database to use
TABLE_NAME = 'crimes'           # Crime records table
POLICE_TABLE = 'police_officers' # Police officers table
```

### Streamlit Configuration (Optional)

Create `.streamlit/config.toml` in the project directory:

```toml
[theme]
primaryColor = "#FF0000"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[client]
maxUploadSize = 200

[server]
maxUploadSize = 200
```

---

## 🎯 Running the Application

### Start the Application

```bash
# Ensure virtual environment is activated
streamlit run app.py
```

### Expected Output

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Open in Browser

Click on the local URL or open your browser and go to:
```
http://localhost:8501
```

### Stop the Application

Press `Ctrl+C` in the terminal where Streamlit is running.

---

## 📖 Usage Guide

### 1️⃣ First-Time Setup

1. **Create Database Tables**
   - Go to ⚙️ Setup tab
   - Click "Create Database Tables"
   - Confirm successful creation

2. **Register Police Officer**
   - On login page, click "Register" tab
   - Fill in details:
     - Full Name
     - Email
     - Badge Number (unique)
     - Username (4+ characters)
     - Password (6+ characters)
   - Click Register

### 2️⃣ Login

1. Go to Login tab
2. Enter Username and Password
3. Click "Login" button
4. On success, redirected to Police Panel

### 3️⃣ Police Panel Operations

#### ➕ Add Crime Record
1. Select "Add Crime Record"
2. Fill in form:
   - **Crime Type**: Select from dropdown
   - **City**: Select Indian state/city
   - **Crime Date**: Pick date
   - **Time**: Select time
   - **Victim Gender**: Choose gender
   - **Weapon**: Select weapon type
3. Click "Add Record"
4. Success message confirms

#### ✏️ Update Record
1. Select "Update Record"
2. Choose record from dropdown
3. Modify any field
4. Click "Update Record"

#### 🗑️ Delete Record
1. Select "Delete Record"
2. Choose record to delete
3. Review warning
4. Click "Delete" to confirm

#### 📋 View All Records
1. Select "View All Records"
2. See all crime records in table format

### 4️⃣ Crime Analysis Dashboard

1. Select "Dashboard" from sidebar
2. **Use Filters (Left Sidebar)**
   - Select City: View crimes in specific city
   - Select Crime Type: Filter by crime type
   - Select Gender: Filter by victim gender

3. **View Analysis Tabs**
   - 📍 **By City**: Bar chart of crimes by city
   - ⚠️ **By Type**: Bar chart of crime types
   - 📈 **Trend**: Monthly trend line chart
   - 👥 **Gender**: Gender distribution pie chart
   - 🔫 **Weapons**: Weapon usage pie chart

4. **Review Statistics**
   - Total crimes
   - Number of cities
   - Crime types count
   - Most common weapon

5. **Safety Status**
   - 🟢 Safe: < 5 crimes
   - 🟡 Moderate: 5-15 crimes
   - 🔴 High Risk: > 15 crimes

6. **Emergency Contacts**
   - Police: 100
   - Women Safety: 1091
   - Ambulance: 102

### 5️⃣ Logout

Click "Logout" button on Police Panel to logout and return to login page.

---

## 📚 Module Descriptions

### `app.py`
**Main application file**
- Streamlit UI configuration
- Session state management
- Navigation between modules
- Authentication pages
- Main app logic

### `db_config.py`
**Database configuration**
- MySQL connection settings
- Database and table names
- Application constants

### `modules/db_operations.py`
**Database operations**
- `DatabaseManager` class handles:
  - Database connection/disconnection
  - Table creation
  - Crime CRUD operations
  - Police officer authentication
  - Data retrieval

**Key Functions:**
- `connect()` - Establish DB connection
- `create_tables()` - Initialize tables
- `add_crime()` - Insert crime record
- `update_crime()` - Update record
- `delete_crime()` - Delete record
- `authenticate_police()` - Login verification

### `modules/police_module.py`
**Police officer operations**
- `PoliceOfficer` class handles:
  - Officer registration
  - Officer login
  - Crime record management
  - Input validation
  - Dropdown data for forms

**Key Functions:**
- `register_officer()` - New officer signup
- `login_officer()` - Officer authentication
- `add_crime_record()` - Add crime with validation
- `update_crime_record()` - Update record
- `delete_crime_record()` - Delete record
- `validate_crime_input()` - Validate form input

### `modules/analysis.py`
**Data analysis**
- `CrimeAnalyzer` class handles:
  - Loading data from database
  - Statistical calculations
  - Chart generation
  - Trend analysis

**Key Functions:**
- `load_data()` - Load into DataFrame
- `crime_count_by_city()` - Count by city
- `gender_distribution()` - Gender stats
- `monthly_trend()` - Time series data
- `safety_level()` - Calculate safety
- `bar_chart_city_crimes()` - Generate chart
- `line_chart_monthly_trend()` - Trend chart
- `pie_chart_gender_distribution()` - Gender chart

### `modules/filters.py`
**Data filtering**
- `DataFilter` class handles:
  - Data loading
  - Filtering operations
  - Dropdown categories
  - Summary statistics

**Key Functions:**
- `get_unique_cities()` - Get city list
- `get_unique_crime_types()` - Get crime types
- `filter_by_city()` - Single filter
- `filter_multiple()` - Multi-criteria filter
- `get_summary_stats()` - Statistics

### `modules/dashboard.py`
**Dashboard UI**
- `Dashboard` class handles:
  - Dashboard rendering
  - Filter UI
  - Chart display
  - Emergency contacts
  - Summary cards

**Key Functions:**
- `render_header()` - Dashboard header
- `render_filters()` - Filter sidebar
- `render_analysis_section()` - Charts and tabs
- `render_data_table()` - Data visualization
- `render_emergency_contacts()` - Contact info

### `modules/data_loader.py`
**Data loading utility**
- `DataLoader` class handles:
  - CSV file loading
  - Data cleaning
  - Data preparation for DB

---

## 🔒 Security Considerations

1. **Password Storage**: Currently stored in plaintext (for demo). Use proper hashing in production:
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

2. **Database Credentials**: 
   - ⚠️ Never commit `db_config.py` to public repositories
   - Use environment variables for sensitive data:
   ```python
   import os
   PASSWORD = os.getenv('DB_PASSWORD')
   ```

3. **SQL Injection Prevention**: Already using parameterized queries with `%s` placeholders

4. **Access Control**: Implement role-based access in production

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'mysql'"

**Solution:**
```bash
pip install mysql-connector-python
```

### Issue: "Connection refused" - Cannot connect to MySQL

**Solution:**
1. Check if MySQL is running:
   ```bash
   # Windows
   tasklist | findstr mysql
   
   # Linux
   sudo systemctl status mysql
   ```
2. Verify credentials in `db_config.py`
3. Check MySQL port (default 3306)

### Issue: "Access denied for user 'root'@'localhost'"

**Solution:**
1. Update password in `db_config.py`
2. Reset MySQL root password if forgotten

### Issue: "Permission denied" when running

**Solution:**
```bash
# Linux/Mac
chmod +x app.py
python -m streamlit run app.py
```

### Issue: Tables not visible after setup

**Solution:**
```sql
USE crime_db;
SHOW TABLES;
DESCRIBE crimes;
DESCRIBE police_officers;
```

---

## 📊 Sample Data

The `setup_database.sql` includes sample data:

**Sample Police Officers:**
- Username: `officer_01`, Password: `pass123`
- Username: `officer_02`, Password: `pass123`
- Username: `officer_03`, Password: `pass123`

**Sample Crime Records:**
- 10 crime records across different cities
- Various crime types (Theft, Robbery, Assault, etc.)
- Different weapons used

---

## 🔄 Workflow

```
1. User Registration
   ↓
2. User Login (Authentication)
   ↓
3. Police Panel Access
   ├→ Add Crime Record
   ├→ Update Crime Record
   ├→ Delete Crime Record
   └→ View All Records
   ↓
4. Crime Analysis Dashboard
   ├→ Apply Filters
   ├→ View Statistics
   ├→ Analyze Charts
   └→ Review Safety Status
   ↓
5. Logout
```

---

## 📈 Future Enhancements

- [ ] Advanced authentication (2FA)
- [ ] Role-based access control
- [ ] Password hashing with bcrypt
- [ ] Email notifications
- [ ] Data export to PDF/Excel
- [ ] Advanced search functionality
- [ ] API integration
- [ ] Mobile app version
- [ ] Predictive analytics
- [ ] Machine learning models

---

## 📝 License

This project is for educational and demonstration purposes.

---

## 👥 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review module documentation
3. Check error messages in Streamlit UI

---

## 📞 Contact

For support, contact your development team or administrator.

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Status:** ✅ Production Ready

---

**Happy Crime Analysis! 🚨**
