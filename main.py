from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from session import create_get_session

from schema import Score as SchemaScore
from schema import User as SchemaUser

from schema import Score
from schema import User

from model import Score as ModelScore
from model import User as ModelUser


app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.post('/register/', response_model=SchemaUser)
async def register(user: SchemaUser, db: Session = Depends(create_get_session)):
    user = ModelUser(
        nick=user.nick,
        password=user.password,
        email=user.email,
        )
    db.add(user)
    db.commit()
    return user

@app.get('/score/')
async def score(db: Session = Depends(create_get_session)):
    score = db.query(Score).all()
    return score


@app.post('/score/', response_model=SchemaScore)
async def score(score: SchemaScore, db: Session = Depends(create_get_session)):
    score = ModelScore(
        type=score.type,
        size=score.size,
        value=score.value,
        time=score.time,
        user_id=score.user_id
        )
    db.add(score)
    db.commit()
    return score


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     games_played: int | None = None
#     disabled: bool | None = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# def fake_decode_token(token):
#     user = get_user('db', token)
#     return user
#
#
# def fake_hash_password(password: str):
#     return "fakehashed" + password
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
# @app.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_dict = "db".get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}
#
#
# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user
#
#
# @app.get("/scores/me/")
# async def read_scores(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {'token': token}

# @app.get("/scores/me/")

# @app.get("scores/{user}/")

# @app.get("leaderboard/{size}/{type}/")

# @app.post("score/")

# @app.get("users/{user}/")
