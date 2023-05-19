import traceback
from fastapi import Depends, FastAPI, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import exc
from Backend.TESTS import SignUp_Test,Competitions_Test, Test_Admins as ta
from Backend.SCHEMAS import Administrators_Schemas, SignUp_Schemas, Competitions_Schema
from Backend.CONFIG.connection import engine, Base, SessionLocal
from pydantic import ValidationError, SecretStr
import json as json
from jwt.exceptions import DecodeError, InvalidSignatureError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT, HTTP_201_CREATED

Base.metadata.create_all(bind = engine)

"""To view documentation of the endpoints change the below variable to be 
    app = FastAPI()
"""
# app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()


"""Orins, the variable containing all the IP allowed to use the backend application in this case the only IP allowed is the ASCEPUPR Domain name"""
# origins = [
#     "https://ajeto.azurewebsites.net",
#     "20.119.16.30"
# ]

# """Add the allowed origins IP's to the fastapi application variable """
# app.add_middleware(
#     # CORSMiddleware(origins,allow_methods=["*"], allow_headers=["*"])
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.middleware("http")
# async def block_localhost(request: Request, call_next):
#     client_host = request.client.host

#     if client_host == "127.0.0.1" or client_host == "::1" or client_host == "localhost":
#         raise HTTPException(status_code=403, detail="Access Forbidden from localhost")

#     response = await call_next(request)
#     return response


@app.post("/ascepupr/login/user/form/user/logintodashboard/", response_model=Administrators_Schemas.Administrator_Validate_User)
def loginAdmin(userName:str, passwd: SecretStr, db: Session = Depends(get_db)):
    """Endpoint used to validate and authenticate administrator user by comparing the username and password to the ones in the database"""
    try:
        data = ta.loginAdmin(db,admin = Administrators_Schemas.Administrator_LoginAccount_INPUTS(userName=userName,passwd=passwd))
        return {"status_code":HTTP_201_CREATED, 'body':data}
    except (ValidationError, Exception,DecodeError,InvalidSignatureError) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == Exception: return {"status_code":404, 'body':str(e)}
        # elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
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
        # elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.post("/ascepupr/competitions/form/signuptocompetition/", status_code=HTTP_201_CREATED, response_model=Administrators_Schemas.Output_return)
def competitionSignUp(name: str, email: str, asce_member:str ,ascemembership_number: str, competition_name: str, courses:str, experiences: str,daily_availability: str, travel_availability: str, travel_june:str,older_than_twentyfive:str,heavy_driver:str, official_driver:str, db: Session = Depends(get_db)):
    try:
        data = Competitions_Test.put_Competition_Data(db=db,user=Competitions_Schema.set_Competitions_Data(name=name, email=email,asce_member=asce_member, ascemembership=ascemembership_number,competition_name=competition_name,courses=courses,experiences=experiences,daily_availability=daily_availability, travel_availability=travel_availability, travel_june=travel_june,older_than_twentyfive=older_than_twentyfive,heavy_driver=heavy_driver,official_driver=official_driver))
        return {"status_code":HTTP_201_CREATED, 'body':data}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        # elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.post("/ascewepupr/signup/form/signuptochapter/", status_code=HTTP_201_CREATED,response_model=Administrators_Schemas.Output_return)
def chapterSignUp(name: str, email: str, phone:str, tshirt_size: str, age: int, bachelor:str, department: str, Academic_Years: int, db: Session = Depends(get_db)):
    try:
        data = SignUp_Test.put_SignUp_Data(db=db,user=SignUp_Schemas.set_SignUp_Data(name=name, email=email, phone=phone, tshirt_size=tshirt_size, age=age, bachelor=bachelor, department=department, aca_years=Academic_Years))
        return {"status_code":HTTP_201_CREATED, 'body':data}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        # elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
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
        return {"status_code":500, 'body':"Internal Server Error"}

