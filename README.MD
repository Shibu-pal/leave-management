# 📅 Leave Management System API

A lightweight, high-performance **RESTful API** built with **FastAPI** for managing employee leave requests, balances, and records. This system uses a thread-safe JSON flat-file database, making it perfect for internal HR tools or proof-of-concept deployments.

---

## 🚀 Features

- **Employee Management:** Create and retrieve employee profiles with unique auto-incrementing IDs.
- **Leave Request Workflow:** Submit requests with automatic duration calculation (includes start and end dates).
- **Balance Tracking:** Real-time tracking of Annual, Sick, and Casual leave quotas per employee per year.
- **Thread-Safe Persistence:** Implements file-level locking using `portalocker` to ensure data integrity during concurrent operations.
- **Automatic Documentation:** Native OpenAPI/Swagger UI support for instant testing.
- **Consistent Response Wrapper:** All API outputs use a standard `{success, message, data}` structure.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Web Server:** Uvicorn
- **Database:** Flat-file JSON (`database.json`)
- **Concurrency:** `portalocker`

---

## 📥 Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/leave-management-api.git](https://github.com/your-username/leave-management-api.git)
    cd leave-management-api
    ```

2.  **Install dependencies:**

    ```bash
    pip install fastapi uvicorn portalocker pydantic
    ```
or
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```
    _The server will start at `http://127.0.0.1:8000`._

---

| Category      | Method | Endpoint                                       | Description                            |
| :------------ | :----- | :--------------------------------------------- | :------------------------------------- |
| **Employees** | `GET`  | `/api/employees`                               | List all registered employees          |
|               | `POST` | `/api/employees`                               | Register a new employee                |
| **Leaves**    | `GET`  | `/api/leaves/employee/{id}`                    | Fetch leave history for an employee    |
|               | `POST` | `/api/leaves`                                  | Submit a new leave request             |
| **Balances**  | `GET`  | `/api/leavebalances/employee/{id}/year/{year}` | Check remaining days for specific year |

---

## 🏗️ Project Structure

```text
.
├── main.py              # Application entry point & API routes
├── database.json        # Flat-file database (auto-generated)
├── requirements.txt     # Dependency list
├── test_main.py         # Automated test suite
├── README.md            # Project documentation
└── requiremrnt (1).md   # Question file
```
