from pydantic import BaseModel

class ProductChangeRequest(BaseModel):
    new_name: str | None
    new_price: int | None