from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TaskTemplate(BaseModel):
    title: str
    description: str
    completed: bool


class Task(TaskTemplate):
    task_id: UUID


class Department(str, Enum):
    hr: str = "HR"
    legal: str = "Legal"
    sales: str = "Sales"
    finance: str = "Finance"
    marketing: str = "Marketing"


class EmployeeTemplate(BaseModel):
    name: str
    username: str
    email: EmailStr
    department: Department


class Employee(EmployeeTemplate):
    employee_id: UUID
    tasks: list[Task]
    hashed_password: str | None

    def to_dict(self):
        return {
            "employee_id": str(self.employee_id),
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "department": self.department,
            "tasks": [
                {
                    "task_id": str(task.task_id),
                    "title": task.title,
                    "description": task.description,
                    "completed": str(task.completed),
                }
                for task in self.tasks
            ],
            "hashed_password": self.hashed_password,
        }
