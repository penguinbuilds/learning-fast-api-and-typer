import os
from dotenv import load_dotenv
from typing_extensions import Annotated
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from .schema import Employee
from .storage import read_from_file
from .schema import TokenData

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_employee(username: str):
    employees: list[Employee] = read_from_file()
    for employee in employees:
        if employee.username == username:
            return employee


def authenticate_user(username: str, password: str):
    employee = get_employee(username)
    if not employee:
        return False
    if not verify_password(password, employee.hashed_password):
        return False
    return employee


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# def fake_decode_token(token: Annotated[str, Depends()], employee_id: UUID):
#     employees: list[Employee] = read_from_file()
#     for employee in employees:
#         if employee.employee_id == employee_id:
#             employee.username = f"{token}+{employee.username}"
#             return employee


async def get_current_employee(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    employee = get_employee(username=token_data.username)
    if employee is None:
        raise credentials_exception
    return employee


async def admin_login(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Admin privileges required.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username != "admin":
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    employee = get_employee(username=token_data.username)
    # if employee is None:
    #     raise credentials_exception
    return employee
