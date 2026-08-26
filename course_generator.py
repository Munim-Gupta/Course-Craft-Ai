import json
import random

def generate_course_curriculum(topic, category="General", level="Beginner", duration="4 Weeks", num_modules=4, learning_goals="", depth_mode="detailed", target_audience="Students & Professionals", language="English"):
    """
    Generates an extensive course syllabus with rich HTML-formatted lesson content,
    structured paragraphs, clean bullet points, callout boxes, code walk-throughs,
    and hands-on practical labs.
    """
    topic_clean = topic.strip()
    
    # Custom titles based on difficulty level
    if level == "Beginner":
        title = f"{topic_clean}: Master the Fundamentals"
        subtitle = f"A {duration} {level}-level course tailored for {target_audience} in {language}."
    elif level == "Intermediate":
        title = f"{topic_clean}: Practical Software Engineering"
        subtitle = f"An intensive {duration} building production-grade solutions in {language}."
    elif level == "Advanced":
        title = f"Advanced {topic_clean}: Architecture & Optimization"
        subtitle = f"A high-level {duration} specialization for senior practitioners in {language}."
    elif level == "Expert":
        title = f"Expert {topic_clean}: Deep Mastery & Enterprise Systems"
        subtitle = f"An elite {duration} expert-level mastery track in {language}."
    else:
        title = f"{topic_clean}: Comprehensive Course"
        subtitle = f"A {duration} custom course tailored for {target_audience} in {language}."
        
    description = (
        f"Welcome to <strong>{title}</strong>! This curriculum is crafted specifically for <strong>{target_audience}</strong> in <strong>{language}</strong>. "
        f"You will explore key concepts in <strong>{topic_clean}</strong> through structured lesson modules, "
        f"production code examples, hands-on lab exercises, and a complete capstone project."
    )
    if learning_goals:
        description += f" <br><br><strong>Primary Focus & Goal:</strong> {learning_goals}"
        
    prerequisites = [
        f"Basic computer literacy and a text/code editor installed",
        f"Commitment to completing hands-on exercises and practical labs",
        f"No prior experience with {topic_clean} required" if level == "Beginner" else f"Foundational understanding of {category}"
    ]
    
    learning_outcomes = [
        f"Master the core architecture, syntax, and operational mechanics of {topic_clean}.",
        f"Build functional, error-resilient software applications using industry best practices.",
        f"Write clean, modular code designed specifically for {target_audience}.",
        f"Complete a portfolio-ready Capstone Project in {topic_clean}."
    ]
    
    # Subtopic decomposition
    subtopics = decompose_topic(topic_clean, category, num_modules, learning_goals)
    
    modules = []
    for idx, subtopic in enumerate(subtopics, 1):
        mod_title = f"Module {idx}: {subtopic['name']}"
        mod_summary = subtopic['description']
        
        lessons = []
        for l_idx, lesson_name in enumerate(subtopic['lessons'], 1):
            lesson_title = f"Lesson {idx}.{l_idx}: {lesson_name}"
            
            # Rich HTML content generation with paragraphs, bullet points, and headings
            lesson_content = generate_rich_lesson_html(topic_clean, subtopic['name'], lesson_name, level, idx, l_idx, depth_mode, target_audience)
            code_snippet, code_lang, code_explain = generate_realistic_code_example(topic_clean, subtopic['name'], lesson_name)
            practical_lab = generate_practical_lab(topic_clean, lesson_name)
            
            read_time = "10-15 mins" if depth_mode in ["concise", "quick"] else ("20-25 mins" if depth_mode == "standard" else ("40+ mins" if depth_mode == "masterclass" else "30-35 mins"))
            
            lessons.append({
                "lesson_id": f"m{idx}_l{l_idx}",
                "lesson_number": f"{idx}.{l_idx}",
                "title": lesson_name,
                "full_title": lesson_title,
                "reading_time": read_time,
                "content": lesson_content,
                "code_example": {
                    "language": code_lang,
                    "code": code_snippet,
                    "explanation": code_explain
                },
                "practical_exercise": practical_lab,
                "key_takeaways": [
                    f"Understanding {lesson_name} is critical when designing {topic_clean} systems.",
                    f"Always maintain clean component separation for maintainability.",
                    f"Use defensive validation and logging to catch edge cases early."
                ]
            })
        
        modules.append({
            "module_id": f"m{idx}",
            "module_number": idx,
            "title": subtopic['name'],
            "summary": mod_summary,
            "estimated_hours": f"{random.randint(4, 8)} Hours",
            "lessons": lessons
        })
    
    # Capstone Project
    capstone = generate_capstone_project(topic_clean, category)
    
    course_data = {
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "category": category,
        "level": level,
        "duration": duration,
        "depth_mode": depth_mode,
        "language": language,
        "target_audience": target_audience,
        "prerequisites": prerequisites,
        "learning_outcomes": learning_outcomes,
        "modules": modules,
        "capstone_project": capstone
    }
    
    return course_data

