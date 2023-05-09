import sys
import os
from fastapi import Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session

# from pydantic import SecretStr

from Backend.TESTS import Test_Admins as ta
from Backend.DATABASE.Administrators_Table import Administrators_Table
from Backend.SCHEMAS import Administrators_Schemas
from Backend.CONFIG.connection import engine, Base, SessionLocal
# from Backend.CONFIG.connection import engine

user = APIRouter()

@user.get("/")
def root():
    return {"message":"API is working"}



