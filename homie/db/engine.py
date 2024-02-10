from sqlmodel import SQLModel, create_engine


sqlite_url = "sqlite:///./homie.db"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    from homie.db import models  # noqa
    SQLModel.metadata.create_all(engine)