@app.get("/ascepupr/dashboard/user/table/members/",status_code=HTTP_200_OK, response_model=Administrators_Schemas.Output_return)
def getMembers(masterAdminToken: str, db: Session = Depends(get_db)):
    try:
        data = ta.get_SignUp_Table(db=db, admin=Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        return {'status_code':HTTP_200_OK, 'body':data}
    except (HTTPException,DecodeError,InvalidSignatureError) as e:
        if type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        if type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        return {"status_code":500, 'body':"Internal Server Error"}

@app.get("/ascepupr/dashboard/user/table/competitions/", status_code=HTTP_200_OK,response_model=Administrators_Schemas.Output_return)
def getCompetitionsMembers(masterAdminToken: str, db: Session = Depends(get_db)):
    try:
        data = ta.get_Competitions_Table(db=db, admin=Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        return {'status_code':HTTP_200_OK, 'body':data}
    except (HTTPException,DecodeError,InvalidSignatureError) as e:
        if type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        if type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        return {"status_code":500, 'body':"Internal Server Error"}

@app.get("/ascewepupr/isTokenValid/", status_code=HTTP_200_OK, response_model=Administrators_Schemas.Output_return)
def isTokenValid(masterAdminToken:str, db:Session = Depends(get_db)):
    try:
        data = ta.isTokenValid(db, admin=Administrators_Schemas.Administrator_MasterAdminToken(masterAdminToken=masterAdminToken))
        return {"status_code": HTTP_200_OK, "body": data}
    except(Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        if type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        else: return {"status_code": 500, "body": "Internal Server Error"}

@app.put("/ascepupr/dashboard/admin/table/update/admin/updatefromadmin/", status_code=HTTP_201_CREATED,response_model=Administrators_Schemas.Output_return)
def updateAdmins(userName: str, masterAdminToken: str, newPasswd: str = None, newEmail: str = None,newPhone: str = None, newLevel: str = None,db: Session = Depends(get_db)):
    try:
        ta.updateAdmin(db=db,admin=Administrators_Schemas.Administrator_ChangePasswdEmail_INPUTS(userName=userName,masterAdminToken=masterAdminToken, newPasswd=newPasswd,newEmail=newEmail, newPhone=newPhone, newLevel=newLevel))
        return {"status_code":HTTP_201_CREATED, 'body':"User updated"}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}
    
@app.put("/ascepupr/dashboard/admin/table/update/members/updatefrommember", status_code=HTTP_201_CREATED,response_model=Administrators_Schemas.Output_return)
def updateMembers(token: str,email: str, newEmail: str = None, newPhone:str = None, newTshirt_size: str = None, newAge: int = None, newBachelor:str = None, newDepartment: str = None, newAcademic_Years: int = None, newMembership: str = None, db: Session = Depends(get_db)):
    try:
        data = ta.updateMembers(db=db,user=Administrators_Schemas.Member_update_table(masterAdminToken=token, email=email, newEmail=newEmail, newPhone=newPhone, newTshirt_size=newTshirt_size, newAge=newAge, newBachelor=newBachelor, newDepartment=newDepartment, newAca_years=newAcademic_Years, newMembershipPaid=newMembership))
        return {"status_code":HTTP_201_CREATED, 'body':data}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.put("/ascepupr/dashboard/admin/table/update/competitionsmember/updatefromcompetitionsmember", status_code=HTTP_201_CREATED,response_model=Administrators_Schemas.Output_return)
def updateCompetitionsMembers(token: str, email: str, newEmail: str = None, newPhone: str = None, newAscemember: str = None, newAscemembership: str = None,newCompetition_name:str = None, newCourses: str = None, newDaily_Avail: str = None, newTravel: str = None, newTravel_june: str = None, newOlder: str=None, newHeavy: str = None, newOffdriver: str = None, newCompetitions_form: str = None, newExperiences: str =None ,db: Session = Depends(get_db)):
    try:
        data = ta.updateCompetitionsMembers(db=db,user=Administrators_Schemas.Competitions_update_table(masterAdminToken=token, email=email, newEmail=newEmail, newPhone=newPhone, newAscemember=newAscemember, newAscemembership=newAscemembership, newCompetition_name=newCompetition_name, newCourses=newCourses, newDaily_availability=newDaily_Avail, newTravel_availability=newTravel, newOlder_than_twentyfive=newOlder, newHeavy_driver=newHeavy, newOfficial_driver=newOffdriver, newTravel_june=newTravel_june, newCompetitions_form=newCompetitions_form,newExperiences=newExperiences))
        return {"status_code":HTTP_201_CREATED, 'body':"User updated"}
    except (ValidationError, ValueError, Exception,DecodeError,InvalidSignatureError, HTTPException) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':json.loads(e.json())[0]['msg']}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {'status_code':e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}






@app.delete("/ascepupr/dashboard/admin/table/delete/admin/deleteadminfromtable/", status_code=HTTP_200_OK,response_model=Administrators_Schemas.Output_return)
def deleteAdmin(masterAdminToken: str, email: str, db:Session = Depends(get_db)):
    try:
        data = ta.delete_admin(db=db, admin = Administrators_Schemas.Administrator_Delete_Entry_INPUTS(masterAdminToken=masterAdminToken, email=email))
        return {"status_code":HTTP_200_OK, 'body':data}
    except (ValidationError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.delete("/ascepupr/dashboard/admin/table/delete/members/deletemembers/", status_code=HTTP_200_OK,response_model=Administrators_Schemas.Output_return)
def deleteMembers(masterAdminToken: str, email: str, db:Session = Depends(get_db)):
    try:
        data = ta.delete_members(db=db, admin = Administrators_Schemas.Administrator_Delete_Entry_INPUTS(masterAdminToken=masterAdminToken, email=email))
        return {"status_code":HTTP_200_OK, 'body':data}
    except (ValidationError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.delete("/ascepupr/dashboard/admin/table/delete/competitionsmember/deletecompetitionsmember/", status_code=HTTP_200_OK,response_model=Administrators_Schemas.Output_return)
def deleteCompetitions(masterAdminToken: str, email: str, db:Session = Depends(get_db)):
    try:
        data = ta.delete_competitionsMember(db=db, admin = Administrators_Schemas.Administrator_Delete_Entry_INPUTS(masterAdminToken=masterAdminToken, email=email))
        return {"status_code":HTTP_200_OK, "body":data}
    except (ValidationError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.delete("/ascepupr/dashboard/admin/table/delete/members/list/deletemembers/", response_model=Administrators_Schemas.Output_return)
def delete_list_members(token:str, emails:list, db: Session = Depends(get_db)):
    try: 
        data = ta.delete_members_list(db=db,admin=Administrators_Schemas.Administrator_list_delete(masterAdminToken=token, emails=emails))
        return {'status_code':HTTP_200_OK, 'body':data}
    except (ValidationError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}

@app.delete("/ascepupr/dashboard/admin/table/delete/members/list/deletecompetitions/", response_model=Administrators_Schemas.Output_return)
def delete_list_competitions(token:str, emails:list, db: Session = Depends(get_db)):
    try: 
        data = ta.delete_competitions_list(db=db,admin=Administrators_Schemas.Administrator_list_delete(masterAdminToken=token, emails=emails))
        return {'status_code':HTTP_200_OK, 'body':data}
    except (ValidationError, HTTPException, Exception) as e:
        if type(e) == ValidationError: return {'status_code':422 ,'body':"Invalid {}".format(str(e).split('\n')[1])}
        elif type(e) == DecodeError or type(e) == InvalidSignatureError: return {"status_code":401, 'body':str(e)}
        elif type(e) == HTTPException: return {"status_code":e.status_code, 'body':e.detail}
        else: return {"status_code":500, 'body':"Internal Server Error"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
