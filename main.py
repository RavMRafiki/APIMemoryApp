from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated
from datetime import datetime, timedelta
from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from session import create_get_session

from schema import Profile, Score as SchemaScore, Token, TokenData, UserInDB, UserRegister
from schema import User as SchemaUser

from schema import Score
from schema import User

from model import Score as ModelScore
from model import User as ModelUser

tags_metadata = [
    {
        "name": "User",
        "description": "All operations related to users.",
    },
    {
        "name": "Score",
        "description": "All operations related to scores.",
    },
    {
        "name": "Leaderboard",
        "description": "All operations related to leaderboard.",
    },
    {
        "name": "Profile",
        "description": "All operations related to profiles.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.get("/")
def read_root():
    return {"message": "Server is up and running!"}


# @app.post('/register/', response_model=SchemaUser, tags=["User"])
# async def register(user: UserRegister, db: Session = Depends(create_get_session)):
#     user = ModelUser(
#         username=user.username,
#         password=get_password_hash(user.password),
#         email=user.email,
#     )
#     db.add(user)
#     db.commit()
#     return user

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # to get a string like this run:
# # openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def get_user(db, username: str):
#     user: ModelUser | None = db.query(ModelUser).filter(
#         ModelUser.username == username).first()
#     if user:
#         return UserInDB(
#             id=user.id,
#             username=user.username,
#             email=user.email,
#             disabled=user.disabled,
#             hashed_password=user.password,
#         )


# def authenticate_user(db, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     db: Session = Depends(create_get_session)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token", response_model=Token, tags=["User"])
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     db: Session = Depends(create_get_session)
# ):
#     user = authenticate_user(
#         db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.delete("/user/me/", response_model=User, tags=["User"])
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
#     db: Session = Depends(create_get_session)
# ):
#     parent = db.query(ModelUser).filter(
#         ModelUser.id == current_user.id).first()
#     if parent:
#         childs = db.query(ModelScore).filter(
#             ModelScore.user_id == current_user.id).all()
#         for child in childs:
#             db.delete(child)
#         db.delete(parent)
#         db.commit()
#         return current_user


# @app.get("/user/me/", response_model=User, tags=["User"])
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
#     db: Session = Depends(create_get_session)
# ):
#     return current_user


# # @app.get("/users/me/items/")
# # async def read_own_items(
# #     current_user: Annotated[User, Depends(get_current_active_user)],
# #     db: Session = Depends(create_get_session)
# # ):
# #     return [{"item_id": "Foo", "owner": current_user.username}]


# @app.post('/score/', response_model=SchemaScore, tags=["Score"])
# async def score(score: SchemaScore,
#                 current_user: Annotated[User, Depends(get_current_active_user)],
#                 db: Session = Depends(create_get_session)):
#     score = ModelScore(
#         type=score.type,
#         size=score.size,
#         value=score.value,
#         time=score.time,
#         user_id=current_user.id
#     )
#     db.add(score)
#     db.commit()
#     return score


# @app.get("/score/me/", response_model=List[SchemaScore], tags=["Score"])
# async def score(
#     current_user: Annotated[User, Depends(get_current_active_user)],
#     db: Session = Depends(create_get_session)
# ):
#     scores = db.query(ModelScore).filter(
#         ModelScore.user_id == current_user.id).all()
#     return scores


# @app.get("/score/{user}/", response_model=List[SchemaScore], tags=["Score"])
# async def scores(user: int, db: Session = Depends(create_get_session)):
#     scores = db.query(ModelScore).filter(
#         ModelScore.user_id == user).all()
#     return scores


# @app.get("/leaderboard/{size}/{type}/", response_model=List[SchemaScore], tags=["Leaderboard"])
# async def leaderboard(size: int, type: str,
#                       db: Session = Depends(create_get_session)):
#     scores = db.query(ModelScore).filter(ModelScore.type == type).filter(
#         ModelScore.size == size).order_by(ModelScore.value.desc()).all()
#     return scores


# @app.get("/profile/me/", response_model=Profile, tags=["Profile"])
# async def profile(
#         current_user: Annotated[User, Depends(get_current_active_user)],
#         db: Session = Depends(create_get_session)):
#     user = db.query(ModelUser).filter(ModelUser.id == current_user.id).first()
#     last_scores = db.query(ModelScore).filter(
#         ModelScore.user_id == user.id).order_by(ModelScore.time_created.desc()).limit(10).all()
#     best_scores = db.query(ModelScore).filter(
#         ModelScore.user_id == user.id).order_by(ModelScore.value.desc()).limit(10).all()
#     played_games = db.query(ModelScore).filter(
#         ModelScore.user_id == user.id).count()
#     return Profile(
#         username=user.username,
#         last_scores=last_scores,
#         best_scores=best_scores,
#         time_created=user.time_created,
#         played_games=played_games
#     )


# @app.get("/profile/{user}/", response_model=Profile, tags=["Profile"])
# async def profile(user: int, db: Session = Depends(create_get_session)):
#     user = db.query(ModelUser).filter(ModelUser.id == user).first()
#     last_scores = db.query(ModelScore).filter(
#         ModelScore.user_id == user.id).order_by(ModelScore.time_created.desc()).limit(10).all()
#     best_scores = db.query(ModelScore).filter(
#         ModelScore.user_id == user.id).order_by(ModelScore.value.desc()).limit(10).all()
#     played_games = db.query(ModelScore).filter(
#         ModelScore.user_id == user.id).count()
#     return Profile(
#         username=user.username,
#         last_scores=last_scores,
#         best_scores=best_scores,
#         time_created=user.time_created,
#         played_games=played_games
#     )
