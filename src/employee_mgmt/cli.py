from uuid import uuid4
from typing_extensions import Annotated

import typer

from .schema import Task, Employee
from .storage import read_from_file, save_to_file

employees: list[Employee] = read_from_file()

app = typer.Typer()
# task_operations = typer.Typer()

# app.add_typer(task_operations, name="task operations")

# current_user: str | None = None


# @app.command()
# def say_Hi() -> None:
#     typer.echo("Hi")


# @app.command()
# def login(
#     username: Annotated[
#         str,
#         typer.Option(
#             default=...,
#             help="Employee's username.",
#             prompt="Enter your username",
#         ),
#     ],
#     password: Annotated[
#         str,
#         typer.Option(
#             default=...,
#             help="Employee's password.",
#             prompt="Enter your password",
#             hide_input=True,
#         ),
#     ],
# ) -> None:
#     for index, employee in enumerate(employees):
#         if employee.username == username:
#             # call add_task() here
#             break

#         else:
#             typer.echo("Invalid username. Exiting...")
#             raise typer.Exit(code=1)


@app.command()
def add_task(
    username: Annotated[
        str,
        typer.Argument(
            help="Name of the user to whom the task must be assigned."
        ),
    ],
    title: Annotated[
        str,
        typer.Option(
            default=...,
            help="Enter title of the task.",
            prompt="Enter task title",
        ),
    ],
    description: Annotated[
        str,
        typer.Option(
            default=" ",
            help="Description for task.",
            prompt="Enter task description",
        ),
    ],
    task_status: Annotated[
        str,
        typer.Option(
            help="Completion state of task.",
            prompt="Has this task been completed? (y/n)",
        ),
    ],
) -> None:
    for employee in employees:
        if employee.username == username:
            completed: bool = False
            if task_status == "y":
                completed = True
            task = Task(
                task_id=uuid4(),
                title=title,
                description=description,
                completed=completed,
            )
            employee.tasks.append(task)
            save_to_file(employees)
            typer.echo("Task added.")
            return

    typer.echo("Invalid username. Exiting...")
    raise typer.Exit(code=1)


@app.command()
def update_task(
    username: Annotated[
        str,
        typer.Argument(
            help="Name of the user to whom the task must be assigned."
        ),
    ],
    task_id: Annotated[
        str,
        typer.Option(
            default=...,
            help="Enter task id of the task.",
            prompt="Enter task id",
        ),
    ],
    description: Annotated[
        str,
        typer.Option(
            help="Description for task.",
            prompt="Enter task description",
        ),
    ],
    task_status: Annotated[
        str,
        typer.Option(
            help="Completion state of task.",
            prompt="Has this task been completed? (y/n)",
        ),
    ],
) -> None:
    for employee in employees:
        if employee.username == username:
            for index, task in enumerate(employee.tasks):
                if str(task.task_id) == task_id:
                    completed: bool = False
                    if task_status == "y":
                        completed = True
                    title = task.title
                    updated_task = Task(
                        task_id=task_id,
                        title=title,
                        description=description,
                        completed=completed,
                    )
                    employee.tasks[index] = updated_task
                    save_to_file(employees)
                    typer.echo("Task Updated")
                    return
            typer.echo("Invalid task id. Exiting...")
            raise typer.Exit(code=1)

    typer.echo("Invalid username. Exiting...")
    raise typer.Exit(code=1)


@app.command()
def delete_task(
    username: Annotated[
        str,
        typer.Argument(help="Name of the user whose task must be deleted."),
    ],
    task_id: Annotated[
        str,
        typer.Option(
            default=...,
            help="Enter task id of the task.",
            prompt="Enter task id",
        ),
    ],
) -> None:
    for employee in employees:
        if employee.username == username:
            for index, task in enumerate(employee.tasks):
                if str(task.task_id) == task_id:
                    del employee.tasks[index]
                    save_to_file(employees)
                    typer.echo("Task Deleted")
                    return
            typer.echo("Invalid task id. Exiting...")
            raise typer.Exit(code=1)

    typer.echo("Invalid username. Exiting...")
    raise typer.Exit(code=1)


@app.command()
def view_tasks(
    username: Annotated[
        str,
        typer.Argument(
            help="username of the employee whose tasks you wanna view."
        ),
    ],
) -> None:
    for employee in employees:
        if employee.username == username:
            for task in employee.tasks:
                typer.echo(
                    f"\nTitle: {task.title}\nTask ID: {task.task_id}\nDescription: {task.description}\nTask Completed: {task.completed}\n"
                )
            return

    typer.echo("Invalid username. Exiting...")
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
