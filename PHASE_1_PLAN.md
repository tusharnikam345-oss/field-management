# FIELD PLUS — Phase 1: Planning, Requirements & Architecture Document

---

## 1. Project Title
**FIELD PLUS** — Smart Field Workforce & Task Management System  
*(A Full-Stack Web Application for Field Operations Management)*

---

## 2. Project Purpose
The purpose of **FIELD PLUS** is to provide small, medium, and educational/field organizations with a centralized, web-based management system to coordinate field workers, schedule and assign tasks, monitor progress updates, maintain work attendance without intrusive tracking, streamline employee leave workflows, and generate operational activity logs and reports.

The project is structured specifically to serve as a comprehensive college academic project, demonstration system, and viva presentation showcase, illustrating industry-standard full-stack web engineering with Python, Flask, and MySQL.

---

## 3. Problem Statement
Many field-based service teams, municipal inspectorships, logistics teams, and field survey groups still rely on disparate communication channels (such as messaging apps, paper checklists, and basic spreadsheets) to manage field tasks. This leads to:
1. **Lack of Central Accountability:** Supervisors cannot reliably determine who is working on which assignment or what stage a task is currently in.
2. **Scattered Communication:** Status updates, delay notes, and completion remarks are lost in private chat threads.
3. **Disorganized Attendance Records:** Maintaining physical registers or unstructured check-in sheets causes record tampering and human error.
4. **Delayed Leave Approvals:** Informal leave requests leave shifts understaffed without real-time schedule awareness.
5. **No Consolidated Reporting:** Generating end-of-month performance reports or audit logs requires tedious manual consolidation.

**FIELD PLUS** directly resolves these problems with a unified, role-governed web application.

---

## 4. Objectives
- **Centralize Task Allocation:** Enable administrators to create, assign, prioritize, and track field tasks from a single dashboard.
- **Provide Field Visibility:** Give workers a clean, mobile-responsive portal to check their assignments, update progress percentages (0–100%), and submit progress notes.
- **Maintain Tamper-Resistant Attendance:** Allow workers to record daily check-in and check-out times with built-in constraints preventing duplicate records per day (without relying on invasive GPS/location tracking).
- **Streamline Leave Processing:** Provide a digital leave application and approval workflow with automated validation rules.
- **Maintain an Operational Audit Trail:** Log system activities and notify stakeholders immediately upon key events (task assigned, status altered, leave decided).
- **Ensure Academic & Architectural Excellence:** Produce clean, modular, maintainable, beginner-friendly code following MVC/Flask blueprint design patterns.

---

## 5. Target Users
1. **System Administrators / Operations Managers:**
   - Field operations coordinators, team leads, or organizational managers who oversee tasks, approve leaves, manage worker rosters, and review organizational reports.
2. **Field Workers / Technicians / Agents:**
   - On-field personnel executing assigned physical or technical tasks, marking their work shifts, reporting progress milestones, and requesting time off.

---

## 6. Admin Responsibilities
- **Authentication & Security:** Register administrative accounts, log in securely, manage profile details, and update passwords.
- **Field Worker Management:** Add new field workers, view worker details, edit worker information, search and filter the worker roster, and deactivate workers when inactive.
- **Task Management:** Create tasks with priorities (Low, Medium, High, Urgent) and deadlines; assign tasks to eligible workers; edit or cancel tasks; inspect granular progress histories.
- **Attendance Oversight:** View company-wide daily and historical attendance logs, filter by worker/date/status, and monitor absenteeism.
- **Leave Decisioning:** Review pending leave applications with start/end dates and justifications; approve or reject requests with administrative remarks.
- **System Monitoring & Reports:** Access statistical dashboard cards, visual charts (status distributions, monthly completions), real-time notifications, and audit activity logs.

---

