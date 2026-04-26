# 🔧 Complete Setup Instructions

## Crime Record Management & Analysis System

This guide provides step-by-step instructions to set up and run the application.

---

## ✅ Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL Server installed and running
- [ ] Git (optional, for cloning repository)
- [ ] Text editor or IDE (VS Code, PyCharm, etc.)
- [ ] Administrator access to install packages

**Verify your setup:**

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check MySQL (Windows)
mysql --version

# Check MySQL (Mac/Linux)
mysql --version
```

---

## 📥 Step 1: Download/Clone Project

### Option A: Direct Download
1. Download the project folder
2. Extract to desired location
3. Open terminal/command prompt
4. Navigate to project folder:
   ```bash
   cd D:\projects\crime_record\crime_dashboard
   ```

### Option B: Clone from Repository
```bash
git clone <repository-url>
cd crime_dashboard
```

---

## 🐍 Step 2: Set Up Python Virtual Environment

### Windows

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### macOS / Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

✅ **Verification:** Terminal prompt shows `(venv)` prefix

---

## 📦 Step 3: Install Python Dependencies

Ensure your virtual environment is activated before proceeding.

```bash
# Install all packages from requirements.txt
pip install -r requirements.txt
```

**What gets installed:**
- `streamlit` - Web UI framework
- `pandas` - Data processing
- `mysql-connector-python` - MySQL driver
- `plotly` - Visualizations
- `numpy` - Numerical computing
- `streamlit-option-menu` - Navigation menu

✅ **Verification:**
```bash
pip list
```

Should show all installed packages.

---

## 🗄️ Step 4: MySQL Database Setup

### 4.1 Start MySQL Server

#### Windows
```bash
# If installed as Windows service
net start MySQL80

# Or find MySQL in Services and start it
# Services → Search for "MySQL" → Right-click → Start
```

#### macOS
```bash
mysql.server start

# Or using Homebrew
brew services start mysql
```

#### Linux
```bash
sudo systemctl start mysql

# Or
sudo service mysql start
```

✅ **Verification:**
```bash
# This should connect successfully
mysql -u root

# You should see MySQL prompt: mysql>
# Type 'exit' to quit
```

### 4.2 Update Database Credentials

Edit `db_config.py` in project root:

```python
DB_CONFIG = {
    'host': 'localhost',        # ← Usually 'localhost'
    'user': 'root',             # ← Your MySQL user
    'password': 'your_password', # ← ⚠️ UPDATE YOUR PASSWORD HERE
    'database': 'crime_db'
}
```

**Common MySQL setups:**
- Fresh install: username=`root`, password=`` (empty) or `your_password`
- XAMPP: username=`root`, password=`` (empty)
- WAMP: username=`root`, password=`` (empty)

### 4.3 Create Database and Tables

#### Option A: Using Python (Recommended for beginners)

You can create tables directly from the app (Step 6), or run:

```bash
# Ensure virtual environment is activated
python

# In Python shell:
from modules.db_operations import DatabaseManager
db = DatabaseManager()
db.create_tables()
exit()
```

#### Option B: Using MySQL CLI

```bash
# Open MySQL command line
mysql -u root -p

# Enter your password when prompted
```

Then paste this SQL or run from file:

```sql
-- Copy and paste from setup_database.sql
-- Then press Enter
```

Or run directly:

```bash
# One-liner command
mysql -u root -p < setup_database.sql

# Or if password is empty
mysql -u root < setup_database.sql
```

#### Option C: Using MySQL Workbench

1. Open MySQL Workbench
2. Click "+" to create new connection (if needed)
3. Connect to MySQL server
4. Open `setup_database.sql` file
5. Execute (click lightning bolt icon or Ctrl+Enter)

### 4.4 Verify Database Setup

```bash
# Connect to MySQL
mysql -u root -p

# List databases
SHOW DATABASES;

# Should show: crime_db in the list

# Switch to database
USE crime_db;

# List tables
SHOW TABLES;

# Should show:
# - crimes
# - police_officers

# Check police officers
SELECT COUNT(*) FROM police_officers;

# Check crime records
SELECT COUNT(*) FROM crimes;

# Exit MySQL
exit
```

---

## 🎯 Step 5: Configure Application (Optional)

### Database Configuration

Edit `db_config.py` if you haven't already:

```python
DB_CONFIG = {
    'host': 'localhost',        # MySQL server address
    'user': 'root',             # MySQL username
    'password': 'password',     # MySQL password
    'database': 'crime_db'      # Database name
}
```

### Streamlit Configuration (Optional)

Create file: `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#FF0000"
backgroundColor = "#0E1117"
textColor = "#FAFAFA"
font = "sans serif"

[client]
maxUploadSize = 200

[server]
port = 8501
headless = true
```

---

## 🚀 Step 6: Run the Application

### Activate Virtual Environment (if not already active)

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Start Streamlit Application

```bash
streamlit run app.py
```

### Expected Output

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  ^C to quit
```

✅ **Success:** Browser automatically opens to http://localhost:8501

If browser doesn't open, manually navigate to: `http://localhost:8501`

---

## 📋 Step 7: Initial Application Setup

### First Time Using Application

1. **Page Load Issues?**
   - Refresh browser (Ctrl+R or Cmd+R)
   - Check terminal for errors

2. **Create Database Tables (if not done earlier)**
   - Go to "⚙️ Setup" tab
   - Click "Create Database Tables"
   - Should show success message

