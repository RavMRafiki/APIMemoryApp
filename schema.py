from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Score(BaseModel):
    id: Optional[int] = None
    type: str
    size: int
    value: int
    time: int
    time_created: Optional[datetime] = None
    time_updated: Optional[datetime] = None
    user_id: int

    class Config:
        from_attributes = True


class User(BaseModel):
    id: Optional[int] = None
    nick: str
    password : str
    email : Optional[str]
    token : Optional[str]

    class Config:
        from_attributes = True
