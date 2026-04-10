# Requirement Document: Leave Management System (Python API)

## 1. Executive Summary
The objective is to develop a lightweight, high-performance RESTful API for managing employee leave requests, balances, and records. This system will serve as the backend for an organization's internal HR functions, implemented using a Python-based framework to ensure rapid iteration and clear documentation.

---

## 2. Functional Requirements

### 2.1 Employee Management
* **Create/Update:** Ability to manage core employee details.
* **Retrieve:** Fetch all employees or a specific employee by ID.
* **Data Fields:** `employeeId`, `firstName`, `lastName`, `email`, `department`, `joinDate`.

### 2.2 Leave Request Management
* **Submission:** Employees must be able to submit requests with a `startDate`, `endDate`, `leaveType`, and `reason`.
* **Automatic Logic:** The system must calculate the total number of leave days automatically based on the date range.
* **Status Workflow:** Requests default to **"Pending"** and can be updated to **"Approved"** or **"Rejected"**.
* **Filtering:** Support for retrieving leaves by `status` or by `employeeId`.

### 2.3 Leave Balance Tracking
* **Yearly Quotas:** Track available days per employee, per leave type (Annual, Sick, Casual), per year.
* **Validation:** Provide endpoints to check if an employee has enough balance for a requested period.

---

## 3. Technical Specifications

### 3.1 Tech Stack
* **Language:** Python 3.10+
* **Framework:** **FastAPI** (Recommended for native OpenAPI support) or **Flask**.
* **Database:** A single `database.json` file acting as a flat-file document store.

### 3.2 Data Persistence & Safety
* **Thread Safety:** Must implement file-level locking to handle concurrent read/write operations safely.
* **Auto-Increment:** Logic to generate unique IDs for all new records.
* **Response Wrapper:** All API responses must use a consistent generic wrapper:
    ```json
    {
      "success": true,
      "message": "Detailed action message",
      "data": { ... }
    }
    ```

---

## 4. API Endpoints

| Category | Method | Endpoint |
| :--- | :--- | :--- |
| **Employees** | `GET` | `/api/employees` |
| | `POST` | `/api/employees` |
| **Leaves** | `GET` | `/api/leaves/employee/{id}` |
| | `POST` | `/api/leaves` |
| **Balances** | `GET` | `/api/leavebalances/employee/{id}/year/{year}` |

---

## 5. Documentation & Deliverables

### 5.1 Interactive Documentation
The API must automatically serve an interactive documentation page for testing:
* **FastAPI:** Must provide Swagger UI at `/docs`.
* **Flask:** Must provide an OpenAPI/Swagger page (e.g., via Flasgger).
* **Specification:** The raw OpenAPI JSON must be accessible via `/openapi.json`.

### 5.2 Source Control
The project must be hosted in a **GitHub Repository** containing:
* `main.py` / `app.py`: The application entry point.
* `requirements.txt`: Necessary Python packages (FastAPI/Flask, Uvicorn, etc.).
* `database.json`: Initialized with 5 sample employees and 15 balance records.
* `README.md`: Detailed setup and run instructions.

---

## 6. Future Enhancements
* Migration to a relational database (SQLAlchemy/PostgreSQL).
* JWT-based Authentication and Role-Based Access Control (RBAC).
* Automated email notifications for status changes.