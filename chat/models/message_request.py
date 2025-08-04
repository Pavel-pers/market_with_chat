from pydantic import BaseModel

class MessageRequest(BaseModel):
    message: str
    user_id: int
