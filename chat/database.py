from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, Session
from fastapi import Depends

from libs import db_functional

class ChatBase(DeclarativeBase): pass

get_session = db_functional.init_engine()
SessionDep = Annotated[Session, Depends(get_session)]
