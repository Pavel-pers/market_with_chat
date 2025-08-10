from pydantic import BaseModel

class ClientCartPositionsRequest(BaseModel):
    product_id: int
    quantity: int