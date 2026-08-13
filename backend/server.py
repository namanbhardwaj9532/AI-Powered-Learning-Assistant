from fastapi import FastAPI, Request
from pydantic import BaseModel
from config.db import collection
from routes.auth import router as auth_router

app=FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def server():
    return {"message":"server running"}

app.include_router(auth_router)