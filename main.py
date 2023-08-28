import contextlib
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

app = FastAPI()
client = MongoClient('mongodb://localhost:27017/')
db = client['MemoryApp']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@app.get("/scores/me/")
async def read_scores(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}

# @app.get("/scores/me/")

# @app.get("scores/{user}/")

# @app.get("leaderboard/{size}/{type}/")

# @app.post("score/")

# @app.get("user/{user}/")
