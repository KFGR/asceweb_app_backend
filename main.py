# from fastapi import FastAPI
# from Backend.CRUD_FUNCTIONS.router import user
# import os

# app = FastAPI()

# app.include_router(user)

# if _name_ == "_main_":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

import traceback
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Backend.TESTS import SignUp_Test,Competitions_Test, Test_Admins as ta
from Backend.SCHEMAS import Administrators_Schemas, SignUp_Schemas, Competitions_Schema
from Backend.CONFIG.connection import engine, Base, SessionLocal
from pydantic import ValidationError
import json as json
from jwt.exceptions import DecodeError, InvalidSignatureError

from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT, HTTP_201_CREATED
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

@app.post("/ascepupr/login/user/form/user/logintodashboard/", response_model=Administrators_Schemas.Administrator_Validate_User)
def loginAdmin(userName:str, passwd: str, token: str = None, db: Session = Depends(get_db)):
    """Endpoint used to validate and authenticate administrator user by comparing the username and password to the ones in the database"""
    try:
        data = ta.loginAdmin(db,admin = Administrators_Schemas.Administrator_LoginAccount_INPUTS(userName=userName,passwd=passwd,token=token))
        return {"status_code":data[0], 'body':data[1]}
    except (ValidationError, Exception,DecodeError,InvalidSignatureError) as e:
        if type(e) == ValidationError: return {'status_code':404 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == Exception: return {"status_code":404, 'body':str(e)}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":404, 'body':str(e)}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.post("/ascepupr/dashboard/user/create/admin/createadmin/",status_code=HTTP_201_CREATED, response_model=Administrators_Schemas.Output_return)
def createAdmin(userName:str, passwd:str, name:str, email:str, phone: str, adminLevel: str, token: str, db: Session = Depends(get_db)):
    """Verificar si despues el token tiene que ser obligatorio"""
    '''
        Testing purposes or failsafe
    '''
    try:
        data = ta.createAdmin(db=db, admin=Administrators_Schemas.Administrator_CreateAccount_INPUTS(userName=userName, passwd=passwd,name=name,email=email,adminLevel=adminLevel, masterAdminToken=token, phone=phone))
        return{"status_code":HTTP_201_CREATED, 'body': data}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":404, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.post("/ascepupr/competitions/form/signuptocompetition/", status_code=HTTP_201_CREATED, response_model=Administrators_Schemas.Output_return)
def competitionSignUp(name: str, email: str, asce_member:str ,ascemembership_number: str, competition_name: str, courses:str, experiences: str,daily_availability: str, travel_availability: str, travel_june:str,older_than_twentyfive:str,heavy_driver:str, official_driver:str, db: Session = Depends(get_db)):
    try:
        data = Competitions_Test.put_Competition_Data(db=db,user=Competitions_Schema.set_Competitions_Data(name=name, email=email,asce_member=asce_member, ascemembership=ascemembership_number,competition_name=competition_name,courses=courses,experiences=experiences,daily_availability=daily_availability, travel_availability=travel_availability, travel_june=travel_june,older_than_twentyfive=older_than_twentyfive,heavy_driver=heavy_driver,official_driver=official_driver))
        return {"status_code":HTTP_201_CREATED, 'body':data}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":404, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.post("/ascewepupr/signup/form/signuptochapter/", status_code=HTTP_201_CREATED,response_model=Administrators_Schemas.Output_return)
def chapterSignUp(name: str, email: str, phone:str, tshirt_size: str, age: int, bachelor:str, department: str, Academic_Years: int, db: Session = Depends(get_db)):
    try:
        data = SignUp_Test.put_SignUp_Data(db=db,user=SignUp_Schemas.set_SignUp_Data(name=name, email=email, phone=phone, tshirt_size=tshirt_size, age=age, bachelor=bachelor, department=department, aca_years=Academic_Years))
        return {"status_code":HTTP_201_CREATED, 'body':data}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":404, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.get("/ascepupr/dashboard/user/table/admins/", status_code=HTTP_200_OK,response_model=Administrators_Schemas.Output_return)
def getAdmins(masterAdminToken: str, db: Session = Depends(get_db)):
    try:
        data = ta.getAdmins(db,admin=Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        return {'status_code':HTTP_200_OK, 'body':data}
    except (HTTPException,DecodeError,InvalidSignatureError) as e:
        if type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        if type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        return {"status_code":500, 'body':"Invalid Server Error"}

@app.get("/ascepupr/dashboard/user/table/members/", response_model=Administrators_Schemas.Output_return)
def getMembers(masterAdminToken: str, db: Session = Depends(get_db)):
    try:
        data = ta.get_SignUp_Table(db=db, admin=Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        return {'status_code':HTTP_200_OK, 'body':data}
    except (HTTPException,DecodeError,InvalidSignatureError) as e:
        if type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        if type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        return {"status_code":500, 'body':"Invalid Server Error"}

@app.get("/ascepupr/dashboard/user/table/competitions/", response_model=Administrators_Schemas.Output_return)
def getCompetitionsMembers(masterAdminToken: str, db: Session = Depends(get_db)):
    try:
        data = ta.get_Competitions_Table(db=db, admin=Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        return {'status_code':HTTP_200_OK, 'body':data}
    except (HTTPException,DecodeError,InvalidSignatureError) as e:
        if type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        if type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        return {"status_code":500, 'body':"Invalid Server Error"}

@app.put("/ascepupr/dashboard/admin/table/update/admin/updatefromadmin/", response_model=Administrators_Schemas.Output_return)
def updateAdmins(userName: str, masterAdminToken: str, newPasswd: str = None, newEmail: str = None,newPhone: str = None, newLevel: str = None,db: Session = Depends(get_db)):
    try:
        ta.updateAdmin(db=db,admin=Administrators_Schemas.Administrator_ChangePasswdEmail_INPUTS(userName=userName,masterAdminToken=masterAdminToken, newPasswd=newPasswd,newEmail=newEmail, newPhone=newPhone, newLevel=newLevel))
        return {"status_code":HTTP_201_CREATED, 'body':"User updated"}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":404, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}
    
@app.put("/ascepupr/dashboard/admin/table/update/members/updatefrommember", response_model=Administrators_Schemas.Output_return)
def updateMembers(token: str,name: str = None, email: str = None, phone:str = None, tshirt_size: str = None, age: int = None, bachelor:str = None, department: str = None, Academic_Years: int = None, db: Session = Depends(get_db)):
    try:
        data = ta.updateMembers(db=db,admin=Administrators_Schemas.Member_upate_table(name=name,masterAdminToken=token, email=email,phone=phone, tshirt_size=tshirt_size, age=age, bachelor=bachelor,department=department,aca_years=Academic_Years))
        return {"status_code":HTTP_201_CREATED, 'body':"User updated"}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":404, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.put("/ascepupr/dashboard/admin/table/update/competitionsmember/updatefromcompetitionsmember", response_model=Administrators_Schemas.Output_return)
def updateCompetitionsMembers(token: str,name: str = None, email: str = None, phone:str = None, tshirt_size: str = None, age: int = None, bachelor:str = None, department: str = None, Academic_Years: int = None, db: Session = Depends(get_db)):
    try:
        data = ta.updateMembers(db=db,admin=Administrators_Schemas.Competitions_upate_table(name=name,masterAdminToken=token, email=email,phone=phone, tshirt_size=tshirt_size, age=age, bachelor=bachelor,department=department,aca_years=Academic_Years))
        return {"status_code":HTTP_201_CREATED, 'body':"User updated"}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":404, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.delete("/ascepupr/dashboard/admin/table/delete/admin/deleteadminfromtable/", response_model=Administrators_Schemas.Output_return)
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

@app.delete("/ascepupr/dashboard/admin/table/delete/members/deletemembers/", response_model=Administrators_Schemas.Output_return)
def deleteMembers(masterAdminToken: str, email: str, db:Session = Depends(get_db)):
    try:
        a = ta.delete_all_Member(db=db, admin = Administrators_Schemas.Administrator_Delete_Entry_INPUTS(masterAdminToken=masterAdminToken, email=email))
        if a == True:
            return {"status_code":200, 'body':"Deletion was a success."}
        return {"status_code":401, 'body': 'Deletion was not successful. Check if token and email were correct.'}
    except (ValidationError, ValueError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}

@app.delete("/ascepupr/dashboard/admin/table/delete/competitionsmember/deletecompetitionsmember/", response_model=Administrators_Schemas.Output_return)
def deleteCompetitions(masterAdminToken: str, email: str, db:Session = Depends(get_db)):
    try:
        a = ta.delete_all_competitionsMember(db=db, admin = Administrators_Schemas.Administrator_Delete_Entry_INPUTS(masterAdminToken=masterAdminToken, email=email))
        return {"status_code":200, "body":a}
    except (ValidationError, ValueError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
        elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
        else: return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}

# @app.delete("/ASCEPUPR/ADMIN/DEL_ALL/", response_model=Administrators_Schemas.Output_return)
# def deleteAdmin(masterAdminToken: str, db:Session = Depends(get_db)):
#     '''
#         What I remember about the rise of the Empire is ... is how quiet it was. During the waning hours of the Clone Wars, 
#         the 501st Legion was discreetly transferred back to Coruscant. It was a silent trip. We all knew what was about to 
#         happen, and what we were about to do. Did we have any doubts? Any private, traitorous thoughts? Perhaps, but no one 
#         said a word. Not on the flight to Coruscant, not when Order 66 came down, and not when we marched into the Jedi Temple. 
#         Not a word.

#         This will not delete master admins for security measure.
#     '''
#     try:
#         a = ta.deleteAdminAll(db=db, admin = Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
#         if a == True:
#             return {"status_code":200, 'body':"Deletion was a success."}
#         return {"status_code":401, 'body': 'Deletion was not successful. Check if token is correct.'}
#     except (ValidationError, ValueError, HTTPException, Exception) as e:
#         if type(e) == ValidationError: return {'status_code':400 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
#         elif type(e) == ValueError: return {'status_code': 400,'body':str(e)}
#         elif type(e) == Exception: return {'status_code': 400,'body':str(e)}
#         elif type(e) == HTTPException: return {"status_code":400, 'body':e.detail}
#         else: return {"status_code":404, 'body':"Invalid {}".format(str(e).split()[1])}
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
    
