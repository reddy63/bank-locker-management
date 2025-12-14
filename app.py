from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here_change_in_production'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'locker_management'

mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            flash('Please log in first', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('register'))

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address', 'danger')
            return redirect(url_for('register'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s', (username, email))
        account = cursor.fetchone()

        if account:
            flash('Username or email already exists', 'danger')
        else:
            hashed_password = hash_password(password)
            cursor.execute('INSERT INTO users (username, email, password, created_at) VALUES (%s, %s, %s, NOW())',
                         (username, email, hashed_password))
            mysql.connection.commit()
            flash('Registration successful! Please log in', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Please enter username and password', 'danger')
            return redirect(url_for('login'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account and account['password'] == hash_password(password):
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            flash(f'Welcome {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    user_id = session['user_id']
    cursor.execute('SELECT la.*, l.locker_number, l.location, l.size FROM locker_allocations la JOIN lockers l ON la.locker_id = l.locker_id WHERE la.user_id = %s', (user_id,))
    user_locker = cursor.fetchone()

    cursor.execute('SELECT COUNT(*) as total FROM lockers')
    total_lockers = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as allocated FROM lockers WHERE status = "allocated"')
    allocated_lockers = cursor.fetchone()['allocated']

    available_lockers = total_lockers - allocated_lockers

    return render_template('dashboard.html', 
                         user_locker=user_locker, 
                         total_lockers=total_lockers,
                         allocated_lockers=allocated_lockers,
                         available_lockers=available_lockers)

@app.route('/request_locker', methods=['GET', 'POST'])
@login_required
def request_locker():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session['user_id']

    cursor.execute('SELECT * FROM locker_allocations WHERE user_id = %s', (user_id,))
    existing_locker = cursor.fetchone()

    if existing_locker:
        flash('You already have an allocated locker', 'warning')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        cursor.execute('SELECT locker_id FROM lockers WHERE status = "available" LIMIT 1')
        available_locker = cursor.fetchone()

        if available_locker:
            locker_id = available_locker['locker_id']
            
            cursor.execute('UPDATE lockers SET status = "allocated" WHERE locker_id = %s', (locker_id,))
            cursor.execute('INSERT INTO locker_allocations (user_id, locker_id, allocated_at) VALUES (%s, %s, NOW())',
                         (user_id, locker_id))
            mysql.connection.commit()

            flash(f'Locker allocated successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('No lockers available at the moment', 'danger')

    cursor.execute('SELECT COUNT(*) as available FROM lockers WHERE status = "available"')
    available_count = cursor.fetchone()['available']

    return render_template('request_locker.html', available_count=available_count)

@app.route('/release_locker', methods=['POST'])
@login_required
def release_locker():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session['user_id']

    cursor.execute('SELECT locker_id FROM locker_allocations WHERE user_id = %s', (user_id,))
    allocation = cursor.fetchone()

    if allocation:
        locker_id = allocation['locker_id']
        
        cursor.execute('UPDATE lockers SET status = "available" WHERE locker_id = %s', (locker_id,))
        cursor.execute('DELETE FROM locker_allocations WHERE user_id = %s', (user_id,))
        mysql.connection.commit()

        flash(f'Locker released successfully!', 'success')
    else:
        flash('No locker to release', 'warning')

    return redirect(url_for('dashboard'))

@app.route('/profile')
@login_required
def profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
    user = cursor.fetchone()
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