def decompose_topic(topic, category, num_modules, learning_goals=""):
    """Decomposes course topic into rich, realistic modules and lesson titles."""
    t_lower = topic.lower()
    
    if "python" in t_lower:
        base_modules = [
            {
                "name": "Python Fundamentals & Workspace Setup",
                "description": "Mastering Python syntax, dynamic typing, memory references, control flow, and virtual environments.",
                "lessons": [
                    "Setting Up Virtual Environments, Pip & VS Code",
                    "Variables, Memory Models & Primitive Data Types",
                    "Deep Dive into Control Flow: If-Else & Loops"
                ]
            },
            {
                "name": "Data Structures & Functional Programming",
                "description": "In-depth exploration of Python data structures, list comprehensions, lambda functions, and scope.",
                "lessons": [
                    "Mastering Lists, Tuples & Immutability",
                    "High-Performance Dictionaries & Sets",
                    "First-Class Functions, Scope & Lambda Expressions"
                ]
            },
            {
                "name": "Object-Oriented Programming Architecture",
                "description": "Designing scalable software with classes, inheritance, encapsulation, and magic methods.",
                "lessons": [
                    "Classes, Constructors & Instance Attributes",
                    "Inheritance, Polymorphism & Abstract Classes",
                    "Special Magic Methods (__str__, __repr__, __call__)"
                ]
            },
            {
                "name": "File Systems, Exception Handling & JSON",
                "description": "Interacting with the OS, robust exception handling, parsing JSON data, and logging.",
                "lessons": [
                    "File I/O Operations & Context Managers (with clause)",
                    "Custom Exception Hierarchies & Debugging",
                    "JSON Parsing & Structured Data Handling"
                ]
            },
            {
                "name": "Database Integration & REST APIs",
                "description": "Connecting Python to relational databases with SQLite, writing SQL queries, and making HTTP requests.",
                "lessons": [
                    "Relational Database Integration with SQLite",
                    "Consuming REST APIs with Requests & HTTP Headers",
                    "Database ORM Basics & Data Mapping"
                ]
            },
            {
                "name": "Testing, Optimization & Production Delivery",
                "description": "Automated testing with PyTest, performance profiling, and packaging applications.",
                "lessons": [
                    "Automated Testing with PyTest & Assertions",
                    "Profiling Code Performance & Memory Usage",
                    "Packaging Python Modules & Requirements Management"
                ]
            }
        ]
    elif "web" in t_lower or "flask" in t_lower or "django" in t_lower:
        base_modules = [
            {
                "name": "Web Architecture & Protocol Fundamentals",
                "description": "HTTP request-response lifecycle, headers, status codes, and server initialization.",
                "lessons": [
                    "HTTP Lifecycle: Requests, Responses & Headers",
                    "REST Architecture & Endpoint Design Principles",
                    "Environment Configuration & Dev Server Initialization"
                ]
            },
            {
                "name": "Routing, Views & Template Rendering",
                "description": "Creating dynamic web routes, extracting parameters, and rendering server-side templates.",
                "lessons": [
                    "Dynamic URL Routing & Parameter Extraction",
                    "Jinja2 Template Inheritance & Control Flow",
                    "Handling Forms, POST Data & Input Validation"
                ]
            },
            {
                "name": "Database Models, ORM & Authentication",
                "description": "Relational database schemas, data persistence, user registration, and secure sessions.",
                "lessons": [
                    "Database Schema Design & Migration Flow",
                    "User Registration, Password Hashing & Security",
                    "Session Management, Cookies & Route Guards"
                ]
            },
            {
                "name": "REST API Development & AJAX",
                "description": "Building JSON API endpoints, consuming APIs asynchronously, and dynamic UI updates.",
                "lessons": [
                    "Building JSON REST APIs & Serialization",
                    "Asynchronous JavaScript & Fetch API Integration",
                    "Handling File Uploads & Multipart Requests"
                ]
            },
            {
                "name": "Security, Middleware & Error Handling",
                "description": "Preventing OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF) and middleware logic.",
                "lessons": [
                    "Preventing SQL Injection, XSS & CSRF Attacks",
                    "Custom Error Handlers (404, 500) & Logging",
                    "Middleware Pipelines & Access Control"
                ]
            },
            {
                "name": "Production Deployment & Server WSGI",
                "description": "Deploying web applications to production servers using Gunicorn, Nginx, and cloud hosting.",
                "lessons": [
                    "Production WSGI Configuration with Gunicorn",
                    "Managing Environment Variables & Production Secrets",
                    "Cloud Hosting, SSL Certificates & Domain Binding"
                ]
            }
        ]
    elif "machine learning" in t_lower or "data science" in t_lower or "ai" in t_lower:
        base_modules = [
            {
                "name": "Data Manipulation & Mathematical Foundations",
                "description": "Data wrangling, linear algebra operations, array broadcasting with NumPy, and Pandas.",
                "lessons": [
                    "NumPy Vectorized Operations & Arrays",
                    "Pandas DataFrames, Cleaning & Filtering",
                    "Exploratory Data Analysis & Visualization"
                ]
            },
            {
                "name": "Supervised Learning: Regression & Classification",
                "description": "Building predictive models using Linear Regression, Logistic Regression, and Decision Trees.",
                "lessons": [
                    "Linear & Polynomial Regression Modeling",
                    "Classification with Logistic Regression & Decision Trees",
                    "Model Evaluation: Confusion Matrices & ROC-AUC"
                ]
            },
            {
                "name": "Unsupervised Learning & Feature Engineering",
                "description": "Clustering unlabeled data, dimensionality reduction with PCA, and scaling numeric features.",
                "lessons": [
                    "K-Means & Hierarchical Clustering",
                    "Dimensionality Reduction using PCA",
                    "Feature Engineering, Scaling & Encoding"
                ]
            },
            {
                "name": "Deep Learning & Neural Networks",
                "description": "Artificial neural networks, activation functions, backpropagation, and PyTorch/TensorFlow.",
                "lessons": [
                    "Perceptrons & Multi-Layer Neural Networks",
                    "Activation Functions, Loss Functions & Optimizers",
                    "Building Models with PyTorch / TensorFlow"
                ]
            },
            {
                "name": "Model Optimization & Hyperparameter Tuning",
                "description": "Regularization, cross-validation, and automated hyperparameter tuning.",
                "lessons": [
                    "Cross-Validation & Grid Search Optimization",
                    "Regularization Techniques (L1 Lasso, L2 Ridge)",
                    "Handling Imbalanced Datasets & Resampling"
                ]
            },
            {
                "name": "Model Serialization & API Serving",
                "description": "Serializing trained models into disk formats and deploying them as REST API services.",
                "lessons": [
                    "Saving Models with Pickle & ONNX Format",
                    "Building Real-Time Inference APIs",
                    "ML Model Monitoring & Drift Detection"
                ]
            }
        ]
    else:
        # Universal fallback for any custom topic
        base_modules = [
            {
                "name": f"Foundations & Architecture of {topic}",
                "description": f"Core concepts, key terminology, and underlying mechanics of {topic}.",
                "lessons": [
                    f"Introduction to {topic} & Core Terminology",
                    f"Architectural Building Blocks of {topic}",
                    f"Setting Up Your Development Workspace for {topic}"
                ]
            },
            {
                "name": f"Core Operational Principles",
                "description": f"Standard workflows, data management, and fundamental operations of {topic}.",
                "lessons": [
                    f"Data Flow & Execution Models in {topic}",
                    f"Implementation Patterns & Syntax",
                    f"Working with Standard Utilities"
                ]
            },
            {
                "name": f"Intermediate Application & Integration",
                "description": f"Connecting components, handling external inputs, and state management.",
                "lessons": [
                    f"State Management & Component Interaction",
                    f"Integrating External Libraries & Packages",
                    f"Handling Exceptions & Unexpected Inputs"
                ]
            },
            {
                "name": f"Advanced Techniques & System Design",
                "description": f"Architectural best practices, performance optimization, and scalable engineering.",
                "lessons": [
                    f"Advanced Design Patterns in {topic}",
                    f"Performance Profiling & Bottleneck Resolution",
                    f"Security Hardening & Code Refactoring"
                ]
            },
            {
                "name": f"Production Delivery & Real-World Projects",
                "description": f"Building end-to-end solutions, automated testing, and deployment.",
                "lessons": [
                    f"Building End-to-End Solutions for {topic}",
                    f"Automated Testing & Quality Assurance",
                    f"Deployment, Documentation & Maintenance"
                ]
            }
        ]
        
    return base_modules[:min(num_modules, len(base_modules))]

