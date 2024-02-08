from sqlmodel import Session

from .engine import engine


def db_session(func):
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            # Perform any necessary database connection setup here
            return func(*args, **kwargs, session=session)
    return wrapper
