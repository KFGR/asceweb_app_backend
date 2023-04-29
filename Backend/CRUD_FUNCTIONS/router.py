import sys
sys.path.append("../")
from fastapi import APIRouter, FastAPI, Response
from Backend.DATABASE.connection import engine
app = FastAPI()

@app.get("/")
def root():
    return {"message":"API is working"}
