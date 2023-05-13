from sqlalchemy.orm import Session
from sqlalchemy import or_, exc
from Backend.DATABASE.Administrators_Table import Administrators_Table
from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
from Backend.DATABASE.Competitions_Table import Competitions_Table
import Backend.SCHEMAS.Administrators_Schemas as adminSchema
from Backend.API.Security import Secuirity as sc
from fastapi import HTTPException
from typing import Union
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
                raise HTTPException(status_code=422, detail='Username already exist')
            if db_profile.email == user.email:
                raise HTTPException(status_code=422, detail='Email already exist')
            if db_profile.phone == user.phone:
                raise  HTTPException(status_code=422, detail='Phone already exist')
        return False
    elif table == "UpdateAdmin":
        db_profile = db.query(Administrators_Table).filter(or_(Administrators_Table.email == user.newEmail,Administrators_Table.username == user.userName,Administrators_Table.phone == user.newPhone)).first()
        if db_profile:
            if db_profile.email == user.newEmail:
                raise HTTPException(status_code=422, detail='Email already exist')
            if db_profile.phone == user.newPhone:
                raise  HTTPException(status_code=422, detail='Phone already exist')
        return False
    elif table == "UpdateChapterMember":
        db_profile = db.query(Chapter_Members_Table).filter(or_(Chapter_Members_Table.idchapter_members == user.email,Chapter_Members_Table.email == user.userName,Chapter_Members_Table.phone == user.phone)).first()
        if db_profile:
            if db_profile.email == user.newEmail:
                raise HTTPException(status_code=422, detail='Email already exist')
            if db_profile.phone == user.newPhone:
                raise  HTTPException(status_code=422, detail='Phone already exist')
        return False
    elif table == "UpdateCompetitionsSignUp":
        db_profile = db.query(Competitions_Table).filter(or_(Competitions_Table.idchapter_members == user.email,Competitions_Table.email == user.userName,Competitions_Table.phone == user.phone)).first()
        if db_profile:
            if db_profile.email == user.newEmail:
                raise HTTPException(status_code=422, detail='Email already exist')
            if db_profile.phone == user.newPhone:
                raise  HTTPException(status_code=422, detail='Phone already exist')
        return False
    raise Exception("Table {} does not exist").format(table)



def createAdmin(db:Session, admin: adminSchema.Administrator_CreateAccount_DB):
    """Function used to create admin users, by first validating that the username, phone and email does not exist"""
    if not ValidateExist(db, table="CreateAdmin", user=admin):
        admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
        if admin_user and __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user.admin_level == 'MA':
            dbAdmin = Administrators_Table(name=admin.name, email=admin.email,phone=admin.phone, username=admin.userName, password=__sc.encryptHash(admin.passwd.get_secret_value()), admin_level=admin.adminLevel,created_at=admin.createdAt, updated_at=admin.updatedAt)
            db.add(dbAdmin)
            db.commit()
            db.refresh(dbAdmin)
            return True
        raise Exception('Invalid Administrator')
    raise Exception('Username, email or phone already exist')


def loginAdmin(db: Session, admin: adminSchema.Administrator_LoginAccount_DB) -> list:
    """Validate username and password as well as token to return either an invalid login or valid login"""
    db_information = db.query(Administrators_Table.username, Administrators_Table.password, Administrators_Table.admin_level).filter(Administrators_Table.username == admin.userName).first()
    if db_information is not None and __sc.validateUsername(admin.userName, db_information[0]) and __sc.validateHash(admin.passwd.get_secret_value(), str(db_information[1])):
        if( admin.token == None):
            return [201, __sc.createToken({'username': admin.userName, 'admin_level':str(db_information[2])})]
        elif admin.token and __sc.validateToken(admin.userName,db_information[2],admin.token) == [True, True]:
            return [200, "Successful Authenticacion!"]
        elif admin.token and __sc.validateToken(admin.userName,db_information[2],admin.token) == [True, False]:
            return [201, __sc.createToken({'username': admin.userName, 'admin_level':db_information[2]})]
        elif admin.token and __sc.validateToken(admin.userName,db_information[2],admin.token) == [False, True]:
            return [401, "Unauthorized"]
    else:
        return [401, "Invalid Username or Password"]



