from models import Todo, OutTask, InTask, DATABASE
from utils import connect_pgsql, get_last_record, get_record_by_id
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from sqlalchemy import select, delete, update
from sqlalchemy.sql.expression import func

app = FastAPI(title='TODO tracking app')
# I purposely skipped part 1 (with storing data in local file on server) of the task
# because it's the easier version of whole task, so I decided to implement PostgreSQL data storing right away


@app.put("/tasks", response_model=List[OutTask])
def add_tasks(tasks: List[InTask]):
    """
    :param tasks: List of dictionaries with task(str) and status(bool), where each element is a unique task.
    task_id is automatically adding in table by incrementing from last task_id, so it is not required to input here.

    :return: List of all added tasks with "task_id", "task" and "status" columns.
    """
    session = connect_pgsql(DATABASE)
    new_data = []
    for row in tasks:
        new_row = Todo(task=row.task, status=row.status)
        session.add(new_row)
        session.commit()

        just_added = get_last_record(session)
        new_data.append(just_added)
    session.close()
    return new_data


@app.delete("/tasks/{id_task}", response_model=None)
def delete_task(id_task: int):
    """
    :param id_task: Single int, that is unique identifier of the task, that should be removed.

    :return: null if operation was done successfully
    """
    session = connect_pgsql(DATABASE)

    if not get_record_by_id(session, id_task):
        raise HTTPException(status_code=404, detail='Task not found')

    statement = delete(Todo).where(Todo.task_id == id_task)
    session.execute(statement)
    session.commit()
    session.close()


@app.post("/tasks/{id_task}", response_model=OutTask)
def update_task(id_task: int, new_task: InTask):
    """
    :param id_task: Single int, that is unique identifier of the task, that should be modified.

    :param new_task: Dictionary with task(str) and status(bool) which is a unique task.
    task_id will not change and is not required to input here.

    :return: Modified task with "task_id", "task" and "status" columns
    """
    session = connect_pgsql(DATABASE)

    last_id = session.query(func.max(Todo.task_id)).all()[0][0]
    if id_task > last_id:
        raise HTTPException(status_code=404, detail='Task not found')

    statement = (update(Todo)
                 .where(Todo.task_id == id_task)
                 .values(task_id=id_task, task=new_task.task, status=new_task.status))
    session.execute(statement)
    session.commit()

    just_added = get_record_by_id(session, id_task)
    session.close()
    return just_added


@app.get("/tasks", response_model=List[OutTask])
def get_tasks(id_task: Optional[int | None] = None):
    """
    :param id_task: Optional single int, that is unique identifier of the task. Default is None, which will
    print all tasks in database. If provided, prints only task with given id.

    :return: List of tasks or a single task.
    """
    session = connect_pgsql(DATABASE)

    last_id = session.query(func.max(Todo.task_id)).all()[0][0]
    if id_task and id_task > last_id:
        raise HTTPException(status_code=404, detail='Task not found')

    if id_task:
        statement = select(Todo.task_id, Todo.task, Todo.status).where(Todo.task_id == id_task)
    else:
        statement = select(Todo.task_id, Todo.task, Todo.status)
    selected_tasks = sorted(session.execute(statement).all(), key=lambda x: x[0])
    session.close()
    return selected_tasks


@app.post("/int_to_roman/{number}", response_model=str)
def int_to_roman(number: int):
    vals = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400, 'C': 100, 'XC': 90,
            'L': 50, 'XL': 40, 'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}
    curr = ""
    for val in vals:
        while number - vals[val] >= 0:
            curr += val
            number -= vals[val]
    return curr