## 7. Worker Responsibilities
- **Authentication:** Secure login with email and password, profile management, and password updates.
- **Dashboard Review:** Immediate overview of assigned tasks (pending, in progress, completed), today's attendance status, and recent notifications.
- **Task Execution & Reporting:** View assigned task details, update current progress percentage (0–100%), transition task status (e.g., Assigned → In Progress → Completed), and log timestamped progress notes.
- **Attendance Marking:** Check in and check out once per calendar day; add optional work remarks.
- **Leave Application:** Submit leave requests with chosen category, start date, end date, and reason; track approval status and admin notes.
- **Notifications:** Receive alerts when new tasks are assigned, progress is acknowledged, or leaves are reviewed.

---

## 8. Main Modules

```
                       ┌───────────────────────────────┐
                       │          FIELD PLUS           │
                       └──────────────┬────────────────┘
                                      │
        ┌──────────────┬──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼
┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐
│Authentication││Worker Roster ││     Task     ││  Attendance  ││    Leave     │
│   & RBAC     ││  Management ││  Management  ││  Management  ││  Management  │
└──────────────┘└──────────────┘└──────────────┘└──────────────┘└──────────────┘
        │              │              │              │              │
        └──────────────┴──────────────┼──────────────┴──────────────┘
                                      │
                       ┌──────────────┴──────────────┐
                       ▼                             ▼
              ┌──────────────────┐          ┌──────────────────┐
              │  Notifications   │          │ Reports, Logs &  │
              │   & Feedbacks    │          │  REST API Layer  │
              └──────────────────┘          └──────────────────┘
```

1. **Authentication & Authorization Module:** Session-based authentication, role validation (`admin` vs `worker`), Werkzeug password hashing, route protection guards.
2. **Worker Management Module:** Full CRUD operations for field personnel, account status toggling (`active` / `inactive`), duplicate email prevention.
3. **Task Management Module:** Creation, priority handling, worker allocation, status transitions, percentage tracking, and historical progress audit logs.
4. **Attendance Module:** Daily single-entry check-in / check-out tracker with remarks, status calculation (Present, Half Day, Absent, Leave), and zero GPS dependencies.
5. **Leave Management Module:** Worker application submission, date conflict validation, approval/rejection decision pipeline with admin feedback remarks.
6. **Notification & Activity Log Module:** In-app notification dispatcher for milestone events and audit log generation for tracking administrative actions.
7. **Reporting & Dashboard Analytics Module:** Aggregate statistical computations, chart data pipelines, and search/filter queries.
8. **REST API Module:** Standardized JSON endpoints for authentication, worker records, task manipulation, attendance logging, and leave processing.

---

## 9. Functional Requirements
- **FR-01 (Authentication):** Users must authenticate with valid credentials. Passwords must be hashed using strong one-way hashing algorithms (e.g., `werkzeug.security.generate_password_hash`).
- **FR-02 (Role Enforcement):** Unauthorized access to `/admin/*` routes by a worker or `/worker/*` routes by an admin must be intercepted and rejected with HTTP 403 Forbidden.
- **FR-03 (Worker CRUD):** Admins can add workers with unique emails. Admins can edit names, phone numbers, and designations, or deactivate accounts without deleting historical task records.
- **FR-04 (Task Assignment):** Admins can create tasks and bind them to an active worker.
- **FR-05 (Progress Validation):** Task progress inputs must be integers strictly within the range of 0 to 100. When 100% is submitted, the status must automatically suggest or transition to `Completed`.
- **FR-06 (Restricted Task Editing):** Workers must only be able to view and log progress on tasks explicitly assigned to their worker ID.
- **FR-07 (Attendance Uniqueness):** The system must enforce a unique constraint on `(worker_id, attendance_date)`. A worker cannot create multiple attendance entries for the same calendar date.
- **FR-08 (Check-out Constraint):** A worker can only record a check-out time if a check-in time for that day already exists, and the check-out time must be equal to or later than the check-in time.
- **FR-09 (Leave Date Integrity):** When applying for leave, `end_date` must not precede `start_date`.
- **FR-10 (Notification Triggers):** The system must generate notification records whenever:
  - An admin assigns a task to a worker.
  - A worker submits a task progress update.
  - An admin updates a leave request status.
