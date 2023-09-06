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
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class UserRegister(User):
    password: str

class Profile(BaseModel):
    username: str
    last_scores: list[Score] | None = None
    best_scores: list[Score] | None = None
    time_created: Optional[datetime] = None
    played_games: int | None = None

    class Config:
        from_attributes = True