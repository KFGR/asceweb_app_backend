import sys
from fastapi import APIRouter, FastAPI, Response
from sqlalchemy.orm import Session
# from Backend.CONFIG.connection import engine

user = APIRouter()

@user.get("/")
def root():
    return {"message":"API is working"}

