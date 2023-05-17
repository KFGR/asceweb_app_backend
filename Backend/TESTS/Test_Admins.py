from sqlalchemy.orm import Session
from sqlalchemy import or_, exc
from Backend.DATABASE.Administrators_Table import Administrators_Table
from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
from Backend.DATABASE.Competitions_Table import Competitions_Table
import Backend.SCHEMAS.Administrators_Schemas as adminSchema
from Backend.API.Security import Secuirity as sc
from fastapi import HTTPException
from typing import Union
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
__sc = sc()
'''
    If working properly, functions to be moved elsewhere in the future.
'''


def ValidateExist(db:Session,table: str, user: Union[adminSchema.Administrator_LoginAccount_DB, adminSchema.Member_upate_table,adminSchema.Administrator_ChangePasswdEmail_DB, adminSchema.Competitions_upate_table]):
    """Returns false if user does not exist, else raise exception if username, phone or email exist"""
    if table == "CreateAdmin":
        db_profile = db.query(Administrators_Table).filter(or_(Administrators_Table.email == user.email,Administrators_Table.username == user.userName,Administrators_Table.phone == user.phone)).first()
        if db_profile:
            if db_profile.username == user.userName:
                raise HTTPException(status_code=409, detail='Username already exist')
            if db_profile.email == user.email:
                raise HTTPException(status_code=409, detail='Email already exist')
            if db_profile.phone == user.phone:
                raise  HTTPException(status_code=409, detail='Phone already exist')
        return False
    elif table == "UpdateAdmin":
        db_profile = db.query(Administrators_Table).filter(or_(Administrators_Table.email == user.newEmail,Administrators_Table.username == user.userName,Administrators_Table.phone == user.newPhone)).first()
        if db_profile:
            if db_profile.email == user.newEmail:
                raise HTTPException(status_code=409, detail='Email already exist')
            if db_profile.phone == user.newPhone:
                raise  HTTPException(status_code=409, detail='Phone already exist')
        return False
    elif table == "UpdateChapterMember":
        db_profile = db.query(Chapter_Members_Table).filter(or_(Chapter_Members_Table.email == user.email)).first()
        if db_profile:
            if db_profile.email == user.newEmail:
                raise HTTPException(status_code=409, detail='Email already exist')
            if db_profile.phone == user.newPhone:
                raise  HTTPException(status_code=409, detail='Phone already exist')
        return False
    elif table == "UpdateCompetitionsSignUp":
        db_profile = db.query(Competitions_Table).filter(or_(Competitions_Table.email == user.email)).first()
        if db_profile:
            if db_profile.email == user.newEmail:
                raise HTTPException(status_code=409, detail='Email already exist')
            if db_profile.phone == user.newPhone:
                raise  HTTPException(status_code=409, detail='Phone already exist')
            if db_profile.asce_member == user.newAscemember:
                raise  HTTPException(status_code=409, detail='Membership already exist')
        return False
    raise Exception("Table {} does not exist".format(table))



def createAdmin(db:Session, admin: adminSchema.Administrator_CreateAccount_DB):
    """Function used to create admin users, by first validating that the username, phone and email does not exist"""
    if not ValidateExist(db, table="CreateAdmin", user=admin):
        admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
        if admin_user:
            if __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user.admin_level == 'MA':
                dbAdmin = Administrators_Table(name=admin.name, email=admin.email,phone=admin.phone, username=admin.userName, password=__sc.encryptHash(admin.passwd.get_secret_value()), admin_level=admin.adminLevel,created_at=admin.createdAt, updated_at=admin.updatedAt)
                db.add(dbAdmin)
                db.commit()
                db.refresh(dbAdmin)
                return "Administrator created"
            raise HTTPException(status_code=401, detail="Invalid Administrator")
        raise HTTPException(status_code=404, detail="No username found")
    raise HTTPException(status_code=409, detail="User already in table")


