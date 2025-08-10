from pydantic import BaseModel

class ProductQuantityDifference(BaseModel):
    product_id: int
    difference: int
