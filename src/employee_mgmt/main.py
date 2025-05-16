from uuid import uuid4, UUID
from typing_extensions import Annotated
from datetime import timedelta

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from .schema import EmployeeTemplate, Employee, Token
from .storage import read_from_file, save_to_file
from .auth import (
    oauth2_scheme,
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_employee,
    admin_login,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

app = FastAPI()


@app.get("/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    return {"token": token}


# @app.post("/token/")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     employees: Employee = read_from_file()
#     for employee in employees:
#         if employee.username == form_data.username:
#             hashed_password = get_password_hash(form_data.password)
#             if not hashed_password == employee.hashed_password:
#                 raise HTTPException(
#                     status_code=400, detail="Incorrect username or password"
#                 )
#             return {"access_token": employee.username, "token_type": "bearer"}
#     raise HTTPException(
#         status_code=400, detail="Incorrect username or password"
#     )


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/employees/")
async def view_all_employees(
    token: Annotated[str, Depends(get_current_employee)],
) -> list[Employee]:
    employees: Employee = read_from_file()
    return employees


@app.get("/employees/{employee_id}", response_model=Employee)
async def view_employee(
    token: Annotated[str, Depends(admin_login)], employee_id: UUID
) -> Employee:
    employees: Employee = read_from_file()
    for employee in employees:
        if employee.employee_id == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found.")


@app.post("/employees/")
async def create_employees(
    token: Annotated[str, Depends(admin_login)],
    employee_details: EmployeeTemplate,
) -> Employee:
    # username = employee_details.name.lower().replace(" ", "")
    employees: Employee = read_from_file()
    new_employee = Employee(
        employee_id=uuid4(),
        tasks=[],
        hashed_password=get_password_hash(f"{employee_details.username}@123"),
        # username=username,
        # email=f"{username}@company.com",
        **employee_details.model_dump(),
    )
    employees.append(new_employee)
    save_to_file(employees)
    return new_employee


@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(
    token: Annotated[str, Depends(admin_login)],
    employee_id: UUID,
    updated_details: EmployeeTemplate,
) -> Employee:
    employees: Employee = read_from_file()
    for index, employee in enumerate(employees):
        if employee.employee_id == employee_id:
            employee_tasks = employee.tasks
            employee_hashed_pass = employee.hashed_password
            updated_employee = Employee(
                employee_id=employee_id,
                tasks=employee_tasks,
                hashed_password=employee_hashed_pass,
                **updated_details.model_dump(),
            )
            employees[index] = updated_employee
            save_to_file(employees)
            return updated_employee
    raise HTTPException(status_code=404, detail="Employee not found.")


@app.delete("/employees/{employee_id}", status_code=204)
async def delete_employee(
    token: Annotated[str, Depends(admin_login)], employee_id: UUID
) -> None:
    employees: Employee = read_from_file()
    for index, employee in enumerate(employees):
        if employee.employee_id == employee_id:
            del employees[index]
            save_to_file(employees)
            return
    raise HTTPException(status_code=404, detail="Employee not found.")
