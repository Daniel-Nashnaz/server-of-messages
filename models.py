from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    ID: int
    UserID: int
    Subject: str
    Body: str
    SentTime: str = None
    Email: str


class MessageList(BaseModel):
    messages: List[Message]