def loginAdmin(db: Session, admin: adminSchema.Administrator_LoginAccount_DB) -> list:
    """Validate username and password as well as token to return either an invalid login or valid login"""
    db_information = db.query(Administrators_Table.username, Administrators_Table.password, Administrators_Table.admin_level).filter(Administrators_Table.username == admin.userName).first()
    if db_information:
        if __sc.validateUsername(admin.userName, db_information[0]) and __sc.validateHash(admin.passwd.get_secret_value(), str(db_information[1])):
            data = __sc.createToken({'username':admin.userName,'admin_level':db_information[2]})
            return data
        raise HTTPException(status_code=401, detail="Invalid username or password")
    raise HTTPException(status_code=404, detail="No username found")
    



def getAdmins(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    """Function that returns the whole table of admins users"""
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user:
        if __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True]:
            if admin_user[1] == "MA":
                admins = db.query(Administrators_Table).all()
                if admins:
                    return [adminSchema.Administrator_GETTER(idAdministrators=entry.idadministrators,name=entry.name,userName=entry.username,password=entry.password,email=entry.email, phone=entry.phone,adminLevel=entry.admin_level, createdAt=entry.created_at, updatedAt=entry.updated_at) for entry in admins]
                raise HTTPException(status_code=400, detail="No data was found")
            
            elif admin_user[1] == "GA":
                admins = db.query(Administrators_Table).all()
                if admins:
                    return [adminSchema.Administrator_GETTER(idAdministrators=entry.idadministrators,name=entry.name,userName=entry.username,password="",email=entry.email, phone=entry.phone,adminLevel=entry.admin_level, createdAt=entry.created_at, updatedAt=entry.updated_at) for entry in admins]
                raise HTTPException(status_code=400, detail="No data was found")
            else:raise HTTPException(status_code=401, detail="Invalid Admin Level")
        raise HTTPException(status_code=401, detail="Invalid Administrator")
    raise HTTPException(status_code=404, detail="No administrator found")


