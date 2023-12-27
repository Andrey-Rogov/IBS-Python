from models import HOST, USER, PASSWORD, PORT
from models import Todo, Base
from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func


def connect_pgsql(database):
    # Ensure that table exists and connect
    engine_data = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}"
    engine = create_engine(engine_data)
    if not database_exists(f"postgresql://{USER}@{HOST}:{PORT}/{database}"):
        Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return session


def get_last_record(session):
    # To return just added data with id's, make a select query to database using max task_id
    last_id = session.query(func.max(Todo.task_id)).all()[0][0]
    statement = select(Todo.task_id, Todo.task, Todo.status).where(Todo.task_id == last_id)
    just_added = session.execute(statement).all()
    return {col: val for col, val in zip(('task_id', 'task', 'status'), *just_added)}


def get_record_by_id(session, id_t):
    statement = select(Todo.task_id, Todo.task, Todo.status).where(Todo.task_id == id_t)
    record = session.execute(statement).all()
    if record:
        return {col: val for col, val in zip(('task_id', 'task', 'status'), *record)}
    else:
        return None