- **FR-11 (Database-Backed Search & Filtering):** Search queries (e.g., worker name, task title, attendance date, leave status) must be executed at the SQL layer with parameterized queries, rather than simple client-side array filters.
- **FR-12 (REST API Standards):** API endpoints must consume and return JSON, validate input bodies, provide meaningful HTTP status codes (200, 201, 400, 401, 403, 404, 500), and include authorization headers or active session verification.

---

## 10. Non-Functional Requirements
- **NFR-01 (Security):** All SQL statements must be parameterized to prevent SQL injection vulnerabilities. Sessions must be cookie-protected. Form inputs must be sanitized.
- **NFR-02 (Performance):** Page queries should execute efficiently through proper database indexing on foreign keys (`worker_id`, `admin_id`, `task_id`) and status fields.
- **NFR-03 (Usability & Accessibility):** Clean typography, intuitive dashboard layouts, clear visual badges for priorities/statuses, and accessible form controls.
- **NFR-04 (Responsiveness):** Fluid responsive layout functional across desktop monitors (1920x1080, 1366x768), tablets, and mobile screen viewports (down to 360px width).
- **NFR-05 (Maintainability):** Modular code structure separating data models, route blueprints, business utilities, and HTML templates.
- **NFR-06 (Reliability & Robustness):** Graceful error handling for missing database records, invalid route IDs, or database connection losses with friendly custom error pages (403, 404, 500).

---

## 11. Technology Stack

| Layer | Technology | Justification & Purpose |
|---|---|---|
| **Frontend Structure** | HTML5 | Semantic structure for web pages, accessibility compliance |
| **Frontend Styling** | CSS3 + Bootstrap 5 | Modern custom styling, CSS grid/flexbox, utility classes, cards, modal components |
| **Icons & Typography** | Font Awesome 6 + Google Fonts (Inter) | Clean iconography and modern typography for a polished UI |
| **Frontend Logic** | Vanilla JavaScript (ES6+) | Form validation, dynamic AJAX progress submissions, interactive modal handling |
| **Charts / Visuals** | Chart.js (CDN) | Lightweight, responsive interactive graphs for task and attendance analytics |
| **Backend Framework** | Python 3.10+ / Flask 3.x | Lightweight, beginner-friendly WSGI framework with full routing and blueprint modularity |
| **Database Connector** | PyMySQL / mysql-connector-python | Pure-Python connector for executing parameterized SQL queries against MySQL |
| **Database Engine** | MySQL 8.x / MariaDB | Industry-standard relational database with ACID guarantees, foreign keys, and indexes |
| **Security Layer** | Werkzeug Security | Secure, salted password hashing (`pbkdf2:sha256` or `scrypt`) |
| **Environment Config** | python-dotenv | Keeps secret keys and database credentials decoupled from source code |

---

## 12. Security Approach
1. **Password Hashing:** Passwords will never be stored in plain text. When a user registers or is created, their password is processed through `generate_password_hash()`. Verification uses `check_password_hash()`.
2. **Session-Based Role Authorization:**
   - Custom Flask view decorators (`@login_required`, `@admin_required`, `@worker_required`) wrap all protected endpoints.
   - User identity and role are kept in server-signed session storage.
3. **SQL Injection Defense:**
   - All database queries will strictly utilize parameterized SQL placeholders (`%s`) via the DB-API cursor.
   - Zero raw string concatenations will be allowed inside SQL queries.
4. **Cross-User Data Isolation:**
   - Worker endpoints verify that requested task or update operations correspond to `session['user_id']` / `worker_id`. A worker cannot tamper with another worker's task or attendance.
5. **CSRF & Form Validation:**
   - Server-side validation checks data types, string lengths, valid enum values, and date ranges before any database transaction commits.

---

## 13. High-Level Architecture

FIELD PLUS follows a clean **Three-Tier Architectural Model**:

