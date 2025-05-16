Implementing an employee management app through FastAPI and an employee's task management CLI interface with Typer.

### Pre-requisites:

- Create a virual environemnt: `python -m venv .venv`
- Activate the virtual environment: `.\.venv\Scripts\Activate.ps1 `
- then install dependencies with: `pip install -r requirements.txt`
- clone `.env.local` as `.env` and generate secret key with `openssl rand -hex 32` Git Bash is recommended for this.

### Launching the WebApp

- `fastapi dev .\src\employee_mgmt\main.py`
- Once the above command has been run, CRUD methods can be tested out [here](http://127.0.0.1:8000/docs).

### The CLI Interface

- The CLI program can be run with: `python -m src.employee_mgmt.cli --help` This will also list the available commands.
- More information about these commands can be viewed using `python -m src.employee_mgmt.cli <command-name> --help`

### Authorization

As of now, the project has very rudimentary authorization implemented.

- An employee must login with their username and password to be able to view a specific employee's detail or to be able to view the list of all employees.
- Only admin can create, update, or delete users.

### To Do

- improve authorization logic
- adapt production ready project structure