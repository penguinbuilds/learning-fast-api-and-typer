import json
from pathlib import Path

from .schema import Employee


def read_from_file() -> list[Employee]:
    data_file_path = Path("./data/data.json").resolve()
    with open(data_file_path, "r") as file:
        employees_data = json.load(file)
    employees = [Employee(**emp) for emp in employees_data]
    return employees


def save_to_file(employees: list[Employee]) -> None:
    employees_data = [employee.to_dict() for employee in employees]
    data_file_path = Path("./data/data.json").resolve()
    with open(data_file_path, "w") as file:
        json.dump(employees_data, file, indent=2)
