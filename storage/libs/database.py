from typing import Annotated, Generator, Any
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from fastapi import Depends
import os


class StorageBase(DeclarativeBase): pass
class ProductQuantityBase(DeclarativeBase): pass

# startup init
SQL_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQL_DATABASE_URL)

def get_session() -> Generator[Session, Any, None]:
    with Session(bind=engine) as session:
        yield session


def init_tables() -> None:
    """
    :param engine: engine of database
    :param Base: Base of classes that should be initialized
    :return:
    """

    try:
        StorageBase.metadata.create_all(engine)
        ProductQuantityBase.metadata.create_all(engine)
    except OperationalError:
        raise Exception('Database connection failed')

