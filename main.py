from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import employees

app = FastAPI(title="Employee Management API")

class Employee(BaseModel):
    id: int
    name: str
    role: str
    salary: float

@app.get("/employees", response_model=List[Employee])
def get_employees():
    return employees

@app.post("/employees", response_model=Employee)
def add_employee(emp: Employee):
    employees.append(emp)
    return emp

@app.put("/employees/{emp_id}", response_model=Employee)
def update_employee(emp_id: int, updated: Employee):
    for i, emp in enumerate(employees):
        if emp.id == emp_id:
            employees[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    for emp in employees:
        if emp.id == emp_id:
            employees.remove(emp)
            return {"message": "Employee deleted"}
    raise HTTPException(status_code=404, detail="Employee not found")