def generate_rich_lesson_html(topic, module_name, lesson_name, level, mod_num, lesson_num, depth_mode="detailed", target_audience="Students"):
    """
    Generates beautifully formatted HTML content with clear section headings (h3/h4),
    structured paragraphs (<p>), bullet point lists (<ul><li>), and pro-tip callout boxes.
    """
    depth_intro = "This lesson provides an <strong>intensive deep dive</strong> into" if depth_mode == "detailed" else ("This lesson covers standard principles of" if depth_mode == "standard" else "This lesson gives a concise overview of")
    
    html = f"""
    <h3>🎯 Lesson Overview</h3>
    <p>
        In <strong>Lesson {mod_num}.{lesson_num}</strong>, {depth_intro} <strong>{lesson_name}</strong>, as part of our module on <em>{module_name}</em>.
        Designed specifically for <strong>{target_audience}</strong>, this material translates theoretical concepts into actionable engineering skills when building applications in <strong>{topic}</strong>.
    </p>

    <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 1.5rem 0;">

    <h3>💡 Real-World Industry Context</h3>
    <p>Why does <strong>{lesson_name}</strong> matter in production software systems?</p>
    <ul>
        <li><strong>Scalability:</strong> High-throughput applications require deterministic execution flows to handle thousands of concurrent operations without performance degradation.</li>
        <li><strong>Maintainability:</strong> Clear separation of concerns ensures that business logic can be updated independently without breaking dependent modules.</li>
        <li><strong>Reliability:</strong> Robust handling of state and memory prevents system crashes, memory leaks, and unexpected downtime during peak traffic.</li>
    </ul>

    <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 1.5rem 0;">

    <h3>🔬 Deep Dive: Theoretical Foundations & Architecture</h3>

    <h4 style="font-size: 1.15rem; color: var(--text-main); margin: 1.25rem 0 0.5rem 0;">1. System Execution Phases</h4>
    <p>When executing operations with {lesson_name}, the underlying system moves through three distinct phases:</p>
    <ol>
        <li><strong>Initialization Phase:</strong> Memory allocations are reserved, environment variables are parsed, and initial state objects are constructed.</li>
        <li><strong>Execution Phase:</strong> Core algorithmic functions transform incoming inputs into validated output payloads.</li>
        <li><strong>Completion & Resource Cleanup:</strong> Open handles, network sockets, or database connection instances are safely returned to pool management.</li>
    </ol>

    <h4 style="font-size: 1.15rem; color: var(--text-main); margin: 1.25rem 0 0.5rem 0;">2. Core Design Principles</h4>
    <ul>
        <li><strong>Component Isolation:</strong> Encapsulating state so that internal mutations do not produce unwanted global side-effects.</li>
        <li><strong>State Determinism:</strong> Ensuring that identical input configurations reliably return identical, testable outcomes.</li>
        <li><strong>Defensive Exception Handling:</strong> Gracefully bubbling up error events to structured log handlers rather than failing silently.</li>
    </ul>

    <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 1.5rem 0;">

    <h3>🛠️ Step-by-Step Implementation Guide</h3>
    <p>To implement <strong>{lesson_name}</strong> in a real-world <strong>{topic}</strong> project, adhere to the following standard workflow:</p>
    <ol>
        <li><strong>Verify Workspace Setup:</strong> Ensure all runtime packages, dependencies, and configuration files are present.</li>
        <li><strong>Define Data Contracts:</strong> Declare explicit type hints or schemas for input payloads and return objects.</li>
        <li><strong>Implement Business Logic:</strong> Write modular functions or classes with single, well-defined responsibilities.</li>
        <li><strong>Add Guard Clauses:</strong> Check for empty or invalid values at the entry point of your functions.</li>
        <li><strong>Execute Automated Tests:</strong> Verify expected outcomes using unit tests and log output monitoring.</li>
    </ol>

    <div style="background: rgba(99, 102, 241, 0.1); border-left: 4px solid var(--primary); border-radius: var(--radius-sm); padding: 1rem 1.25rem; margin-top: 1.5rem;">
        <strong style="color: var(--primary);"><i class="fa-solid fa-lightbulb"></i> Production Pro Tip:</strong>
        Never hardcode secret keys or configuration parameters directly inside your source code. Always consume configuration via environment variables or central configuration settings objects.
    </div>
    """
    return html

