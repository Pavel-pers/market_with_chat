from typing import Callable, Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import OperationalError
from os import environ

SQL_DATABASE_URL = environ.get('DATABASE_URL')

def init_engine() -> Callable[[], Generator[Session, Any, None]]:
    """
    :param Base: Base of classes that should be initialized
    :return: get_session function
    """
    engine = create_engine(SQL_DATABASE_URL)

    def get_session() -> Generator[Session, Any, None]:
        with Session(bind=engine) as session:
            yield session

    return get_session

def init_tables(engine: create_engine, Base: DeclarativeBase) -> None:
    """
    :param engine: engine of database
    :param Base: Base of classes that should be initialized
    :return:
    """

    try:
        Base.metadata.create_all(engine)
    except OperationalError:
        raise Exception('Database connection failed')