```
+-------------------------------------------------------------------------+
|                         PRESENTATION TIER (UI)                          |
|  - HTML5 Templates (Jinja2 Inheritance)                                 |
|  - Custom CSS3 (Tokens, Glassmorphism, Responsive Grid)                 |
|  - JavaScript (Fetch API, Live Validations, UI State Management)        |
+-------------------------------------------------------------------------+
                                    │
                               HTTP │ Requests / Responses
                                    ▼
+-------------------------------------------------------------------------+
|                          APPLICATION TIER (Flask)                       |
|  - Flask Application Factory / App Config                               |
|  - Blueprints / Routes:                                                  |
|      * auth_bp (Login, Logout, Session Guards)                          |
|      * admin_bp (Dashboard, Worker Management, System Oversight)        |
|      * worker_bp (Dashboard, Task Progress, Attendance, Leaves)         |
|      * api_bp (Standardized RESTful Endpoints)                          |
|  - Utilities: Auth Decorators, Validation Helpers, Notification Engine  |
|  - Models / Data Access Layer: Parameterized SQL Query Modules          |
+-------------------------------------------------------------------------+
                                    │
                              DB-API│ Parameterized SQL Connection
                                    ▼
+-------------------------------------------------------------------------+
|                           DATA TIER (MySQL)                             |
|  - Tables: users, admins, workers, tasks, task_updates, attendance,     |
|            leave_requests, notifications, activity_logs                 |
|  - Constraints: Primary Keys, Foreign Keys (ON DELETE CASCADE/RESTRICT),|
|                 Unique Keys, Indexes                                    |
+-------------------------------------------------------------------------+
```

---

## 14. Application Workflow

### 14.1 User Access & Authentication Flow
1. User visits `/` $\rightarrow$ Redirects to a lightweight Field Plus opening screen with animated branding, then loads `/login`.
2. User enters credentials (Email & Password).
3. System verifies account existence, checks account status (`active`), and verifies password hash.
4. System stores `user_id`, `role`, and `full_name` in the session.
5. Redirects to `/admin/dashboard` if role is `admin`, or `/worker/dashboard` if role is `worker`.

### 14.2 Task Lifecycle Flow
```
[Admin Creates Task] ──► Status: "Assigned" / "Pending" (Progress: 0%)
                                 │
                                 ▼
                     [Worker Views Task in Portal]
                                 │
                                 ▼
                     [Worker Starts Work] ──► Status: "In Progress"
                                 │
                                 ▼
                     [Worker Posts Progress Updates (e.g. 25%, 50%, 80%)]
                     - System adds entry to `task_updates`
                     - System notifies Admin
                                 │
                                 ▼
                     [Worker Sets Progress to 100%] ──► Status: "Completed"
                                 │
                                 ▼
                     [Admin Reviews & Verifies in History]
```

### 14.3 Daily Attendance Flow
1. Worker navigates to the Attendance section.
2. If no record exists for today, worker clicks **"Check In"**. The system records `check_in_time`, sets status to `Present`, and records optional remarks.
3. Later in the shift, the worker clicks **"Check Out"**. The system updates `check_out_time`.
4. If total hours fall below the standard threshold, status can reflect `Half Day`.
5. Duplicate check-ins for the same calendar date are rejected by the database unique key.

### 14.4 Leave Request Lifecycle Flow
1. Worker submits a leave application form (Leave Type, Start Date, End Date, Reason).
2. Record is created with status `Pending`. Admin is notified.
3. Admin reviews the request from the Admin Leave Management portal.
4. Admin clicks **"Approve"** or **"Reject"**, adding an administrative remark.
5. Record updates with status and timestamp; a notification is delivered to the worker.

---

## 15. Database Entity Overview
The database is structured in Third Normal Form (3NF) to avoid redundancy and maintain data integrity:

