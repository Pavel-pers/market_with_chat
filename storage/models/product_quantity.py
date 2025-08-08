from sqlalchemy import Column, Integer, String
from fastapi.encoders import jsonable_encoder
from libs import database
from uuid import uuid4

class ProductQuantity(database.ProductQuantityBase):
    __tablename__ = 'product_quantity'

    storage_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)

    def __init__(self, storage_id, product_id, quantity):
        self.storage_id = storage_id
        self.product_id = product_id
        self.quantity = quantity

class ProductQuantityResponce:
    def __init__(self, product_quantity):
        self.storage_id = product_quantity.storage_id
        self.product_id = product_quantity.product_id
        self.quantity = product_quantity.quantity

    def toJSON(self):
        return jsonable_encoder(self)
