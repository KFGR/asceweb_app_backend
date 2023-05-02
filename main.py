# from fastapi import FastAPI
# from Backend.CRUD_FUNCTIONS.router import user
# import os

# app = FastAPI()

# app.include_router(user)

# if _name_ == "_main_":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

import os
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import SecretStr

from Backend.TESTS import Test_Admins as ta
from Backend.DATABASE.Administrators_Table import Administrators_Table
from Backend.SCHEMAS import Administrators_Schemas
from Backend.CONFIG.connection import engine, Base, SessionLocal

# chapter_members.Base.metadata.create_all(bind=connection.engine)
Base.metadata.create_all(bind = engine)

app = FastAPI()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/Content/AdminCreate/", response_model=Administrators_Schemas.Administrator_CreateAccount_OUT)
def createAdmin(admin: Administrators_Schemas.Administrator_CreateAccount_IN, db: Session = Depends(get_db)):
    dbAdmin = ta.getAdminbyEmail(db, email=admin.email)
    if dbAdmin:
        raise HTTPException(status_code=400, detail="Email already registered")
    return ta.createAdmin(db=db, admin=admin)

@app.post("/Content/AdminLogin/")
def loginAdmin(admin: Administrators_Schemas.Administrator_LoginAccount_IN, db: Session = Depends(get_db)) -> bool:
    dbAdmin = ta.loginAdmin(db,admin=admin)
    if dbAdmin == False:
        raise HTTPException(status_code=401, detail="Wrong User Name or Password")
    return dbAdmin

@app.get("/Content/Admins/")
def getAdmins(db: Session = Depends(get_db)) -> list[Administrators_Schemas.Administrator_LookAccount_OUT]:
    dbAdmins = ta.getAdmins(db)
    return dbAdmins