| Entity / Table | Primary Purpose & Key Fields |
|---|---|
| `users` | Base authentication table (`id`, `email`, `password_hash`, `role`, `status`, `created_at`, `updated_at`). |
| `admins` | Profile details for administrative staff linked to `users.id` (`id`, `user_id`, `full_name`, `phone`, `department`). |
| `workers` | Profile details for field staff linked to `users.id` (`id`, `user_id`, `full_name`, `phone`, `designation`, `join_date`). |
| `tasks` | Master task specifications (`id`, `title`, `description`, `assigned_worker_id`, `created_by_admin_id`, `priority`, `start_date`, `due_date`, `status`, `progress_percent`). |
| `task_updates` | Historical audit trail for task progress (`id`, `task_id`, `worker_id`, `progress_percent`, `update_note`, `status_at_update`, `created_at`). |
| `attendance` | Daily shift logs (`id`, `worker_id`, `attendance_date`, `check_in_time`, `check_out_time`, `status`, `remarks`). |
| `leave_requests`| Worker leave applications (`id`, `worker_id`, `leave_type`, `start_date`, `end_date`, `reason`, `status`, `admin_remark`, `reviewed_by_admin_id`). |
| `notifications` | Internal message queue (`id`, `user_id`, `title`, `message`, `link_url`, `is_read`, `created_at`). |
| `activity_logs` | System audit ledger (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `details`, `created_at`). |

---

## 16. API Overview

All API endpoints follow REST conventions, return standard JSON envelopes `{ success: true/false, data: ..., message: ... }`, and require authentication.

### Authentication
- `POST /api/login` — Authenticate and receive session confirmation.

### Workers
- `GET /api/workers` — List all workers (supports query params: `search`, `status`).
- `POST /api/workers` — Create a new worker account (Admin only).
- `GET /api/workers/<id>` — Retrieve worker profile and assigned tasks.
- `PUT /api/workers/<id>` — Update worker details.
- `DELETE /api/workers/<id>` — Deactivate worker account.

### Tasks
- `GET /api/tasks` — List tasks with filters (`priority`, `status`, `worker_id`).
- `POST /api/tasks` — Create and assign a task (Admin only).
- `GET /api/tasks/<id>` — Get single task details with update history.
- `PUT /api/tasks/<id>` — Update task attributes (Admin) or status/progress (Assigned Worker).
- `DELETE /api/tasks/<id>` — Remove or cancel a task (Admin only).

### Attendance
- `GET /api/attendance` — Retrieve attendance history (filtered by worker, date range, status).
- `POST /api/attendance/check-in` — Worker check-in for current date.
- `POST /api/attendance/check-out` — Worker check-out for current date.

### Leaves
- `GET /api/leaves` — List leave requests (Admin sees all; Worker sees own).
- `POST /api/leaves` — Submit new leave request (Worker).
- `PUT /api/leaves/<id>` — Approve/Reject leave with remark (Admin only).

### Notifications
- `GET /api/notifications` — Fetch user's notifications.
- `PUT /api/notifications/<id>/read` — Mark notification as read.

---

## 17. UI/UX Plan
- **Design Philosophy:** Clean, modern, enterprise-grade aesthetic. Subtle glassmorphism, tailored color palettes, rounded borders, clear typographic hierarchy.
- **Color Palette:**
  - Primary / Brand: Deep Indigo (`#2563eb` / `#1d4ed8`)
  - Accent / Vibrant: Bright Cyan (`#06b6d4`)
  - Dark Slate Neutral: `#0f172a` (Sidebar and headers)
  - Background Neutral: Light Gray (`#f8fafc` / `#f1f5f9`)
  - Surface Cards: Pure White (`#ffffff`) with subtle border shadows
  - Status Accents: Success (`#10b981`), Warning (`#f59e0b`), Danger (`#ef4444`), Info (`#3b82f6`)
