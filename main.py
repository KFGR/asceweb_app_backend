# from fastapi import FastAPI
# from Backend.CRUD_FUNCTIONS.router import user
# import os

# app = FastAPI()

# app.include_router(user)

# if _name_ == "_main_":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

import traceback
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Backend.TESTS import Test_Admins as ta
from Backend.TESTS import SignUp_Test
from Backend.SCHEMAS import Administrators_Schemas, SignUp_Schemas
from Backend.CONFIG.connection import engine, Base, SessionLocal
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from pydantic import ValidationError
# chapter_members.Base.metadata.create_all(bind=connection.engine)
Base.metadata.create_all(bind = engine)

app = FastAPI()
# user= APIRouter()
#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik1hZ25vbGlhMTIiLCJleHBfZGF0ZSI6MTY4MzU5ODE0NS40NzY0LCJsZXZlbCI6Ik1BIn0.xlqHr8lIqunzYWR_O_fK86vrTvG9MqD50pBdYLVSEsM
@app.get("/ASCEPUPR/ADMIN/GET_ADMINS/", response_model=Administrators_Schemas.Output_return)
def getAdmins(masterAdminToken: str, db: Session = Depends(get_db)):
    try:
        dbAdmins = ta.getAdmins(db,admin=Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        return {'status_code':200, 'body':dbAdmins}
    except Exception as e:
        return {'status_code': 404, 'body':"Invalid {}".format(str(e).split()[1])}

@app.post("/ASCEPUPR/ADMIN/CREATE_ACCOUNT/", response_model=Administrators_Schemas.Output_return)
def createAdmin(userName:str, passwd:str, name:str, email:str, phone:str, adminLevel:str,masterAdminToken:str, db: Session = Depends(get_db)):
    try:
        admin = Administrators_Schemas.Administrator_CreateAccount_INPUTS(userName=userName, passwd=passwd,name=name,email=email,phone=phone,adminLevel=adminLevel, masterAdminToken=masterAdminToken)
        dbAdmin = ta.getAdminbyEmail(db, email=admin.email)
        if dbAdmin:
            raise HTTPException(status_code=409, detail="Email already registered")
        dbAdmin = ta.getAdminbyUserName(db, username=admin.userName)
        if dbAdmin:
            raise HTTPException(status_code=409, detail="User Name already registered")
        if ta.createAdmin(db=db, admin=admin):
            return {'status_code':201, 'body':"User created"}
        else:
            raise Exception
    except (ValidationError, ValueError,HTTPException,IntegrityError, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        elif type(e) == IntegrityError: return {"status_code":404, 'body': "duplicate entry"}
        else: return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}
    # except Exception as e:
    #     return {'response': 500, 'message': repr(e)}    # I left this since this can help us, still. It can be deleted later on.

@app.post("/ASCEPUPR/ADMIN/CREATE_MASTER_ADMIN/", response_model=Administrators_Schemas.Output_return)
def createAdmin(userName:str, passwd:str, name:str, email:str, phone: str, db: Session = Depends(get_db)):
    """Verificar si despues el token tiene que ser obligatorio"""
    '''
        Testing purposes or failsafe
    '''
    try:
        admin = Administrators_Schemas.Administrator_CreateAccount_INPUTS(userName=userName, passwd=passwd,name=name,email=email,adminLevel="MA", masterAdminToken="0", phone=phone)
        dbAdmin = ta.getAdminbyEmail(db, email=admin.email)
        if dbAdmin:
            raise HTTPException(status_code=409, detail="Email already registered")
        dbAdmin = ta.getAdminbyUserName(db, username=admin.userName)
        if dbAdmin:
            raise HTTPException(status_code=409, detail="User Name already registered")
        if ta.createMasterAdmin(db=db, admin=admin):
            return {'status_code':201, 'body':"User created"}
        else:
            raise Exception
    except (ValidationError, ValueError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body': "Invalid {}".format(str(e).split()[1])}
    # except Exception as e:
    #     return {'response': 500, 'message': repr(e)}    # I left this since this can help us, still. It can be deleted later on.

@app.post("/ASCEPUPR/ADMIN/LOGIN/", response_model=Administrators_Schemas.Administrator_Validate_User)
def loginAdmin(userName:str, passwd: str, token: str = None, db: Session = Depends(get_db)):
    try:
        admin = Administrators_Schemas.Administrator_LoginAccount_INPUTS(userName=userName,passwd=passwd,token=token)
        a = ta.loginAdmin(db,admin = admin)
        return {"status_code":a[0], 'body':a[1]}
    except (ValidationError, ValueError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}


@app.put("/ASCEPUPR/ADMIN/CHANGE_PASSWD_EMAIL/", response_model=Administrators_Schemas.Output_return)
def changeAdminPasswd(userName: str, masterAdminToken: str, newPasswd: str = None, newEmail: str = None,newPhone: str = None, db: Session = Depends(get_db)):
    try:
        admin = Administrators_Schemas.Administrator_ChangePasswdEmail_INPUTS(userName=userName,masterAdminToken=masterAdminToken, newPasswd=newPasswd,newEmail=newEmail, newPhone=newPhone)
        a = ta.changeAdminPasswdEmail(db=db,admin=admin)
        if a == True:
            return {"status_code":200, 'body':"Data was changed."}
        return {"status_code":400, 'body': 'Data was not changed: Invalid User Name'}
    except (ValidationError, ValueError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}
    # except Exception as e:
    #     return {'status_code': 500, 'body': repr(e)}
    
@app.delete("/ASCEPUPR/ADMIN/DEL_ACCOUNT/", response_model=Administrators_Schemas.Output_return)
def deleteAdmin(masterAdminToken: str, email: str, db:Session = Depends(get_db)):
    try:
        a = ta.deleteAdminEntry(db=db, admin = Administrators_Schemas.Administrator_Delete_Entry_INPUTS(masterAdminToken=masterAdminToken, email=email))
        if a == True:
            return {"status_code":200, 'body':"Deletion was a success."}
        return {"status_code":401, 'body': 'Deletion was not successful. Check if token and email were correct.'}
    except (ValidationError, ValueError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}

@app.delete("/ASCEPUPR/ADMIN/DEL_ALL/", response_model=Administrators_Schemas.Output_return)
def deleteAdmin(masterAdminToken: str, db:Session = Depends(get_db)):
    '''
        What I remember about the rise of the Empire is ... is how quiet it was. During the waning hours of the Clone Wars, 
        the 501st Legion was discreetly transferred back to Coruscant. It was a silent trip. We all knew what was about to 
        happen, and what we were about to do. Did we have any doubts? Any private, traitorous thoughts? Perhaps, but no one 
        said a word. Not on the flight to Coruscant, not when Order 66 came down, and not when we marched into the Jedi Temple. 
        Not a word.

        This will not delete master admins for security measure.
    '''
    try:
        a = ta.deleteAdminAll(db=db, admin = Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        if a == True:
            return {"status_code":200, 'body':"Deletion was a success."}
        return {"status_code":401, 'body': 'Deletion was not successful. Check if token is correct.'}
    except (ValidationError, ValueError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}


@app.post("/ascepupr/signupchapter/", status_code=HTTP_200_OK, response_model=SignUp_Schemas.output_Schema)
def val(name: str, email: str, phone:str, tshirt_size: str, age: int, bachelor:str, department: str, Academic_Years: int, db: Session = Depends(get_db)):
    try:
        user = SignUp_Schemas.set_SignUp_Data(name=name, email=email, phone=phone, tshirt_size=tshirt_size, age=age, bachelor=bachelor, department=department, aca_years=Academic_Years)
        data = SignUp_Test.put_SignUp_Data(db=db,user=user)
        print('this is data: ', data)
        return {'status_code':data[0], 'body': data[1]}
    except (ValidationError, ValueError, Exception) as e:
        return {'status_code':400, 'body':"Invalid {}".format(str(e).split('\n')[1])}
    
@app.get("/ascepupr/dashboard/table/memberstable/", status_code=HTTP_200_OK, response_model=SignUp_Schemas.output_Schema)
def get_members(db: Session = Depends(get_db)):
    try:
        return {"status_code":200, "body": SignUp_Test.get_SignUp_Table(db=db)}
    except Exception as e:
        return{"status_code": 400, "body":"Bad request"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
