import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_URL = os.getenv('DATABASE_URL')
DB_FILE = os.getenv('DATABASE_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_builder.db'))

def is_postgres():
    return DATABASE_URL is not None and (DATABASE_URL.startswith('postgres://') or DATABASE_URL.startswith('postgresql://'))

def get_db_connection():
    if is_postgres():
        import psycopg2
        import psycopg2.extras
        url = DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        conn = psycopg2.connect(url, cursor_factory=psycopg2.extras.DictCursor)
        return conn
    else:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

def execute_query(cursor, query, params=()):
    if is_postgres():
        query = query.replace('?', '%s')
    cursor.execute(query, params)
    return cursor

def insert_and_get_id(cursor, query, params):
    if is_postgres():
        query_with_returning = query + " RETURNING id"
        execute_query(cursor, query_with_returning, params)
        row = cursor.fetchone()
        return row['id'] if row else None
    else:
        execute_query(cursor, query, params)
        return cursor.lastrowid

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if is_postgres():
        execute_query(cursor, '''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        execute_query(cursor, '''
            CREATE TABLE IF NOT EXISTS courses (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(100),
                level VARCHAR(50),
                duration VARCHAR(50),
                modules_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
    else:
        execute_query(cursor, '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute("PRAGMA table_info(users)")
        columns = [col['name'] for col in cursor.fetchall()]
        if 'is_admin' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
        
        execute_query(cursor, '''
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
        
    # Ensure admin accounts exist and have updated passwords in any database instance
    admin_accounts = [
        ('Munim', 'munim@coursecraft.ai', 'Munim124421'),
        ('admin', 'admin@coursecraft.ai', 'Munim124421')
    ]
    for uname, uemail, upass in admin_accounts:
        execute_query(cursor, "SELECT id FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)", (uname, uemail))
        row = cursor.fetchone()
        hashed = generate_password_hash(upass)
        if not row:
            insert_and_get_id(
                cursor,
                "INSERT INTO users (username, email, password_hash, is_admin) VALUES (?, ?, ?, 1)",
                (uname, uemail, hashed)
            )
        else:
            execute_query(
                cursor,
                "UPDATE users SET password_hash = ?, is_admin = 1 WHERE id = ?",
                (hashed, row['id'])
            )
        
    conn.commit()
    conn.close()

def register_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    clean_username = username.strip()
    clean_email = email.strip().lower()
    
    # Check if username or email already exists (case-insensitive)
    execute_query(
        cursor,
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
    execute_query(cursor, "SELECT COUNT(*) as count FROM users")
    row = cursor.fetchone()
    user_count = row['count'] if row else 0
    is_admin = 1 if user_count == 0 else 0
    
    hashed_pw = generate_password_hash(password)
    try:
        user_id = insert_and_get_id(
            cursor,
            "INSERT INTO users (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)",
            (clean_username, clean_email, hashed_pw, is_admin)
        )
        conn.commit()
        conn.close()
        return True, user_id
    except Exception as e:
        conn.close()
        return False, str(e)

def authenticate_user(username_or_email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    clean_input = username_or_email.strip()
    
    execute_query(
        cursor,
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
    execute_query(
        cursor,
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
    execute_query(
        cursor,
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
    execute_query(
        cursor,
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
    execute_query(cursor, "SELECT id, username, email, is_admin, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def save_course(user_id, title, description, category, level, duration, modules_data_json):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    course_id = insert_and_get_id(
        cursor,
        '''
        INSERT INTO courses (user_id, title, description, category, level, duration, modules_data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (user_id, title, description, category, level, duration, modules_data_json)
    )
    
    conn.commit()
    conn.close()
    return course_id

def get_user_courses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    execute_query(cursor, "SELECT * FROM courses WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    courses = cursor.fetchall()
    conn.close()
    return [dict(course) for course in courses]

def get_course_by_id(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    execute_query(cursor, "SELECT * FROM courses WHERE id = ?", (course_id,))
    course = cursor.fetchone()
    conn.close()
    return dict(course) if course else None

def delete_course(course_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    execute_query(cursor, "DELETE FROM courses WHERE id = ? AND user_id = ?", (course_id, user_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

# --- ADMIN PANEL FUNCTIONS ---

def get_admin_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    execute_query(cursor, "SELECT COUNT(*) as total_users FROM users")
    row1 = cursor.fetchone()
    total_users = row1['total_users'] if row1 else 0
    
    execute_query(cursor, "SELECT COUNT(*) as total_courses FROM courses")
    row2 = cursor.fetchone()
    total_courses = row2['total_courses'] if row2 else 0
    
    conn.close()
    return {
        'total_users': total_users,
        'total_courses': total_courses
    }

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    execute_query(cursor, "SELECT id, username, email, is_admin, created_at FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    return [dict(u) for u in users]

def get_all_courses_with_usernames():
    conn = get_db_connection()
    cursor = conn.cursor()
    execute_query(cursor, '''
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
    execute_query(cursor, "SELECT is_admin FROM users WHERE id = ?", (target_user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False
        
    new_status = 0 if user['is_admin'] == 1 else 1
    execute_query(cursor, "UPDATE users SET is_admin = ? WHERE id = ?", (new_status, target_user_id))
    conn.commit()
    conn.close()
    return True

def admin_delete_user(target_user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    execute_query(cursor, "DELETE FROM users WHERE id = ?", (target_user_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def admin_delete_course(target_course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    execute_query(cursor, "DELETE FROM courses WHERE id = ?", (target_course_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
