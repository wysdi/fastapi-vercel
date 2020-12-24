from typing import List
import requests
from fastapi import Request, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine

# Because we're providing a sqlite db with data,
# we don't need to recreate the database file on startup.
# This simplifies the serverless example.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://wysdi.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Return a Cache-Control header for all requests.
# The no-cache directive disables caching on the zeit CDN.
# Including this better demonstrates using FastAPI as a
# serverless function.
@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.get("/")
def welcome(name=None):
    if name is not None:
        return f"Welcome to serverless FastAPI, { name }!"

    return "Welcome to serverless FastAPI!"


@app.get('/kurs', response_model=List[schemas.Kurs])
def get_kurs():
    results = crud.parse_kurs()
    return results


@app.get('/kebasa', response_model=List[schemas.Kebasa])
def get_kebasa():
    results = crud.parse_kebasa()
    return results