- **Key UI Components:**
  1. **Opening / Splash Screen:** Elegant centered "FIELD PLUS" logo with subtle pulse/shimmer animation, smoothly fading into the login page.
  2. **Top Navigation & Sidebar:** Collapsible responsive sidebar with active route highlights, user profile badge, and notification bell counter.
  3. **Dashboard Stat Cards:** Micro-hover elevations displaying total counts, pending counts, and progress metrics with distinct icons.
  4. **Dynamic Data Tables:** Clean tabular listings with integrated search bars, filter dropdowns, badges for statuses (`Pending`, `In Progress`, `Completed`), and pagination controls.
  5. **Modals & Drawers:** Clean Bootstrap-powered modals for task assignment, progress updates, and leave approvals without jarring page reloads.

---

## 18. Project Folder Architecture

```
field_plus/
│
├── app.py                     # Application factory & entry point
├── config.py                  # Environment-specific configuration classes
├── requirements.txt           # Python dependency declarations
├── README.md                  # Project overview, setup guide, and documentation
├── PHASE_1_PLAN.md            # Detailed planning, requirements & architecture document
├── .env.example               # Template for environment secrets
├── .gitignore                 # Rules ignoring .env, __pycache__, venv
│
├── database/                  # Database scripts
│   ├── db.py                  # PyMySQL connection pooling & helper execution functions
│   └── field_plus.sql         # Complete MySQL DDL, indexes, and initial seed data
│
├── routes/                    # Modular Flask Blueprints
│   ├── __init__.py
│   ├── auth.py                # Login, logout, session verification
│   ├── admin.py               # Admin dashboard, worker roster, analytics
│   ├── worker.py              # Worker dashboard, assigned tasks, profile
│   ├── tasks.py               # Task CRUD, progress update handlers
│   ├── attendance.py          # Attendance check-in/out & reporting
│   ├── leaves.py              # Leave applications & approval workflows
│   └── api.py                 # RESTful JSON endpoints
│
├── models/                    # Data Access Layer / SQL Query abstractions
│   ├── __init__.py
│   ├── user.py                # User authentication & role queries
│   ├── worker.py              # Worker profile queries & CRUD
│   ├── task.py                # Task queries, filters, and history
│   ├── attendance.py          # Attendance logging and summaries
│   ├── leave.py               # Leave submission and review queries
│   └── notification.py        # Notification creation and retrieval
│
├── templates/                 # Jinja2 HTML Templates
│   ├── base.html              # Core layout (header, sidebar, flash toasts, footer)
│   ├── splash.html            # Opening animated splash screen
│   ├── login.html             # Secure login view
│   │
│   ├── errors/                # Custom HTTP error pages
│   │   ├── 403.html           # Forbidden access page
│   │   ├── 404.html           # Page not found
│   │   └── 500.html           # Server internal error
│   │
│   ├── admin/                 # Administrator views
│   │   ├── dashboard.html     # Statistical cards, visual charts, recent activity
│   │   ├── workers.html       # Worker roster, add/edit modal, search/filter
│   │   ├── worker_details.html# Comprehensive worker profile & task history
│   │   ├── tasks.html         # Task list, creation form, assignment controls
│   │   ├── task_details.html  # Single task view with complete timeline history
│   │   ├── attendance.html    # Company-wide attendance records with date filters
│   │   ├── leaves.html        # Leave approval management & remarks
│   │   ├── reports.html       # Printable / exportable summary reports
│   │   └── profile.html       # Admin profile & password change
│   │
│   └── worker/                # Field Worker views
│       ├── dashboard.html     # Assigned task summary, quick check-in card
│       ├── tasks.html         # Worker task list with progress update modals
│       ├── task_details.html  # Task instructions and progress logging form
│       ├── attendance.html    # Personal attendance calendar & check-in/out
│       ├── leaves.html        # Leave request submission and status tracker
│       ├── profile.html       # Worker personal profile & contact info
│       └── notifications.html # Full notification inbox
│
├── static/                    # Frontend Static Assets
│   ├── css/
│   │   ├── style.css          # Design system, CSS variables, typography, buttons
│   │   ├── dashboard.css      # Sidebar, navbar, stat cards, tables, charts
│   │   └── responsive.css     # Media queries for tablet & mobile views
│   │
│   ├── js/
│   │   ├── main.js            # General utilities, auto-dismissing toasts, sidebar toggle
│   │   ├── dashboard.js       # Chart.js initialization & dynamic stats
│   │   └── validation.js      # Client-side form & progress input checks
│   │
│   └── images/                # Static brand graphics and icons
│       └── field-plus-logo.svg
│
└── utils/                     # Helper modules
    ├── __init__.py
    ├── auth.py                # Custom decorators: @login_required, @admin_required, etc.
    └── helpers.py             # Date formatters, flash message helpers, activity loggers
```

