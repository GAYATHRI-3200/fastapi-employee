from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    name: str
    role: str
    salary: float

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    salary: Optional[float] = None
