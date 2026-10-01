# FIELD PLUS — Field Work Management System

[![Project Status: Completed](https://img.shields.io/badge/Status-All%20Phases%20Completed-brightgreen.svg)](#)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](#)
[![Framework](https://img.shields.io/badge/Backend-Flask%203.x-lightgrey.svg)](#)
[![Database](https://img.shields.io/badge/Database-MySQL%208.x-orange.svg)](#)
[![Tests: 49 Passed](https://img.shields.io/badge/Tests-49%2F49%20Passed%20(100%25)-success.svg)](#)

---

## 📌 1. Project Introduction

**FIELD PLUS** is an enterprise-grade, full-stack web application designed to streamline field workforce management, task scheduling, progress tracking, shift attendance recording, and employee leave processing. Built with **Python (Flask)**, **MySQL**, and modern **HTML5/CSS3/JavaScript**, the system delivers dedicated, secure portals for both **Administrators** and **Field Workers**.

The application is engineered specifically for college submissions, final year viva presentations, portfolio demonstrations, and production-grade software engineering education.

---

## 🌟 2. Key Features

- **Role-Based Workspaces:** Distinct, secure portals for Administrators and Field Workers with strict route protection guards (`@admin_required`, `@worker_required`).
- **Worker Management:** Administrative roster management (Add, Edit, View, Deactivate) with auto-generated sequential codes (`FW-1001`) and duplicate email prevention.
- **Task Management & Progress Tracking:** Create tasks with priorities (`Low`, `Medium`, `High`, `Urgent`), assign them to workers, and track percentage progress ($0$–$100\%$) with chronological field notes.
- **Auto-Completion Trigger:** Updating task progress to $100\%$ automatically transitions the task status to `Completed`.
- **Zero-GPS Shift Attendance:** Single-entry daily check-in and check-out tracking enforced via a unique relational composite constraint `(worker_id, attendance_date)`, with automated `Half Day` calculation ($< 4$ hours) and worker privacy protection.
- **Leave Request & Auto-Sync Workflow:** Workers can apply for leave; administrators can review, approve, or reject with administrative remarks. Approving leave automatically syncs `Leave` records to the attendance ledger.
- **Internal Notifications & Relative Time:** Event-driven alerts with human-friendly timestamps (`Just now`, `15m ago`, `2h ago`, `Yesterday`) and an unread notification counter.
- **Database-Backed Search & Filtering:** Server-side parameterized filtering for workers, tasks, attendance records, and leave applications.
- **Standardized REST API:** Comprehensive JSON endpoints mounted under `/api/*` with an interactive documentation page at `/api/docs`.
- **Modern UI/UX:** Responsive interface with custom styling, opening splash screen, status badges, progress bars, and Chart.js analytics.

---

## 🛠️ 3. Technology Stack

- **Backend:** Python 3.10+, Flask 3.x
- **Database:** MySQL 8.x / MariaDB (via PyMySQL connector with `DictCursor`)
- **Frontend:** HTML5, CSS3, Bootstrap 5, Font Awesome 6, Chart.js
- **Client Scripting:** Modern JavaScript (ES6+ Fetch API, DOM manipulation)
- **Security:** Werkzeug password hashing (salted scrypt/pbkdf2), session management, role-based route decorators, 100% parameterized SQL queries
- **Testing:** Python standard `unittest` framework (49/49 tests passing)

---

## 🚀 4. Development Status & Roadmap

| Phase | Description | Status |
|---|---|:---:|
| **Phase 1** | **Project Planning + Requirements + Architecture** | **Completed** ✅ |
| **Phase 2** | **Database Design + ER Diagram + SQL Schema** | **Completed** ✅ |
| **Phase 3** | **Flask Setup + Configuration** | **Completed** ✅ |
| **Phase 4** | **Authentication + Role Management** | **Completed** ✅ |
| **Phase 5** | **Admin Module** | **Completed** ✅ |
| **Phase 6** | **Worker Module** | **Completed** ✅ |
| **Phase 7** | **Task Management** | **Completed** ✅ |
| **Phase 8** | **Attendance Module** | **Completed** ✅ |
| **Phase 9** | **Leave Management** | **Completed** ✅ |
| **Phase 10** | **Notification System** | **Completed** ✅ |
| **Phase 11** | **REST API Layer** | **Completed** ✅ |
| **Phase 12** | **Professional UI/UX & Animations** | **Completed** ✅ |
| **Phase 13** | **Testing & Debugging (49/49 Tests Passed)** | **Completed** ✅ |
| **Phase 14** | **Complete Academic Documentation (Report & Viva Prep)** | **Completed** ✅ |
| **Phase 15** | **GitHub Setup & Production Deployment Guide** | **Completed** ✅ |

---

## 📁 5. Complete Documentation Library

All project documentation is organized in the repository:

- 📄 **Academic Project Report & Architecture (SRS, DFD Level 0/1/2, UML, ER):**  
  [docs/PROJECT_REPORT.md](file:///c:/Users/sai/Downloads/feild%20project/docs/PROJECT_REPORT.md)
- 🎓 **Viva Voce Oral Defense Questions & Answers Guide (35 Q&As):**  
  [docs/VIVA_QUESTIONS_AND_ANSWERS.md](file:///c:/Users/sai/Downloads/feild%20project/docs/VIVA_QUESTIONS_AND_ANSWERS.md)
- 🚀 **GitHub Setup & Production Deployment Guide (Cloud, VPS, Local):**  
  [docs/DEPLOYMENT_AND_GITHUB_GUIDE.md](file:///c:/Users/sai/Downloads/feild%20project/docs/DEPLOYMENT_AND_GITHUB_GUIDE.md)
- 🧪 **Automated Testing & QA Verification Report (49 Passed Tests):**  
  [tests/TESTING_REPORT.md](file:///c:/Users/sai/Downloads/feild%20project/tests/TESTING_REPORT.md)
- 🗄️ **Relational Database Design & Schema Specification:**  
  [database/DATABASE_DESIGN.md](file:///c:/Users/sai/Downloads/feild%20project/database/DATABASE_DESIGN.md)
- 📋 **Phase 1 Initial Requirements & Planning Specification:**  
  [PHASE_1_PLAN.md](file:///c:/Users/sai/Downloads/feild%20project/PHASE_1_PLAN.md)

---

## 💻 6. Quick Setup & Execution Guide (Windows / Linux)

### 1. Clone or Open the Workspace
```powershell
cd "c:\Users\sai\Downloads\feild project"
```

### 2. Create and Activate Virtual Environment
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Database Credentials
Copy `.env.example` to `.env` and verify your MySQL connection settings:
```ini
SECRET_KEY=field_plus_super_secret_session_key_2026
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=field_plus
DB_PORT=3306
FLASK_ENV=development
```

### 5. Initialize the Database Schema & Sample Data
```powershell
# Run the database setup script to create tables and seed default users
python setup_db.py
```

### 6. Run the Automated Test Suite
```powershell
python run_tests.py
```
*(Executes all 49 unit and integration tests across 7 test suites)*

### 7. Launch the Application
```powershell
python app.py
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:5000/`**

---

## 🔐 7. Default Demo Accounts

| Role | Email | Password | Access Area |
|---|---|---|---|
| **System Administrator** | `admin@fieldplus.com` | `admin123` | `/admin/dashboard` |
| **Field Worker** | `worker@fieldplus.com` | `worker123` | `/worker/dashboard` |

---

## 👥 8. Project Contributors
- **Project:** FIELD PLUS — Smart Field Workforce & Task Management System
- **Development & Architecture:** Antigravity AI & Project Engineering Team