def getAdmins(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    """Function that returns the whole table of admins users"""
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user:
        if __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA":
            admins = db.query(Administrators_Table).all()
            if admins:
                return [adminSchema.Administrator_GETTER(idAdministrators=entry.idadministrators,name=entry.name,userName=entry.username,password=entry.password,email=entry.email, phone=entry.phone,adminLevel=entry.admin_level, createdAt=entry.created_at, updatedAt=entry.updated_at) for entry in admins]
            raise HTTPException(status_code=400, detail="No data was found")
        raise HTTPException(status_code=401, detail="Invalid Administrator")
    raise HTTPException(status_code=404, detail="No user found")

def get_SignUp_Table(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user and (__sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA"):
        members = db.query(Chapter_Members_Table).all()
        if members:
            return [adminSchema.get_SignUp_Data(idchapter_members=entry.idchapter_members,name=entry.name,email=entry.email,phone=entry.phone,tshirt_size=entry.tshirt_size,age=entry.age,bachelor=entry.bachelor,department=entry.department,type=entry.type,created_at=entry.created_at,competitions_form=entry.competitions_form,aca_years=entry.aca_years,membership_paid=entry.membership_paid,membership_until=entry.membership_until) for entry in members]
        raise Exception("No data was found")
    raise Exception("Invalid Administrator")

def get_Competitions_Table(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    """Function that returns the whole table of admins users"""
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user and (__sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA"):
        admins = db.query(Competitions_Table).all()
        if admins:
            return [adminSchema.get_Competitions_Data(idchapter_members=entry.idchapter_members,name=entry.name,email=entry.email,phone=entry.phone,asce_member=entry.asce_member,ascemembership=entry.ascemembership, competition_name=entry.competition_name,courses=entry.courses, daily_availability=entry.daily_avail, experiences=entry.experiences, travel_availability=entry.travel_avail, travel_june=entry.travel_june, older_than_twentyfive=entry.age_gt_twtfive,heavy_driver=entry.hv_vehicle,official_driver=entry.offdriver_avail,competitions_form=entry.competitions_form,created_at=entry.created_at) for entry in admins]
        raise HTTPException(status_code=404, detail="No data was found")
    raise HTTPException(status_code=401, detail="Invalid Administrator")



def delete_all_Members(db:Session, admin: adminSchema.Administrator_Delete_Entry_INPUTS):
    tmp = db.query(Administrators_Table.username, Administrators_Table.admin_level, Administrators_Table.email).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if tmp:
        if __sc.validateToken(tmp[0],tmp[1],admin.masterAdminToken) == [True, True] and tmp[1] == "MA" and tmp[2] == admin.email:
            db.query(Chapter_Members_Table).delete()
            db.commit()
            return "Table was deleted"
        else:
            raise Exception("Invalid Administrator")
    raise Exception("No data was deleted")

def delete_all_competitionsMember(db:Session, admin: adminSchema.Administrator_Delete_Entry_INPUTS):
    tmp = db.query(Administrators_Table.username, Administrators_Table.admin_level, Administrators_Table.email).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if tmp:
        if __sc.validateToken(tmp[0],tmp[1],admin.masterAdminToken) == [True, True] and tmp[1] == "MA" and tmp[2] == admin.email:
            db.query(Competitions_Table).delete()
            db.commit()
            return "Table was deleted"
        raise Exception("Invalid Administrator")
    raise Exception("No data was deleted")

def deleteAdminEntry(db: Session, admin: adminSchema.Administrator_Delete_Entry_INPUTS):
    tmp = db.query(Administrators_Table.username,Administrators_Table.admin_level, Administrators_Table.email).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if tmp is None:
        return False
    
    if __sc.validateToken(tmp[0], tmp[1], admin.masterAdminToken) == [True, True] and tmp[1] == "MA" and tmp[2] != admin.email:
        tmp = db.query(Administrators_Table).filter(admin.email == Administrators_Table.email).first()
        if tmp is None:
            return False
        db.query(Administrators_Table).filter(admin.email == Administrators_Table.email).delete()
        db.commit()
        return True
    return False

def delete_all_Members(db:Session, admin: adminSchema.Administrator_Delete_Entry_INPUTS):
    tmp = db.query(Administrators_Table.username, Administrators_Table.admin_level, Administrators_Table.email).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if tmp:
        if __sc.validateToken(tmp[0],tmp[1],admin.masterAdminToken) == [True, True] and tmp[1] == "MA" and tmp[2] == admin.email:
            db.query(Administrators_Table).delete()
            db.commit()
            return "Table was deleted"
        raise Exception("Invalid Administrator")
    raise Exception("No data was deleted")



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

def updateCompetitionsMembers(db: Session, user=adminSchema.Member_upate_table):
    if not ValidateExist(db=db,table="UpdateCompetitionsSignUp", user=user):
        admin_user = db.query(Administrators_Table.username, Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(user.masterAdminToken)['username']).first()
        if admin_user and __sc.validateToken(admin_user[0], admin_user[1], user.masterAdminToken) == [True, True] and admin_user[1] == "MA":
            user_row = db.query(Administrators_Table).filter(Administrators_Table.username == user.userName).first()
            if user_row:
                if not (user.newEmail or user.newPasswd or user.newPhone or user.newLevel):
                    raise HTTPException(status_code=204, detail="No data was changed")
                
                if user.newEmail is not None:
                    if user.newEmail != user_row.email:
                        user_row.email = user.newEmail
                    else: raise HTTPException(status_code=409, detail="This user is already using this email")

                if user.newPasswd is not None:
                    if not __sc.validateHash(user.newPasswd.get_secret_value(),user_row.password):
                        user_row.password = __sc.encryptHash(user.newPasswd.get_secret_value())
                    else: raise HTTPException(status_code=409, detail="Cannot use the same password")

                if user.newPhone is not None:
                    if user.newPhone != user_row.phone:
                        user_row.phone = user.newPhone
                    else: raise HTTPException(status_code=409, detail="This user is already using this phone number")
                
                if user.newLevel is not None:
                    if user.newLevel != user_row.admin_level:
                        user_row.admin_level = user.newLevel
                    else: raise HTTPException(status_code=409, detail="This user is already this administrator level")
                
                user_row.updated_at = user.updatedAt
                db.commit()
                db.refresh(user_row)
                return True
            else:raise HTTPException(status_code=404, detail="No username found")
        else:raise HTTPException(status_code=401, detail="Invalid Administrator")
    raise Exception("Something went wrong") #goes directly to internal server error exception

"""
email
phone
tshirt_size
age
bachelor
department
aca_years
membership_paid
"""
def updateMembers(db: Session, user=adminSchema.Member_upate_table):
    """Email, phone and id are unique"""
    if not ValidateExist(db=db,table="UpdateCompetitionsSignUp", user=user):
        admin_user = db.query(Administrators_Table.username, Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(user.masterAdminToken)['username']).first()
        if admin_user and __sc.validateToken(admin_user[0], admin_user[1], user.masterAdminToken) == [True, True] and admin_user[1] == "MA":
            user_row = db.query(Chapter_Members_Table).filter(Chapter_Members_Table.email == user.email).first()
            if user_row:
                if not (user.newEmail or user.newPhone or user.newTshirt_size or user.newAge or user.newBachelor or user.newDepartment or user.newAca_years or user.newMembership):
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
                    else: raise HTTPException(status_code=409, detail="This user is already using this phone number")
                
                if user.newLevel is not None:
                    if user.newLevel != user_row.admin_level:
                        user_row.admin_level = user.newLevel
                    else: raise HTTPException(status_code=409, detail="This user is already this administrator level")
                
                user_row.updated_at = user.updatedAt
                db.commit()
                db.refresh(user_row)
                return True
            else:raise HTTPException(status_code=404, detail="No username found")
        else:raise HTTPException(status_code=401, detail="Invalid Administrator")
    raise Exception("Something went wrong") #goes directly to internal server error exception
    