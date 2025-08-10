from sqlalchemy import Column, Integer, String
from fastapi.encoders import jsonable_encoder
from libs import database
from uuid import uuid4


class Product(database.productBase):
    __tablename__ = "products"
    COUNT_OF_BITS_ID = 16

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)

    def __init__(self, product_id, name, price):
        self.id = product_id
        self.name = name
        self.price = price


class ProductResponse:
    def __init__(self, product):
        self.id = product.id
        self.name = product.name
        self.price = product.price

    def toJSON(self):
        return jsonable_encoder(self)


def create_product_object(name: str, price: int) -> Product:
    product_id = int(uuid4()) & ((1 << Product.COUNT_OF_BITS_ID) - 1)
    new_product = Product(product_id, name, price)
    return new_product