---

## 19. Development Phases Breakdown

| Phase | Title | Primary Deliverable |
|---|---|---|
| **Phase 1** | Project Planning + Requirements + Architecture | `PHASE_1_PLAN.md` & `README.md` (Current Phase) |
| **Phase 2** | Database Design + ER Diagram + SQL Schema | `database/field_plus.sql` with normalized tables, FKs, sample data |
| **Phase 3** | Flask Setup + Configuration | Flask application factory, `config.py`, database connector |
| **Phase 4** | Authentication + Role Management | Passwords, sessions, `@login_required`, `@admin_required`, login/logout routes |
| **Phase 5** | Admin Module | Worker roster CRUD, search/filter, admin profile |
| **Phase 6** | Worker Module | Worker portal, worker dashboard, personal profile view |
| **Phase 7** | Task Management | Task creation, assignment, progress updates (0-100%), status flow |
| **Phase 8** | Attendance Module | Daily check-in/check-out, unique date validation, zero GPS |
| **Phase 9** | Leave Management | Leave applications, admin approval/rejection with remarks |
| **Phase 10** | Notification System | Internal notifications trigger on task/leave updates |
| **Phase 11** | REST API Layer | Full JSON API with proper status codes & validation |
| **Phase 12** | Professional UI/UX & Animations | Opening screen, Chart.js integrations, responsive tweaks |
| **Phase 13** | Testing & Debugging | Comprehensive manual and unit test cases execution |
| **Phase 14** | Complete Documentation | College-ready documentation: DFDs, Use Cases, Sequence, Architecture |
| **Phase 15** | GitHub Setup | `.gitignore`, clean commit structure, deployment guide |

---

## 20. Testing Strategy
- **Unit Testing (Logic & Validation):**
  - Verify password hash generation and verification.
  - Verify progress percentage boundary checks (rejecting $< 0$ or $> 100$).
  - Verify date validation (rejecting `end_date < start_date`).
- **Database Integrity Testing:**
  - Verify duplicate email registration prevention (`UNIQUE KEY`).
  - Verify duplicate daily attendance prevention (`UNIQUE KEY (worker_id, attendance_date)`).
  - Verify cascading rules on foreign key deletion or restriction.
- **Authorization & Security Testing:**
  - Verify that a logged-out user attempting to access `/admin/dashboard` is redirected to `/login`.
  - Verify that a logged-in field worker accessing `/admin/workers` receives an HTTP 403 Forbidden.
  - Verify that Worker A cannot update tasks assigned to Worker B.
- **Cross-Browser & Responsive Testing:**
  - Test responsiveness on desktop (1920x1080), tablet (768x1024), and mobile (375x667).

---

## 21. Future Scope
While strictly excluded from the current academic build to keep dependencies clean, free, and lightweight:
1. **Offline PWA Support:** Service workers for local task caching when field workers enter areas with poor connectivity.
2. **Export to PDF/Excel:** Generating downloadable monthly attendance and task performance sheets using Python libraries like `reportlab` or `openpyxl`.
3. **SMS / Email Alerts:** Integrating free SMTP (e.g., standard Gmail SMTP) to dispatch email alerts when urgent tasks are assigned.
4. **Barcode / Asset Scanning:** Allowing workers to scan equipment QR codes on site using browser camera capabilities without GPS.
