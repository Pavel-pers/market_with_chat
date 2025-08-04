from sqlalchemy import Column, Integer, String
from chat.libs.database import ChatBase

class Message(ChatBase):
    __tablename__ = 'messages'

    chat_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    text = Column(String)
    date = Column(String)

    def __repr__(self):
        return f'<Message {self.chat_id} {self.user_id} {self.text} {self.date}>'