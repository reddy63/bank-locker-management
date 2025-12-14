# Bank Locker Management System - Setup Guide

## Quick Start Guide

This document provides step-by-step instructions to set up and run the Bank Locker Management System.

## Prerequisites

- **Python**: 3.7 or higher
- **MySQL**: 5.7 or higher
- **pip**: Python package manager
- **Git**: For cloning the repository

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/reddy63/bank-locker-management.git
cd bank-locker-management
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

#### Option A: Using MySQL Command Line

1. Open MySQL Command Prompt/Terminal:
```bash
mysql -u root -p
```

2. Enter your MySQL password

3. Run the following SQL commands:

```sql
-- Create Database
CREATE DATABASE IF NOT EXISTS locker_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE locker_management;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Lockers Table
CREATE TABLE IF NOT EXISTS lockers (
    locker_id INT AUTO_INCREMENT PRIMARY KEY,
    locker_number VARCHAR(50) UNIQUE NOT NULL,
    location VARCHAR(100),
    size VARCHAR(20),
    status ENUM('available', 'allocated', 'maintenance') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_locker_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Locker Allocations Table
CREATE TABLE IF NOT EXISTS locker_allocations (
    allocation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    locker_id INT NOT NULL,
    allocated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    released_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (locker_id) REFERENCES lockers(locker_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_allocation (user_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert Sample Lockers (12 lockers in 4 locations)
INSERT INTO lockers (locker_number, location, size) VALUES
('A-001', 'Floor 1 - Entry Area', 'Small'),
('A-002', 'Floor 1 - Entry Area', 'Small'),
('A-003', 'Floor 1 - Entry Area', 'Medium'),
('B-001', 'Floor 2 - Hallway', 'Small'),
('B-002', 'Floor 2 - Hallway', 'Medium'),
('B-003', 'Floor 2 - Hallway', 'Large'),
('C-001', 'Floor 3 - Near Stairs', 'Small'),
('C-002', 'Floor 3 - Near Stairs', 'Medium'),
('C-003', 'Floor 3 - Near Stairs', 'Large'),
('D-001', 'Floor 4 - West Wing', 'Small'),
('D-002', 'Floor 4 - West Wing', 'Medium'),
('D-003', 'Floor 4 - West Wing', 'Large');

-- Verify table creation
SHOW TABLES;
```

#### Option B: Using MySQL Workbench

1. Open MySQL Workbench
2. Click "New Query Tab"
3. Copy and paste the SQL commands above
4. Click Execute (lightning bolt icon)

### 5. Configure Database Credentials

Edit `app.py` and update the database configuration:

```python
app.config['MYSQL_HOST'] = 'localhost'      # Your MySQL host
app.config['MYSQL_USER'] = 'root'           # Your MySQL username
app.config['MYSQL_PASSWORD'] = ''           # Your MySQL password
app.config['MYSQL_DB'] = 'locker_management'  # Database name
```

### 6. Run the Application

Make sure your virtual environment is activated, then:

```bash
python app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 7. Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

## Creating Test Accounts

### Method 1: Using the Application UI
1. Click "Register" on the login page
2. Fill in the registration form
3. Click "Register"
4. Login with your credentials

### Method 2: Direct Database Insertion

Connect to MySQL and run:

```sql
USE locker_management;

-- Create test users
INSERT INTO users (username, email, password, created_at) VALUES 
('john_doe', 'john@example.com', SHA2('password123', 256), NOW()),
('jane_smith', 'jane@example.com', SHA2('password123', 256), NOW()),
('admin_user', 'admin@example.com', SHA2('admin123', 256), NOW());

-- View created users
SELECT user_id, username, email FROM users;
```

**Test Login Credentials:**
- Username: `john_doe` | Password: `password123`
- Username: `jane_smith` | Password: `password123`
- Username: `admin_user` | Password: `admin123`

## Project Structure

```
bank-locker-management/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── SETUP.md                    # Setup instructions (this file)
├── .gitignore                  # Git ignore file
└── templates/
    ├── base.html              # Base template
    ├── login.html             # Login page
    ├── register.html          # Registration page
    ├── dashboard.html         # User dashboard
    ├── request_locker.html    # Request locker page
    └── profile.html           # User profile page
```

## Verification Checklist

After setup, verify everything is working:

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip list` shows Flask, Flask-MySQLdb, MySQLdb)
- [ ] MySQL database created successfully
- [ ] Database tables created
- [ ] Sample lockers inserted (SELECT COUNT(*) FROM lockers; should return 12)
- [ ] App.py configured with correct MySQL credentials
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000
- [ ] Can register a new account
- [ ] Can login with the new account
- [ ] Can view dashboard
- [ ] Can request a locker

## Troubleshooting

### Issue: MySQL Connection Error

**Error:** `_mysql_exceptions.OperationalError: (2003, "Can't connect to MySQL server")`

**Solution:**
1. Verify MySQL is running
2. Check MySQL credentials in app.py
3. Ensure database name is correct
4. Verify MySQL port (default: 3306)

```bash
# Windows - Check MySQL status
mysql -u root -p -h localhost

# macOS/Linux - Test connection
mysql -u root -p
```

### Issue: ModuleNotFoundError

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Database Not Found

**Error:** `_mysql_exceptions.ProgrammingError: (1049, "Unknown database 'locker_management')")`

**Solution:**
1. Verify database was created
2. Run SQL setup commands again
3. Check for typos in database name

### Issue: Templates Not Found

**Error:** `jinja2.exceptions.TemplateNotFound: login.html`

**Solution:**
1. Verify templates folder exists in project root
2. Check template names are correct
3. Ensure Flask can access the directory

```bash
# Verify structure
ls -la templates/          # macOS/Linux
dir templates             # Windows
```

## Database Connection Testing

Create a file `test_db.py` to test the connection:

```python
from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'locker_management'

mysql = MySQL(app)

try:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT COUNT(*) as count FROM lockers')
    result = cursor.fetchone()
    print(f"✓ Database connection successful!")
    print(f"✓ Total lockers: {result['count']}")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
```

Run it:
```bash
python test_db.py
```

## Default Ports

- **Flask Application:** `http://localhost:5000`
- **MySQL Server:** `localhost:3306`

## Environment Variables (Optional)

For production, use environment variables. Create a `.env` file:

```
FLASK_ENV=production
FLASK_DEBUG=False
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=locker_management
SECRET_KEY=your_secret_key
```

## Next Steps

1. Read the [README.md](README.md) for feature documentation
2. Explore the application UI
3. Test all features (registration, login, locker request, release)
4. Customize the application as needed
5. Deploy to production following best practices

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review error messages carefully
3. Check [README.md](README.md) for more information
4. Open an issue on GitHub

---

**Happy Banking! 🏦 Enjoy your Secure Locker Management System!**