3. **Register Police Officer**
   - Go to "🔐 Login" tab
   - Click "📝 Register" tab
   - Fill in registration form:
     ```
     Full Name: Your Name
     Email: your@email.com
     Badge Number: PB001 (unique)
     Username: officer_01 (min 4 chars)
     Password: password (min 6 chars)
     ```
   - Click "Register" button
   - Confirm success message

4. **Login**
   - Go back to "🔐 Login" tab
   - Enter username and password
   - Click "Login"
   - Should redirect to Police Panel

---

## 🧪 Step 8: Test Features

### Police Panel Testing

1. **Add Crime Record**
   - Go to "👮 Police Panel"
   - Select "➕ Add Crime Record"
   - Fill in form:
     - Crime Type: "Theft"
     - City: "Mumbai"
     - Date: Today's date
     - Time: 10:30 AM
     - Gender: "Male"
     - Weapon: "Knife"
   - Click "Add Record"
   - Should show success message with balloon animation

2. **View Records**
   - Select "📋 View All Records"
   - Should see your added record
   - Record shows all fields

3. **Update Record**
   - Select "✏️ Update Record"
   - Choose record from dropdown
   - Modify a field
   - Click "Update Record"
   - Should show success

4. **Delete Record (Optional)**
   - Select "🗑️ Delete Record"
   - Choose record
   - Click "Delete"
   - Confirm deletion

### Dashboard Testing

1. Click "📊 Dashboard" from sidebar
2. Should see:
   - Summary statistics cards
   - Filters on left sidebar
   - Analysis charts in tabs
   - Data table at bottom
   - Emergency contacts

3. Try Filters:
   - Change city filter
   - Change crime type filter
   - Charts should update automatically

---

## ⚠️ Troubleshooting

### Issue: "ModuleNotFoundError"

**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt

# Or install individually
pip install streamlit
```

### Issue: MySQL Connection Error

**Error:** `Connection refused` or `Access denied`

**Solution:**
1. Verify MySQL is running:
   ```bash
   # Windows - Check if running
   tasklist | findstr mysql
   
   # Mac/Linux
   ps aux | grep mysql
   ```

2. Check credentials in `db_config.py`:
   ```python
   # Test connection in Python
   import mysql.connector
   conn = mysql.connector.connect(
       host='localhost',
       user='root',
       password='your_password'
   )
   print("Connected successfully!")
   ```

3. Make sure MySQL server is started

### Issue: "Database crime_db does not exist"

**Error:** `Unknown database 'crime_db'`

**Solution:**
```bash
# Run database setup
mysql -u root -p < setup_database.sql

# Or in Python
python

from modules.db_operations import DatabaseManager
db = DatabaseManager()
db.create_tables()
exit()
```

### Issue: Streamlit "PORT already in use"

**Error:** `ERROR: Address already in use`

**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill process using port 8501
# Windows
netstat -anomal | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8501
kill -9 <PID>
```

### Issue: Virtual Environment Not Activating

**Solution:**
```bash
# Windows - Try PowerShell instead of CMD
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activation
venv\Scripts\activate

# Or use full path
C:\path\to\project\venv\Scripts\activate
```

---

## 🔄 Daily Startup Process

Once everything is set up, use this daily startup process:

```bash
# 1. Navigate to project folder
cd D:/projects/crime_record/crime_dashboard

# 2. Activate virtual environment (Windows)
venv\Scripts\activate
# Or (Mac/Linux)
source venv/bin/activate

# 3. Verify MySQL is running
# Windows: Services → MySQL → Start
# Mac: brew services start mysql
# Linux: sudo systemctl start mysql

# 4. Run application
streamlit run app.py

# 5. Open browser to http://localhost:8501

# 6. When done, stop Streamlit (Ctrl+C)

# 7. Deactivate virtual environment (optional)
deactivate
```

---

## 📚 Useful Commands

```bash
# List installed packages
pip list

# Check Python version
python --version

# Check if MySQL is running
mysql -u root -p -e "SELECT 1"

# View database
USE crime_db;
SELECT * FROM crimes;

# Install specific package
pip install package_name

# Upgrade package
pip install --upgrade package_name

# Requirements from environment
pip freeze > requirements.txt

# Test database connection
python -c "import mysql.connector; conn = mysql.connector.connect(host='localhost', user='root'); print('Connected!')"
```

---

## 🔒 Production Checklist

Before deploying to production:

- [ ] Update database password in `db_config.py`
- [ ] Use environment variables for credentials
- [ ] Hash passwords using bcrypt
- [ ] Set up SSL for database connection
- [ ] Configure Streamlit security settings
- [ ] Set up logging and monitoring
- [ ] Perform security audit
- [ ] Test with production data
- [ ] Set up backups
- [ ] Document deployment process

---

## 📞 Support Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **MySQL Docs:** https://dev.mysql.com/doc
- **Pandas Docs:** https://pandas.pydata.org/docs
- **Plotly Docs:** https://plotly.com/python

---

## ✨ Next Steps After Setup

1. Explore Police Panel features
2. Add multiple crime records
3. View analytics in Dashboard
4. Experiment with filters
5. Review database queries in Analysis tab
6. Customize colors/themes in Streamlit config
7. Deploy to cloud platform (Streamlit Cloud, Heroku, etc.)

---

**Setup Complete! 🎉**

You're now ready to use the Crime Record Management & Analysis System!

**Questions?** Review the README.md for detailed feature information.
