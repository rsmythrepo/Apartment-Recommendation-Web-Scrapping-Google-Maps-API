from sqlmodel import SQLModel, create_engine

from . import models  # noqa

sqlite_url = "sqlite:///./homie.db"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)




