# 🎓 CourseCraft AI — Intelligent Python Course Generator Platform

CourseCraft AI is a full-stack Python web application designed to automatically generate, structure, and render comprehensive course syllabi and learning materials for any custom topic. 

It features secure **User Authentication (Login & Registration)**, an **AI Course Generator Studio**, an **Interactive Course Reader**, and **Markdown/JSON Course Exports**.

---

## ✨ Features

- **🔐 User Authentication System**:
  - User Registration & Login with password hashing (`Werkzeug` PBKDF2) and session management.
  - User profile badges and route protection.

- **🤖 AI Course Generator Engine**:
  - Generates tailored course syllabi based on Topic, Category, Skill Level (Beginner, Intermediate, Advanced), Duration, Module Count, and Custom Focus.
  - **Structured Lesson Content**: Multi-section theoretical overviews, real-world industry context, step-by-step implementation guides, and pro-tips.
  - **Production Code Walkthroughs**: Realistic code snippets with type annotations, defensive guard validation, and structured logging.
  - **Hands-On Practical Labs**: Step-by-step terminal exercises for students to practice locally.
  - **Capstone Projects**: Final project deliverables and evaluation rubrics.

- **🎨 Modern Glassmorphism UI & Interactive Live Background**:
  - Dark mode glassmorphism design system.
  - 60fps interactive HTML5 canvas particle background that reacts dynamically to mouse cursor movements with laser-glow connection lines and orb parallax.

- **📄 Export Options**:
  - One-click export to formatted **Markdown (.md)** study guides or **JSON** curriculum data.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask, Werkzeug, SQLite3
- **Production WSGI Server**: Gunicorn
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism), JavaScript (ES6+), FontAwesome
- **Dynamic Formatting**: Marked.js
- **Deployment**: Render.com

---

## 🚀 Quick Start & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Munim-Gupta/Course-Craft-Ai.git
cd Course-Craft-Ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Flask Web Application
```bash
python app.py
```

### 4. Access in Browser
Navigate to **`http://127.0.0.1:5000`** in your web browser.

---

## 🌐 Hosting on Render.com

This repository is pre-configured for 1-click deployment on **Render.com**.

1. Connect your GitHub repository on Render.
2. Render auto-detects `render.yaml` with the following configuration:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
3. Click **Deploy Web Service**.

---

## 📁 Project Structure

```
Course-Craft-Ai/
├── app.py                 # Main Flask application & routes
├── database.py            # SQLite database helper & auth logic
├── course_generator.py    # Course synthesis engine
├── requirements.txt       # Dependencies (Flask, Werkzeug, Gunicorn)
├── render.yaml            # Render.com deployment config
├── .gitignore             # Excluded files (database, cache)
├── static/
│   ├── css/
│   │   └── style.css      # Glassmorphism styling & animations
│   └── js/
│       └── main.js        # Interactive JS & canvas particle background
└── templates/
    ├── base.html          # Main HTML layout & navbar
    ├── login.html         # User Login view
    ├── register.html      # User Registration view
    ├── dashboard.html     # User Dashboard & course library
    ├── generate.html      # Course Generator wizard
    └── course_detail.html # Interactive Course Learning Studio
```

---

## 📄 License
This project is open-source and available under the MIT License.
