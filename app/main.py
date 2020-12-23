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
    url = 'https://spreadsheets.google.com/feeds/list/1-NcBjMa6QOFHxMEpgtawvOlP8EQiPnCBsGaBU95mOSA/od6/public/values?alt=json&amp;callback=displayContent&_=1608704607798'

    data = requests.get(url).json()

    results = []
    for item in data['feed']['entry']:

        results.append({
            'bank': item['gsx$bank']['$t'],
            'beli': item['gsx$beli']['$t'],
            'jual': item['gsx$jual']['$t'],
        })
    return results