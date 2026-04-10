import json
import os
from datetime import datetime
from typing import Any, List, Optional, Union

import portalocker
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# --- Configuration ---
DB_FILE = "database.json"

# --- Database Manager (Thread Safe) ---
class FileDB:
    @staticmethod
    def _initialize_db():
        """Creates the database file with default structure if it doesn't exist."""
        if not os.path.exists(DB_FILE):
            initial_data = {
                "employees": [],
                "leaves": [],
                "balances": [],
                "next_employee_id": 1,
                "next_leave_id": 1
            }
            with open(DB_FILE, 'w') as f:
                json.dump(initial_data, f, indent=4)

    @staticmethod
    def read() -> dict:
        FileDB._initialize_db()
        with portalocker.Lock(DB_FILE, 'r', timeout=5) as f:
            return json.load(f)

    @staticmethod
    def write(data: dict):
        with portalocker.Lock(DB_FILE, 'w', timeout=5) as f:
            json.dump(data, f, indent=4)

# --- Schemas ---
class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class EmployeeBase(BaseModel):
    firstName: str
    lastName: str
    email: str
    department: str
    joinDate: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    employeeId: int

class LeaveRequestCreate(BaseModel):
    employeeId: int
    startDate: str  # YYYY-MM-DD
    endDate: str    # YYYY-MM-DD
    leaveType: str  # Annual, Sick, Casual
    reason: str

class LeaveResponse(BaseModel):
    leaveId: int
    employeeId: int
    startDate: str
    endDate: str
    leaveType: str
    totalDays: int
    status: str
    reason: str

# --- FastAPI App ---
app = FastAPI(
    title="Leave Management System",
    description="RESTful API for internal HR leave tracking",
    version="1.0.0"
)

# --- Helper Logic ---
def calculate_days(start_date_str: str, end_date_str: str) -> int:
    fmt = "%Y-%m-%d"
    try:
        start = datetime.strptime(start_date_str, fmt)
        end = datetime.strptime(end_date_str, fmt)
        delta = (end - start).days + 1
        return delta
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

# --- Endpoints ---

@app.get("/api/employees", response_model=ResponseModel)
def get_employees():
    db = FileDB.read()
    return {
        "success": True,
        "message": "Employees retrieved successfully",
        "data": db["employees"]
    }

@app.post("/api/employees", response_model=ResponseModel)
def create_employee(emp: EmployeeCreate):
    db = FileDB.read()
    
    new_id = db["next_employee_id"]
    new_emp = {**emp.dict(), "employeeId": new_id}
    
    db["employees"].append(new_emp)
    db["next_employee_id"] += 1
    
    # Initialize Balances for the current year
    current_year = datetime.now().year
    db["balances"].append({
        "employeeId": new_id,
        "year": current_year,
        "Annual": 20,
        "Sick": 10,
        "Casual": 5
    })
    
    FileDB.write(db)
    return {
        "success": True,
        "message": "Employee created and balances initialized",
        "data": new_emp
    }

@app.post("/api/leaves", response_model=ResponseModel)
def submit_leave(req: LeaveRequestCreate):
    db = FileDB.read()
    
    # Check if employee exists
    emp = next((e for e in db["employees"] if e["employeeId"] == req.employeeId), None)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Calculate duration
    days = calculate_days(req.startDate, req.endDate)
    if days <= 0:
        return {"success": False, "message": "End date must be after start date", "data": None}
    
    # Validate Balance
    year = datetime.strptime(req.startDate, "%Y-%m-%d").year
    balance = next((b for b in db["balances"] if b["employeeId"] == req.employeeId and b["year"] == year), None)
    
    if not balance or balance.get(req.leaveType, 0) < days:
        return {
            "success": False, 
            "message": f"Insufficient {req.leaveType} balance. Requested: {days}", 
            "data": None
        }

    # Record Leave
    new_leave = {
        "leaveId": db["next_leave_id"],
        **req.dict(),
        "totalDays": days,
        "status": "Pending"
    }
    
    db["leaves"].append(new_leave)
    db["next_leave_id"] += 1
    
    # Deduct balance (Logic: Deducting on submission to 'reserve' days)
    balance[req.leaveType] -= days
    
    FileDB.write(db)
    return {
        "success": True,
        "message": "Leave request submitted successfully",
        "data": new_leave
    }

@app.get("/api/leaves/employee/{id}", response_model=ResponseModel)
def get_employee_leaves(id: int):
    db = FileDB.read()
    employee_leaves = [l for l in db["leaves"] if l["employeeId"] == id]
    return {
        "success": True,
        "message": f"Leaves retrieved for employee {id}",
        "data": employee_leaves
    }

@app.get("/api/leavebalances/employee/{id}/year/{year}", response_model=ResponseModel)
def get_balance(id: int, year: int):
    db = FileDB.read()
    balance = next((b for b in db["balances"] if b["employeeId"] == id and b["year"] == year), None)
    
    if not balance:
        return {"success": False, "message": "No balance record found for this year", "data": None}
    
    return {
        "success": True,
        "message": "Balance retrieved",
        "data": balance
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)