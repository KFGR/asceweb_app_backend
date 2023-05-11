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
from Backend.TESTS import SignUp_Test,Competitions_Test, Test_Admins as ta
from Backend.SCHEMAS import Administrators_Schemas, SignUp_Schemas, Competitions_Schema
from Backend.CONFIG.connection import engine, Base, SessionLocal
from pydantic import ValidationError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_200_OK
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

@app.get("/ASCEPUPR/ADMIN/GET_ADMINS/", response_model=Administrators_Schemas.Output_return)
def getAdmins(masterAdminToken: str, db: Session = Depends(get_db)):
    try:
        dbAdmins = ta.getAdmins(db,admin=Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        return {'status_code':200, 'body':dbAdmins}
    except Exception as e:
        return {'status_code': 404, 'body':"Invalid {}".format(str(e).split()[1])}

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFkbWluTWFzdGVyIiwiZXhwX2RhdGUiOjE2ODM3NzUxNjUuNTQ3OTg1LCJsZXZlbCI6Ik1BIn0.3P8AHnvQk2z65nnpvR9isHowXqqAR4HaTFNMQaQFTC0
@app.post("/ascepupr/dashboard/user/create/createadmin/", response_model=Administrators_Schemas.Output_return)
def createAdmin(userName:str, passwd:str, name:str, email:str, phone: str, adminLevel: str, token: str, db: Session = Depends(get_db)):
    """Verificar si despues el token tiene que ser obligatorio"""
    '''
        Testing purposes or failsafe
    '''
    try:
        admin = Administrators_Schemas.Administrator_CreateAccount_INPUTS(userName=userName, passwd=passwd,name=name,email=email,adminLevel=adminLevel, masterAdminToken=token, phone=phone)
        ta.createAdmin(db=db, admin=admin)
        return {"status_code":200, 'body': "User Created"}
    except (ValidationError, ValueError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body': "Invalid {}".format(str(e).split()[1])}

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

@app.post("/ascepupr/signup/form/signuptochapter/", status_code=HTTP_200_OK, response_model=SignUp_Schemas.output)
def chapterSignUp(name: str, email: str, phone:str, tshirt_size: str, age: int, bachelor:str, department: str, Academic_Years: int, db: Session = Depends(get_db)):
    try:
        data = SignUp_Test.put_SignUp_Data(db=db,user=SignUp_Schemas.set_SignUp_Data(name=name, email=email, phone=phone, tshirt_size=tshirt_size, age=age, bachelor=bachelor, department=department, aca_years=Academic_Years))
        return {'status_code': 200, 'body': data}
    except (ValidationError, ValueError, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body':repr(e)}
        # return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}

@app.get("/ascepupr/dashboard/user/table/members/", status_code=HTTP_200_OK, response_model=Administrators_Schemas.Output_return)
def get_members(masterAdminToken: str, db: Session = Depends(get_db)):
    try:
        data = ta.get_SignUp_Table(db=db, admin=Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        return {"status_code":200, "body": data}
    except Exception as e:
        return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}

@app.put("/ascepupr/dashboard/user/table/members/update", response_model=Administrators_Schemas.Output_return)
def updateMembers(token: str,name: str = None, email: str = None, phone:str = None, tshirt_size: str = None, age: int = None, bachelor:str = None, department: str = None, Academic_Years: int = None, db: Session = Depends(get_db)):
    try:
        admin = Administrators_Schemas.Member_upate_table(name=name,masterAdminToken=token, email=email,phone=phone, tshirt_size=tshirt_size, age=age, bachelor=bachelor,department=department,aca_years=Academic_Years)
        a = ta.changeSignUpdata(db=db,admin=admin)
        if a == True:
            return {"status_code":200, 'body':"Data was changed."}
        return {"status_code":400, 'body': 'Data was not changed: Invalid User Name'}
    except (ValidationError, ValueError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body':repr(e)}
# @app.post("/ascepupr/competitions/form/signuptocompetition/", status_code=HTTP_200_OK, response_model=Competitions_Schema.output)
# def chapterSignUp(name: str, email: str, phone:str, ascemembership: str, competition_name: str, courses:str, daily_avail: str, travel_avail: str,age_gt_twtfive:str,heavy_driver:str, offdriver_avail:str, db: Session = Depends(get_db)):
#     try:
#         data = Competitions_Test.put_Competition_Data(db=db,user=Competitions_Schema.set_Competitions_Data(name=name, email=email, phone=phone,ascemembership=ascemembership, competition_name=competition_name, courses=courses, daily_availability=daily_avail, travel_availability=travel_avail,older_than_twentyfive=age_gt_twtfive, official_driver=offdriver_avail, heavy_driver=heavy_driver))
#         return {'status_code': 200, 'body': data}
#     except (ValidationError, ValueError, Exception) as e:
#         if type(e) == ValidationError: return {'status_code':400 ,'body':traceback.format_exception(e)}
#         elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
#         elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
#         elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
#         else: return {"status_code":404, 'body':repr(e)}



# "Invalid {}".format(str(e).split()[1])
        # else: return {"status_code":404, 'body': "Invalid {}".format(str(e).split()[1])}
    # except Exception as e:
    #     return {'response': 500, 'message': repr(e)}    # I left this since this can help us, still. It can be deleted later on.

# @app.post("/ASCEPUPR/ADMIN/CREATE_ACCOUNT/", response_model=Administrators_Schemas.Output_return)
# def createAdmin(userName:str, passwd:str, name:str, email:str, phone:str, adminLevel:str,masterAdminToken:str, db: Session = Depends(get_db)):
#     try:
#         admin = Administrators_Schemas.Administrator_CreateAccount_INPUTS(userName=userName, passwd=passwd,name=name,email=email,phone=phone,adminLevel=adminLevel, masterAdminToken=masterAdminToken)
#         dbAdmin = ta.getAdminbyEmail(db, email=admin.email)
#         if dbAdmin:
#             raise HTTPException(status_code=409, detail="Email already registered")
#         dbAdmin = ta.getAdminbyUserName(db, username=admin.userName)
#         if dbAdmin:
#             raise HTTPException(status_code=409, detail="User Name already registered")
#         dbAdmin = ta.getAdminbyUserName(db, username=admin.phone)
#         if dbAdmin:
#             raise HTTPException(status_code=409, detail="Phone already registered")
#         if ta.createAdmin(db=db, admin=admin):
#             return {'status_code':201, 'body':"User created"}
#         else:
#             raise Exception
#     except (ValidationError, ValueError,HTTPException,IntegrityError, Exception) as e:
#         if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
#         elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
#         elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
#         elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
#         elif type(e) == IntegrityError: return {"status_code":404, 'body': "duplicate entry"}
#         else: return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}
    # except Exception as e:
    #     return {'response': 500, 'message': repr(e)}    # I left this since this can help us, still. It can be deleted later on.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
