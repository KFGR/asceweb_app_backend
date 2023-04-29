import sys
from fastapi import APIRouter, FastAPI, Response
from Backend.DATABASE.connection import engine
user = APIRouter()

@user.get("/")
def root():
    return {"message":"API is working"}
