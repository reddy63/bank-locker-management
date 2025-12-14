# 🔐 Bank Locker Management System

A secure Flask-based application for managing bank locker allocations with user authentication, dynamic locker assignment, and an intuitive dashboard.

## Features

✨ **User Authentication**
- Secure registration with email validation
- Password hashing using SHA-256
- Session-based login system
- Password confirmation validation

🔒 **Locker Management**
- View available lockers in real-time
- Request locker allocation (automatic assignment)
- Release allocated locker anytime
- Locker details with location and size information

📊 **Dashboard**
- System statistics and occupancy rates
- Personal locker allocation status
- Available locker count
- Real-time occupancy visualization

👤 **User Profile**
- View account information
- Account creation date tracking
- Security features overview
- Account status display

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, Jinja2 Templates
- **Security**: Password hashing, Session management

## Project Structure

```
bank-locker-management/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── templates/
    ├── base.html              # Base template with navigation
    ├── login.html             # User login page
    ├── register.html          # User registration page
    ├── dashboard.html         # Main user dashboard
    ├── request_locker.html    # Locker request interface
    └── profile.html           # User profile page
```

## Installation

### Prerequisites
- Python 3.7 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone the Repository**
```bash
git clone https://github.com/reddy63/bank-locker-management.git
cd bank-locker-management
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Database**

Create a MySQL database using the following SQL:

```sql
CREATE DATABASE IF NOT EXISTS locker_management;
USE locker_management;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Lockers Table
CREATE TABLE IF NOT EXISTS lockers (
    locker_id INT AUTO_INCREMENT PRIMARY KEY,
    locker_number VARCHAR(50) UNIQUE NOT NULL,
    location VARCHAR(100),
    size VARCHAR(20),
    status ENUM('available', 'allocated', 'maintenance') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    UNIQUE KEY unique_user_allocation (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert Sample Lockers
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

-- Create Indexes
CREATE INDEX idx_user_id ON locker_allocations(user_id);
CREATE INDEX idx_locker_status ON lockers(status);
CREATE INDEX idx_username ON users(username);
```

5. **Configure Database Credentials**

Update the database configuration in `app.py`:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'locker_management'
```

6. **Run the Application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Registration
1. Click on "Register" link
2. Fill in username, email, and password
3. Submit the form
4. Login with your credentials

### Request a Locker
1. Go to Dashboard
2. Click "Request a Locker"
3. System automatically assigns an available locker
4. View locker details on dashboard

### Release a Locker
1. Go to Dashboard
2. Click "Release Locker" button
3. Locker becomes available for others

### View Profile
1. Click "Profile" in navigation
2. View your account information
3. See account creation date and security features

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home (redirects to dashboard/login) |
| `/login` | GET, POST | User login |
| `/register` | GET, POST | User registration |
| `/dashboard` | GET | User dashboard |
| `/request_locker` | GET, POST | Request locker |
| `/release_locker` | POST | Release locker |
| `/profile` | GET | User profile |
| `/logout` | GET | Logout |

## Database Schema

### Users Table
- `user_id`: Auto-increment primary key
- `username`: Unique username
- `email`: Unique email address
- `password`: SHA-256 hashed password
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Lockers Table
- `locker_id`: Auto-increment primary key
- `locker_number`: Unique locker identifier
- `location`: Physical location of locker
- `size`: Small, Medium, or Large
- `status`: available, allocated, or maintenance

### Locker Allocations Table
- `allocation_id`: Auto-increment primary key
- `user_id`: Foreign key to users
- `locker_id`: Foreign key to lockers
- `allocated_at`: Allocation timestamp
- `released_at`: Release timestamp (nullable)

## Security Features

🔐 **Password Security**
- SHA-256 hashing
- Minimum 6 characters requirement
- Password confirmation validation

🛡️ **Session Management**
- Flask session-based authentication
- Login required decorator for protected routes
- Session timeout on logout

✅ **Input Validation**
- Email format validation
- Username pattern validation
- SQL injection prevention with parameterized queries

## UI/UX Features

- 🎨 Modern gradient design (purple/blue theme)
- 📱 Responsive layout for mobile and desktop
- ⚡ Smooth animations and transitions
- 🎯 Card-based information display
- 🔔 Flash message notifications
- 📊 Real-time statistics and progress bars

## Future Enhancements

- 📧 Email notifications for locker status
- 👨‍💼 Admin panel for locker management
- 🔧 Locker maintenance tracking
- 📝 User activity logs
- 🔐 Two-factor authentication
- 💳 Payment integration
- 📱 Mobile application
- 🎟️ QR code access system
- 🔔 Push notifications

## Production Deployment

For production environment:

1. Set `debug=False` in app.py
2. Use production WSGI server (Gunicorn, uWSGI)
3. Setup reverse proxy (Nginx, Apache)
4. Configure environment variables
5. Enable HTTPS/SSL certificates
6. Implement logging and monitoring
7. Setup database backups

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### MySQL Connection Error
- Verify MySQL server is running
- Check database credentials in app.py
- Ensure database exists
- Default MySQL port is 3306

### Module Not Found
```bash
pip install -r requirements.txt
```

### 404 Template Errors
- Verify templates directory exists in project root
- Check template names match in app.py
- Ensure Flask can access template files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

**Reddy63**
- GitHub: [@reddy63](https://github.com/reddy63)

## Support

For support, email reddy63@github.com or open an issue in the repository.

---

**Made with ❤️ by Reddy63**