def get_SignUp_Table(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user:
        if __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA" or  admin_user[1] == "GA":
            members = db.query(Chapter_Members_Table).all()
            if members:
                return [adminSchema.get_SignUp_Data(idchapter_members=entry.idchapter_members,name=entry.name,email=entry.email,phone=entry.phone,tshirt_size=entry.tshirt_size,age=entry.age,bachelor=entry.bachelor,department=entry.department,type=entry.type,created_at=entry.created_at,competitions_form=entry.competitions_form,aca_years=entry.aca_years,membership_paid=entry.membership_paid,membership_until=entry.membership_until) for entry in members]
            raise HTTPException(status_code=400, detail="No data was found")
        raise HTTPException(status_code=401, detail="Invalid Administrator")
    raise HTTPException(status_code=404, detail="No user found")

def get_Competitions_Table(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    """Function that returns the whole table of admins users"""
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user:
        if __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA" or  admin_user[1] == "GA":
            admins = db.query(Competitions_Table).all()
            if admins:
                return [adminSchema.get_Competitions_Data(idchapter_members=entry.idchapter_members,name=entry.name,email=entry.email,phone=entry.phone,asce_member=entry.asce_member,ascemembership=entry.ascemembership, competition_name=entry.competition_name,courses=entry.courses, daily_availability=entry.daily_avail, experiences=entry.experiences, travel_availability=entry.travel_avail, travel_june=entry.travel_june, older_than_twentyfive=entry.age_gt_twtfive,heavy_driver=entry.hv_vehicle,official_driver=entry.offdriver_avail,competitions_form=entry.competitions_form,created_at=entry.created_at) for entry in admins]
            raise HTTPException(status_code=400, detail="No data was found")
        raise HTTPException(status_code=401, detail="Invalid Administrator")
    raise HTTPException(status_code=404, detail="No user found")

def delete_members(db:Session, admin: adminSchema.Administrator_Delete_Entry_INPUTS):
    admin_user = db.query(Administrators_Table.username, Administrators_Table.admin_level, Administrators_Table.email).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user:
        if __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA":
            user_member = db.query(Chapter_Members_Table).filter(Chapter_Members_Table.email == admin.email).first()
            if user_member:
                comp_member = db.query(Competitions_Table).filter(Competitions_Table.email == admin.email).delete()
                if comp_member:
                    user_member.competitions_form = "No"
                else:
                    db.delete(user_member)
                    db.commit()
                    return "User was deleted"
                raise HTTPException(status_code=204, detail="No data deleted")
            raise HTTPException(status_code=404, detail="Member not found")
        raise HTTPException(status_code=401, detail="Invalid administrator")
    raise HTTPException(status_code=404, detail="Administrator not found")

def delete_competitionsMember(db:Session, admin: adminSchema.Administrator_Delete_Entry_INPUTS):
    admin_user = db.query(Administrators_Table.username, Administrators_Table.admin_level, Administrators_Table.email).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user:
        if __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA" and admin_user[2] != admin.email:
            user_member = db.query(Chapter_Members_Table).filter(Chapter_Members_Table.email == admin.email).first()
            if user_member:
                user_member.competitions_form = 'No'
                if(bool(db.query(Competitions_Table).filter(Competitions_Table.email == admin.email).delete())):
                    db.commit()
                    return "User was deleted"
                raise HTTPException(status_code=204, detail="No data deleted")
            raise HTTPException(status_code=404, detail="Member not found")
        raise HTTPException(status_code=401, detail="Invalid administrator")
    raise HTTPException(status_code=404, detail="Administrator not found")

def delete_admin(db: Session, admin: adminSchema.Administrator_Delete_Entry_INPUTS):
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level, Administrators_Table.email).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user:
        if __sc.validateToken(admin_user[0], admin_user[1], admin.masterAdminToken) == [True, True] and admin_user[1] == "MA" and admin_user[2] != admin.email:
            tmp = db.query(Administrators_Table).filter(admin.email == Administrators_Table.email).first()
            if tmp:
                if(bool(db.query(Administrators_Table).filter(admin.email == Administrators_Table.email).delete())):
                    db.commit()
                    return "User deleted"
                raise HTTPException(status_code=204, detail="No data deleted")
            raise HTTPException(status_code=404, detail="Member not found")
        raise HTTPException(status_code=401, detail="Invalid administrator")
    raise HTTPException(status_code=404, detail="Administrator not found")


def updateAdmin(db: Session, admin: adminSchema.Administrator_ChangePasswdEmail_DB):
    """Function used to make updates in the administrators table, only available if the user making the changes is a MA"""
    if not ValidateExist(db=db,table="UpdateAdmin", user=admin):
        admin_user = db.query(Administrators_Table.username, Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
        if admin_user and __sc.validateToken(admin_user[0], admin_user[1], admin.masterAdminToken) == [True, True] and admin_user[1] == "MA":
            user_row = db.query(Administrators_Table).filter(Administrators_Table.username == admin.userName).first()
            if user_row:
                if not (admin.newEmail or admin.newPasswd or admin.newPhone or admin.newLevel):
                    raise HTTPException(status_code=204, detail="No data was changed")
                
                if admin.newEmail is not None:
                    if admin.newEmail != user_row.email:
                        user_row.email = admin.newEmail
                    else: raise HTTPException(status_code=409, detail="This user is already using this email")

                if admin.newPasswd is not None:
                    if not __sc.validateHash(admin.newPasswd.get_secret_value(),user_row.password):
                        user_row.password = __sc.encryptHash(admin.newPasswd.get_secret_value())
                    else: raise HTTPException(status_code=409, detail="Cannot use the same password")

                if admin.newPhone is not None:
                    if admin.newPhone != user_row.phone:
                        user_row.phone = admin.newPhone
                    else: raise HTTPException(status_code=409, detail="This user is already using this phone number")
                
                if admin.newLevel is not None:
                    if admin.newLevel != user_row.admin_level:
                        user_row.admin_level = admin.newLevel
                    else: raise HTTPException(status_code=409, detail="This user is already this administrator level")
                
                user_row.updated_at = admin.updatedAt
                db.commit()
                db.refresh(user_row)
                return True
            else:raise HTTPException(status_code=404, detail="No username found")
        else:raise HTTPException(status_code=401, detail="Invalid Administrator")
    raise Exception("Something went wrong") #goes directly to internal server error exception

def updateCompetitionsMembers(db: Session, user:adminSchema.Competitions_update):
    if not ValidateExist(db=db,table="UpdateCompetitionsSignUp", user=user):
        admin_user = db.query(Administrators_Table.username, Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(user.masterAdminToken)['username']).first()
        if admin_user and __sc.validateToken(admin_user[0], admin_user[1], user.masterAdminToken) == [True, True] and admin_user[1] == "MA":
            user_row = db.query(Competitions_Table).filter(Competitions_Table.email == user.email).first()
            if user_row:
                user_chapter_row = db.query(Chapter_Members_Table).filter(Chapter_Members_Table.email == user.email).first()
                if not (user.newEmail or user.newPhone or user.newOlder_than_twentyfive or user.newAscemember or user.newAscemembership or user.newCompetition_name or user.newCompetitions_form or user.newCourses or user.newDaily_availability or user.newExperiences or user.newHeavy_driver or user.newOfficial_driver or user.newTravel_availability or user.newTravel_june):
                    raise HTTPException(status_code=204, detail="No data was changed")
                
                if user.newEmail is not None:
                    if user.newEmail != user_row.email:
                        user_row.email = user.newEmail
                        user_chapter_row.email = user_row.email
                    else: 
                        raise HTTPException(status_code=409, detail="This user is already using this email")
                
                if user.newPhone is not None:
                    if user.newPhone != user_row.phone:
                        user_row.phone = user.newPhone
                        user_chapter_row.phone = user_row.phone
                    else:
                        raise HTTPException(status_code=409, detail="The user is already using this phone number")
                    
                if user.newAscemembership is not None:
                    if user.newAscemembership != user_row.ascemembership:
                        user_row.ascemembership = user.newAscemembership
                    else:
                        raise HTTPException(status_code=409, detail="The user is already registered to the ASCE using this number")
                
                if user.newCompetition_name is not None:
                    if user.newCompetition_name != user_row.competition_name:
                        user_row.competition_name = user.newCompetition_name
                    else:
                        raise HTTPException(status_code=409, detail="The user is already registered using these competitions")
                
                if user.newCourses is not None:
                    if user.newCourses != user_row.courses:
                        user_row.courses = user.newCourses
                    else:
                        raise HTTPException(status_code=409, detail="The user is already registered using these courses")
                
                if user.newDaily_availability is not None:
                    if user.newDaily_availability != user_row.daily_avail:
                        user_row.daily_avail = user.newDaily_availability
                    else:
                        raise HTTPException(status_code=409, detail="The user is already available during the same days")
                
                if user.newExperiences is not None:
                    if user.newExperiences != user_row.experiences:
                        user_row.experiences = user.newExperiences
                    else:
                        raise HTTPException(status_code=409, detail="The user is already available during the same days")
                
                if user.newAscemember is not None:
                    if user.newAscemember != user_row.asce_member:
                        user_row.asce_member = user.newAscemember
                    else:
                        raise HTTPException(status_code=409, detail="The user is already of the same ASCE Member Type")
                
                if user.newTravel_availability is not None:
                    if user.newTravel_availability != user_row.travel_avail:
                        user_row.travel_avail = user.newTravel_availability
                    else:
                        raise HTTPException(status_code=409, detail="The user alrady has the same travel availability type")
                
                if user.newTravel_june is not None:
                    if user.newTravel_june != user_row.travel_june:
                        user_row.travel_june = user.newTravel_june
                    else:
                        raise HTTPException(status_code=409, detail="The user alrady has the same travel availability type for June")
                
                if user.newOlder_than_twentyfive is not None:
                    if user.newOlder_than_twentyfive != user_row.age_gt_twtfive:
                        user_row.age_gt_twtfive = user.newOlder_than_twentyfive
                    else:
                        raise HTTPException(status_code=409, detail="The user alrady has the same state for 'Age is greater than 25'")
                    
                if user.newHeavy_driver is not None:
                    if user.newHeavy_driver != user_row.hv_vehicle:
                        user_row.hv_vehicle = user.newHeavy_driver
                    else:
                        raise HTTPException(status_code=409, detail="The user's availability to drive heavy vehicle is the same")
                
                if user.newOfficial_driver is not None:
                    if user.newOfficial_driver != user_row.offdriver_avail:
                        user_row.offdriver_avail = user.newOfficial_driver
                    else:
                        raise HTTPException(status_code=409, detail="The user's availabilty to be the organization official driver is the same")
                
                if user.newCompetitions_form is not None:
                    if user.newCompetitions_form != user_row.competitions_form:
                        user_row.competitions_form = user.newCompetitions_form
                        user_chapter_row = user.newCompetitions_form
                        """cambiar row de mmebers a no"""
                    else:
                        raise HTTPException(status_code=409, detail="The user's availabilty to be the organization official driver is the same")
                
                db.commit()
                db.refresh(user_row)
                db.refresh(user_chapter_row)
                return True
            else:raise HTTPException(status_code=404, detail="No username found")
        else:raise HTTPException(status_code=401, detail="Invalid Administrator")
    raise Exception("Something went wrong") #goes directly to internal server error exception


def updateMembers(db: Session, user:adminSchema.Member_update):
    """Email, phone and id are unique"""
    if not ValidateExist(db=db,table="UpdateChapterMember", user=user):
        admin_user = db.query(Administrators_Table.username, Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(user.masterAdminToken)['username']).first()
        if admin_user and __sc.validateToken(admin_user[0], admin_user[1], user.masterAdminToken) == [True, True] and admin_user[1] == "MA":
            user_row = db.query(Chapter_Members_Table).filter(Chapter_Members_Table.email == user.email).first()
            if user_row:
                if not (user.newEmail or user.newPhone or user.newTshirt_size or user.newAge or user.newBachelor or user.newDepartment or user.newAca_years or user.newMembershipPaid):
                    raise HTTPException(status_code=204, detail="No data was changed")
                
                if user.newEmail is not None:
                    if user.newEmail != user_row.email:
                        user_row.email = user.newEmail
                    else: raise HTTPException(status_code=409, detail="This user is already using this email")

                if user.newTshirt_size is not None:
                    if user.newTshirt_size != user_row.tshirt_size:
                        user_row.tshirt_size = user.newTshirt_size
                    else: pass

                if user.newPhone is not None:
                    if user.newPhone != user_row.phone:
                        user_row.phone = user.newPhone
                    else: raise HTTPException(status_code=409, detail="This user has already this phone number")

                if user.newAge is not None:
                    if user.newAge != user_row.age:
                        user_row.age = user.newAge
                    else: raise HTTPException(status_code=409, detail="This user has already this age")

                if user.newBachelor is not None:
                    if user.newBachelor != user_row.bachelor:
                        user_row.bachelor = user.newBachelor
                    else: raise HTTPException(status_code=409, detail="This user has already this bachelors name")

                if user.newDepartment is not None:
                    if user.newDepartment != user_row.department:
                        user_row.department = user.newDepartment
                    else: raise HTTPException(status_code=409, detail="This user has already this department name")

                if user.newAca_years is not None:
                    if user.newAca_years != user_row.aca_years:
                        user_row.aca_years = user.newAca_years
                    else: raise HTTPException(status_code=409, detail="This user is already using this age")

                if user.newMembershipPaid is not None:
                    if user.newMembershipPaid != user_row.membership_paid:
                        user_row.membership_paid = user.newMembershipPaid
                        if user.newMembershipPaid == "Yes":
                            user_row.membership_until = str(dt.now().date() + relativedelta(years=1))
                        else:
                            user_row.membership_until = "Expired"
                    else: raise HTTPException(status_code=409, detail="This user is already using this membership value")
                
                db.commit()
                db.refresh(user_row)
                return "data canged"
            else:raise HTTPException(status_code=404, detail="No email found")
        else:raise HTTPException(status_code=401, detail="Invalid Administrator")
    raise Exception("Something went wrong") #goes directly to internal server error exception
    
def isTokenValid(db: Session, admin=adminSchema.Administrator_MasterAdminToken):
    """cambiar esta funcion para buscar que el admin realmente este en la tabla"""
    if admin.token:
        tokenDict = __sc.decodeToken(admin.masterAdminToken)
        if __sc.validateToken(tokenDict["username"], tokenDict["level"], admin.masterAdminToken) == [True,True]:
            admin_user = db.query(Administrators_Table).filter(Administrators_Table.username==tokenDict['username']).first()
            if admin_user.username == tokenDict['username'] and admin_user.admin_level == tokenDict['level']:
                return True
            raise HTTPException(status_code=401, detail="Invalid Administrator")
        raise HTTPException(status_code=401,detail="Invalid Token")
    raise HTTPException(status_code=401,detail="No token received")