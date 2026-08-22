import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_builder.db')

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Ensure is_admin column exists for existing DBs
    cursor.execute("PRAGMA table_info(users)")
    columns = [col['name'] for col in cursor.fetchall()]
    if 'is_admin' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
    
    # Create courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            level TEXT,
            duration TEXT,
            modules_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

def register_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    clean_username = username.strip()
    clean_email = email.strip().lower()
    
    # Check if username or email already exists (case-insensitive)
    cursor.execute(
        "SELECT id, username, email FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)",
        (clean_username, clean_email)
    )
    existing = cursor.fetchone()
    if existing:
        conn.close()
        if existing['email'].lower() == clean_email:
            return False, "An account with this email already exists. Please log in using the Log In form."
        else:
            return False, "This username is already taken. Please choose another username or log in."
    
    # Check total users - first registered user becomes admin automatically
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()['count']
    is_admin = 1 if user_count == 0 else 0
    
    hashed_pw = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)",
            (clean_username, clean_email, hashed_pw, is_admin)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except Exception as e:
        conn.close()
        return False, str(e)

def authenticate_user(username_or_email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    clean_input = username_or_email.strip()
    
    cursor.execute(
        "SELECT * FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)",
        (clean_input, clean_input)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None

def get_user_by_username_or_email(username_or_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    clean_input = username_or_email.strip()
    cursor.execute(
        "SELECT id, username, email FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)",
        (clean_input, clean_input)
    )
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def reset_user_password(username_or_email, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    clean_input = username_or_email.strip()
    hashed_pw = generate_password_hash(new_password)
    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)",
        (hashed_pw, clean_input, clean_input)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def make_user_admin(username_or_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    clean_input = username_or_email.strip()
    cursor.execute(
        "UPDATE users SET is_admin = 1 WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)",
        (clean_input, clean_input)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_admin, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def save_course(user_id, title, description, category, level, duration, modules_data_json):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO courses (user_id, title, description, category, level, duration, modules_data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, title, description, category, level, duration, modules_data_json))
    
    conn.commit()
    course_id = cursor.lastrowid
    conn.close()
    return course_id

def get_user_courses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    courses = cursor.fetchall()
    conn.close()
    return [dict(course) for course in courses]

def get_course_by_id(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
    course = cursor.fetchone()
    conn.close()
    return dict(course) if course else None

def delete_course(course_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id = ? AND user_id = ?", (course_id, user_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

# --- ADMIN PANEL FUNCTIONS ---

def get_admin_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total_users FROM users")
    total_users = cursor.fetchone()['total_users']
    
    cursor.execute("SELECT COUNT(*) as total_courses FROM courses")
    total_courses = cursor.fetchone()['total_courses']
    
    conn.close()
    return {
        'total_users': total_users,
        'total_courses': total_courses
    }

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_admin, created_at FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    return [dict(u) for u in users]

def get_all_courses_with_usernames():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT courses.*, users.username as owner_username 
        FROM courses 
        JOIN users ON courses.user_id = users.id 
        ORDER BY courses.created_at DESC
    ''')
    courses = cursor.fetchall()
    conn.close()
    return [dict(c) for c in courses]

def toggle_user_admin_status(target_user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE id = ?", (target_user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False
        
    new_status = 0 if user['is_admin'] == 1 else 1
    cursor.execute("UPDATE users SET is_admin = ? WHERE id = ?", (new_status, target_user_id))
    conn.commit()
    conn.close()
    return True

def admin_delete_user(target_user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (target_user_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def admin_delete_course(target_course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id = ?", (target_course_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
