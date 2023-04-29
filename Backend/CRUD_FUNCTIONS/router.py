from fastapi import APIRouter, FastAPI, Response
from ..DATABASE.connection import engine
# import os
app = FastAPI()

@app.get("/")
def root():
    return {"message":"API is working"}