def generate_realistic_code_example(topic, module_name, lesson_name):
    """Generates realistic, production-style code snippets."""
    t_lower = topic.lower()
    clean_name = lesson_name.replace(' ', '').replace(':', '').replace('-', '')
    
    if "python" in t_lower or "backend" in t_lower or "data" in t_lower:
        lang = "python"
        code = f"""# ==============================================================================
# Production Code Example: {lesson_name}
# Topic: {topic}
# ==============================================================================

import logging
import time
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class {clean_name}Processor:
    \"\"\"
    Implements {lesson_name} operations adhering to production standards.
    \"\"\"
    def __init__(self, service_name: str = "{topic}"):
        self.service_name = service_name
        self.processed_count = 0
        logging.info(f"Initialized {clean_name}Processor for {{self.service_name}}")

    def validate_input(self, payload: Dict[str, Any]) -> bool:
        if not payload or not isinstance(payload, dict):
            logging.warning("Invalid payload format received.")
            return False
        return True

    def process_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        start_time = time.time()
        
        for idx, item in enumerate(records, 1):
            if not self.validate_input(item):
                continue
                
            processed_item = {{
                "id": item.get("id", idx),
                "status": "COMPLETED",
                "result": f"Processed item {{item.get('name', 'Record')}} via {lesson_name}",
                "timestamp": time.time()
            }}
            results.append(processed_item)
            self.processed_count += 1
            
        elapsed = round(time.time() - start_time, 4)
        logging.info(f"Successfully processed {{len(results)}} records in {{elapsed}}s.")
        return results

if __name__ == "__main__":
    processor = {clean_name}Processor()
    sample_data = [
        {{"id": 101, "name": "User_Session_Data"}},
        {{"id": 102, "name": "Telemetry_Log"}}
    ]
    output = processor.process_records(sample_data)
    print("\\nExecution Summary Output:", output)
"""
        explanation = f"This Python example demonstrates an object-oriented processor for **{lesson_name}** with defensive validation and structured logging."
    elif "web" in t_lower or "javascript" in t_lower:
        lang = "javascript"
        code = f"""// ==============================================================================
// Production Code Example: {lesson_name}
// Topic: {topic}
// ==============================================================================

class {clean_name}Service {{
    constructor(apiBaseUrl = "https://api.example.com/v1") {{
        this.apiBaseUrl = apiBaseUrl;
        this.cache = new Map();
    }}

    async executeTask(params) {{
        console.log(`[${{new Date().toISOString()}}] Starting {lesson_name}...`);
        
        if (!params || typeof params !== 'object') {{
            throw new Error("Invalid parameters provided to {lesson_name}");
        }}

        const result = await new Promise((resolve) => {{
            setTimeout(() => {{
                resolve({{
                    status: 200,
                    message: `Successfully executed {lesson_name}`,
                    data: params
                }});
            }}, 300);
        }});

        this.cache.set(params.id || Date.now(), result);
        return result;
    }}
}}

const service = new {clean_name}Service();
service.executeTask({{ id: "REQ-901", action: "UPDATE_STATE" }})
    .then(res => console.log("Task Result:", res))
    .catch(err => console.error("Task Failed:", err));
"""
        explanation = f"This JavaScript snippet shows async execution for **{lesson_name}** using ES6 class architecture and error bounds."
    else:
        lang = "python"
        code = f"""# Implementation Example for {lesson_name}
def execute_{clean_name.lower()}():
    print(f"Initializing {lesson_name} execution pipeline...")
    config = {{"topic": "{topic}", "lesson": "{lesson_name}", "status": "active"}}
    execution_logs = [f"Phase {{i}} completed" for i in range(1, 4)]
    return {{"config": config, "logs": execution_logs, "success": True}}

if __name__ == "__main__":
    result = execute_{clean_name.lower()}()
    print("Pipeline Output:", result)
"""
        explanation = f"This snippet illustrates step-by-step processing for **{lesson_name}**."
        
    return code, lang, explanation

def generate_practical_lab(topic, lesson_name):
    """Generates a practical hands-on lab exercise."""
    return {
        "title": f"Hands-On Lab: Practice {lesson_name}",
        "instructions": [
            f"1. Open your code editor and create a new file named `lab_{lesson_name.lower().replace(' ', '_').replace(':', '')}.py`.",
            f"2. Implement a function/class that accepts input data for {lesson_name} and enforces validation.",
            "3. Test with at least two test cases: one valid input and one invalid input.",
            "4. Verify output logs in your terminal."
        ],
        "expected_output": f"The script outputs a success log for valid data and a warning message for invalid data."
    }

def generate_capstone_project(topic, category):
    """Generates capstone project requirements."""
    return {
        "title": f"Capstone Project: End-to-End {topic} System",
        "description": f"Design, construct, and document a complete, production-ready application for {topic}.",
        "deliverables": [
            f"Functional source code repository for {topic}",
            "Comprehensive `README.md` documentation with setup instructions",
            "Included test suite verifying core business logic"
        ],
        "evaluation_criteria": [
            "Functional Completeness & Requirement Fulfillment (40%)",
            "Code Quality, Modular Architecture & Documentation (30%)",
            "Error Handling & Edge Case Resilience (30%)"
        ]
    }
