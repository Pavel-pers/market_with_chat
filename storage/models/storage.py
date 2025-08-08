from sqlalchemy import Column, Integer, String
from fastapi.encoders import jsonable_encoder
from libs import database
from uuid import uuid4


class Storage(database.StorageBase):
    __tablename__ = 'storages'
    COUNT_OF_BITS_ID = 16

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __init__(self, storage_id: int, name: str):
        self.id = storage_id
        self.name = name


class StorageResponce:
    def __init__(self, storage):
        self.id = storage.id
        self.name = storage.name

    def toJSON(self):
        return jsonable_encoder(self)


def create_storage_object(name: str):
    storage_id = int(uuid4()) & ((1 << Storage.COUNT_OF_BITS_ID) - 1)
    new_storage = Storage(storage_id, name)
    return new_storage