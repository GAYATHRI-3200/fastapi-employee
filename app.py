from fastapi import FastAPI, HTTPException
from database import create_tables, get_db
from models import Employee, EmployeeUpdate

app = FastAPI()

@app.on_event("startup")
def startup():
    create_tables()



@app.post("/employees/")
def create_employee(emp: Employee):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)",
                (emp.name, emp.role, emp.salary))
    conn.commit()
    emp_id = cur.lastrowid
    conn.close()
    return {"id": emp_id, **emp.dict()}



@app.get("/employees/")
def get_employees():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp: Employee):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE employees SET name=?, role=?, salary=? WHERE id=?",
                (emp.name, emp.role, emp.salary, emp_id))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    conn.close()
    return {"id": emp_id, **emp.dict()}


@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    conn.close()
    return {"message": "Employee deleted"}



@app.patch("/employees/{emp_id}")
def patch_employee(emp_id: int, emp: EmployeeUpdate):
    conn = get_db()
    cur = conn.cursor()

    # Fetch existing employee
    cur.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
    existing = cur.fetchone()

    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Employee not found")

    # Prepare updated values
    updated_name = emp.name if emp.name is not None else existing["name"]
    updated_role = emp.role if emp.role is not None else existing["role"]
    updated_salary = emp.salary if emp.salary is not None else existing["salary"]

    # Update only the changed fields
    cur.execute(
        """
        UPDATE employees
        SET name=?, role=?, salary=?
        WHERE id=?
        """,
        (updated_name, updated_role, updated_salary, emp_id)
    )

    conn.commit()
    conn.close()

    return {
        "id": emp_id,
        "name": updated_name,
        "role": updated_role,
        "salary": updated_salary
    }
