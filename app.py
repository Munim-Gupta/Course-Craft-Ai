import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify, Response
from functools import wraps
import database as db
import course_generator as generator

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'antigravity-course-generator-secret-key-2026')

# Initialize DB on start
db.init_db()

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.get_user_by_id(user_id)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or g.user.get('is_admin') != 1:
            flash('Page not found.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if g.user:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html', username=username, email=email)
            
        if len(username) < 3:
            flash('Username must be at least 3 characters long.', 'danger')
            return render_template('register.html', username=username, email=email)
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', username=username, email=email)
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html', username=username, email=email)
            
        success, res = db.register_user(username, email, password)
        if success:
            session.clear()
            session['user_id'] = res
            flash(f'Account created successfully! Welcome to CourseCraft AI, {username}.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(res, 'danger')
            return render_template('register.html', username=username, email=email)
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')
        
        if not username_or_email or not password:
            flash('Please fill in both fields.', 'danger')
            return render_template('login.html', username_or_email=username_or_email)
            
        user = db.authenticate_user(username_or_email, password)
        if user:
            session.clear()
            session['user_id'] = user['id']
            flash(f'Welcome back, {user["username"]}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            existing_user = db.get_user_by_username_or_email(username_or_email)
            if existing_user:
                flash('Incorrect password. If you registered previously, please double check your password.', 'danger')
            else:
                flash('No account found with this username or email. Please register below.', 'danger')
            return render_template('login.html', username_or_email=username_or_email)
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    courses = db.get_user_courses(g.user['id'])
    
    # Calculate stats
    total_courses = len(courses)
    total_modules = 0
    total_lessons = 0
    
    for c in courses:
        try:
            m_data = json.loads(c['modules_data'])
            modules_list = m_data.get('modules', [])
            total_modules += len(modules_list)
            for mod in modules_list:
                total_lessons += len(mod.get('lessons', []))
        except Exception:
            pass
            
    stats = {
        'total_courses': total_courses,
        'total_modules': total_modules,
        'total_lessons': total_lessons
    }
    
    return render_template('dashboard.html', courses=courses, stats=stats)

@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate_course():
    if request.method == 'POST':
        topic = request.form.get('topic', '').strip()
        category = request.form.get('category', 'Programming')
        level = request.form.get('level', 'Beginner')
        duration = request.form.get('duration', '4 Weeks')
        num_modules = int(request.form.get('num_modules', 4))
        depth_mode = request.form.get('depth_mode', 'detailed')
        target_audience = request.form.get('target_audience', 'Students & Professionals')
        learning_goals = request.form.get('learning_goals', '').strip()
        
        if not topic:
            flash('Please enter a course topic.', 'danger')
            return render_template('generate.html')
            
        # Generate course data
        course_json = generator.generate_course_curriculum(
            topic=topic,
            category=category,
            level=level,
            duration=duration,
            num_modules=num_modules,
            learning_goals=learning_goals,
            depth_mode=depth_mode,
            target_audience=target_audience
        )
        
        # Save to database
        modules_json_str = json.dumps(course_json)
        course_id = db.save_course(
            user_id=g.user['id'],
            title=course_json['title'],
            description=course_json['description'],
            category=category,
            level=level,
            duration=duration,
            modules_data_json=modules_json_str
        )
        
        flash(f'Course "{course_json["title"]}" generated successfully!', 'success')
        return redirect(url_for('course_detail', course_id=course_id))
        
    return render_template('generate.html')

@app.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course_row = db.get_course_by_id(course_id)
    if not course_row:
        flash('Course not found.', 'danger')
        return redirect(url_for('dashboard'))
        
    # Allow view if owner OR if admin
    if course_row['user_id'] != g.user['id'] and g.user.get('is_admin') != 1:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
        
    try:
        course_data = json.loads(course_row['modules_data'])
    except Exception as e:
        flash('Error loading course data.', 'danger')
        return redirect(url_for('dashboard'))
        
    return render_template('course_detail.html', course=course_row, course_data=course_data)

@app.route('/course/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    success = db.delete_course(course_id, g.user['id'])
    if success:
        flash('Course deleted successfully.', 'success')
    else:
        flash('Failed to delete course.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/api/export/<int:course_id>/<string:export_format>')
@login_required
def export_course(course_id, export_format):
    course_row = db.get_course_by_id(course_id)
    if not course_row or (course_row['user_id'] != g.user['id'] and g.user.get('is_admin') != 1):
        return jsonify({'error': 'Unauthorized'}), 403
        
    course_data = json.loads(course_row['modules_data'])
    
    if export_format == 'json':
        content = json.dumps(course_data, indent=2)
        filename = f"{course_row['title'].replace(' ', '_')}.json"
        mimetype = 'application/json'
    elif export_format == 'markdown':
        # Format markdown
        md = f"# {course_data['title']}\n\n"
        md += f"*{course_data['subtitle']}*\n\n"
        md += f"**Category:** {course_data['category']} | **Level:** {course_data['level']} | **Duration:** {course_data['duration']}\n\n"
        md += f"## Description\n{course_data['description']}\n\n"
        
        md += "## Learning Outcomes\n"
        for outcome in course_data.get('learning_outcomes', []):
            md += f"- {outcome}\n"
        md += "\n"
        
        for mod in course_data.get('modules', []):
            md += f"--- \n\n## Module {mod['module_number']}: {mod['title']}\n"
            md += f"{mod['summary']}\n\n"
            
            for lesson in mod.get('lessons', []):
                md += f"### Lesson {lesson['lesson_number']}: {lesson['title']}\n"
                md += f"{lesson['content']}\n\n"
                if lesson.get('code_example'):
                    code_info = lesson['code_example']
                    md += f"```{code_info.get('language', 'text')}\n{code_info.get('code', '')}\n```\n\n"
                    
        content = md
        filename = f"{course_row['title'].replace(' ', '_')}.md"
        mimetype = 'text/markdown'
    else:
        return jsonify({'error': 'Invalid format'}), 400
        
    return Response(
        content,
        mimetype=mimetype,
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )

# --- SECRET HIDDEN ADMIN ROUTES ---

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    stats = db.get_admin_stats()
    all_users = db.get_all_users()
    all_courses = db.get_all_courses_with_usernames()
    return render_template('admin.html', stats=stats, all_users=all_users, all_courses=all_courses)

@app.route('/admin/user/<int:user_id>/toggle', methods=['POST'])
@login_required
@admin_required
def admin_toggle_user(user_id):
    db.toggle_user_admin_status(user_id)
    flash(f'User #{user_id} admin privileges toggled.', 'info')
    return redirect(url_for('admin_panel'))

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_user_route(user_id):
    if user_id == g.user['id']:
        flash('You cannot delete your own admin account.', 'danger')
    else:
        db.admin_delete_user(user_id)
        flash(f'User #{user_id} and their courses deleted.', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/course/<int:course_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_course_route(course_id):
    db.admin_delete_course(course_id)
    flash(f'Course #{course_id} deleted by admin.', 'success')
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting CourseCraft AI Python Web Application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
