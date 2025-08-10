from libs.database import ClientCartPositionsBase
from sqlalchemy import Column, Integer, String
from fastapi.encoders import jsonable_encoder


class ClientCartPositions(ClientCartPositionsBase):
    __tablename__ = 'client_cart_positions'

    client_id = Column(Integer, primary_key=True)
    storage_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)

    def __init__(self, client_id: int, storage_id: int, product_id: int, quantity: int):
        self.client_id = client_id
        self.storage_id = storage_id
        self.product_id = product_id
        self.quantity = quantity


class ClientCartPositionsResponce:
    def __init__(self, client_id, storage_id, product_id, quantity):
        self.client_id = client_id
        self.storage_id = storage_id
        self.product_id = product_id
        self.quantity = quantity

    def toJSON(self):
        return jsonable_encoder(self)

