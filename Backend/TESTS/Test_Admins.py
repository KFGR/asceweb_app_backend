from sqlalchemy.orm import Session
from sqlalchemy import or_, exc
from Backend.DATABASE.Administrators_Table import Administrators_Table
from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
from Backend.DATABASE.Competitions_Table import Competitions_Table
import Backend.SCHEMAS.Administrators_Schemas as adminSchema
from Backend.API.Security import Secuirity as sc
import pydantic
from typing import Union
__sc = sc()
'''
    If working properly, functions to be moved elsewhere in the future.
'''

def getAdmins(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    """Function that returns the whole table of admins users"""
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    # print(admin_user or (__sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) != [True, True] and admin_user[1] != "MA"))
    print(admin_user)
    if admin_user and __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA":
        admins = db.query(Administrators_Table).all()
        if admins:
            return [adminSchema.Administrator_GETTER(idAdministrators=entry.idadministrators,name=entry.name,userName=entry.username,password=entry.password,email=entry.email, phone=entry.phone,adminLevel=entry.admin_level, createdAt=entry.created_at, updatedAt=entry.updated_at) for entry in admins]
        raise Exception("No data was found")
    raise Exception("Invalid Administrator")


def ValidateExist(db:Session,table: str, user: Union[adminSchema.Administrator_LoginAccount_DB, adminSchema.Member_upate_table, adminSchema.Competitions_upate_table]):
    """Returns false if user does not exist, else raise exception if username, phone or email exist"""
    if table == "admins":
        db_profile = db.query(Administrators_Table).filter(or_(Administrators_Table.email == user.email,Administrators_Table.username == user.userName,Administrators_Table.phone == user.phone)).first()
        if db_profile:
            if db_profile.username == user.userName:
                raise ValueError('Username already exist')
            if db_profile.email == user.email:
                raise ValueError('Email already exist')
            if db_profile.phone == user.phone:
                raise  ValueError('Phone already exist')
        return False
    elif table == "members":
        db_profile = db.query(Chapter_Members_Table).filter(or_(Chapter_Members_Table.idchapter_members == user.email,Chapter_Members_Table.email == user.userName,Chapter_Members_Table.phone == user.phone)).first()
        if db_profile:
            if db_profile.idchapter_members == user.idchapter_members:
                raise ValueError('Id already exist')
            if db_profile.email == user.email:
                raise ValueError('Email already exist')
            if db_profile.phone == user.phone:
                raise  ValueError('Phone already exist')
        return False
    elif table == "competitions":
        db_profile = db.query(Competitions_Table).filter(or_(Competitions_Table.idchapter_members == user.email,Competitions_Table.email == user.userName,Competitions_Table.phone == user.phone, Competitions_Table.ascemembership == user.ascemembership)).first()
        if db_profile:
            if db_profile.idchapter_members == user.idchapter_members:
                raise ValueError('Id already exist')
            if db_profile.email == user.email:
                raise ValueError('Email already exist')
            if db_profile.phone == user.phone:
                raise  ValueError('Phone already exist')
            if db_profile.ascemembership == user.ascemembership:
                raise  ValueError('ASCE membership already in use')
        return False
    raise Exception("Table {} does not exist").format(table)

# def ValidateExist(db:Session, user: adminSchema.Administrator_CreateAccount_INPUTS):
#     """Returns false if user does not exist, else raise exception if username, phone or email exist"""
#     db_profile = db.query(Administrators_Table).filter(or_(Administrators_Table.email == user.email,Administrators_Table.username == user.userName,Administrators_Table.phone == user.phone)).first()
#     if db_profile:
#         if db_profile.username == user.userName:
#             raise ValueError('Username already exist')
#         if db_profile.email == user.email:
#             raise ValueError('Email already exist')
#         if db_profile.phone == user.phone:
#             raise  ValueError('Phone already exist')
#     else:
#         return False


def createAdmin(db:Session, admin: adminSchema.Administrator_CreateAccount_DB):
    """Function used to create admin users, by first validating that the username, phone and email does not exist"""
    if not ValidateExist(db, table="admins", user=admin):
        admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
        if admin_user and __sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user.admin_level == 'MA':
            dbAdmin = Administrators_Table(name=admin.name, email=admin.email,phone=admin.phone, username=admin.userName, password=__sc.encryptHash(admin.passwd.get_secret_value()), admin_level=admin.adminLevel,created_at=admin.createdAt, updated_at=admin.updatedAt)
            db.add(dbAdmin)
            db.commit()
            db.refresh(dbAdmin)
            return True
        raise Exception('Invalid Administrator')
    raise Exception('Username, email or phone already exist')

"""
1. function to validate username and password
2. function to create token
3. function to validate token from frontend
   a. Get token
   b. Validate username and password from login
   c. Get username and verify username in database
   d. If token is expired, then create new token

"""

class HttpReturn():
    def __init__(self, status_code: int, detail: dict):
        self.status_code = status_code
        self.detail = detail


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

def updateAdmin(db: Session, admin: adminSchema.Administrator_ChangePasswdEmail_DB):
    """Function used to make updates in the administrators table, only available if the user making the changes is a MA"""
    admin_user = db.query(Administrators_Table.username, Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user:
        if __sc.validateToken(admin_user[0], admin_user[1], admin.masterAdminToken) == [True, True] and admin_user[1] == "MA":
            new_data = db.query(Administrators_Table).filter(Administrators_Table.username == admin.userName).first()
            if admin.newEmail != None:
                new_data.email = admin.newEmail
            if admin.newPasswd != None:
                new_data.password = __sc.encryptHash(admin.newPasswd.get_secret_value())
            if admin.newPhone != None:
                new_data.phone = admin.newPhone
            if admin.newLevel != None:
                new_data.admin_level = admin.newLevel
            new_data.updated_at = admin.updatedAt
            db.commit()
            db.refresh(new_data)
            return True
        raise Exception("Invalid Administrator")
    return False


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


"""
Get from chapter members table
"""
def get_SignUp_Table(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user and (__sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA"):
        members = db.query(Chapter_Members_Table).all()
        if members:
            return [adminSchema.get_SignUp_Data(idchapter_members=entry.idchapter_members,name=entry.name,email=entry.email,phone=entry.phone,tshirt_size=entry.tshirt_size,age=entry.age,bachelor=entry.bachelor,department=entry.department,type=entry.type,created_at=entry.created_at,competitions_form=entry.competitions_form,aca_years=entry.aca_years,membership_paid=entry.membership_paid,membership_until=entry.membership_until) for entry in members]
        raise Exception("No data was found")
    raise Exception("Invalid Administrator")

def updateMembers(db: Session, user=adminSchema. Member_upate_table):
    """Email, phone and id are unique"""
    pass

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

"""
Get from chapter competitions table
"""
def get_Competitions_Table(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    """Function that returns the whole table of admins users"""
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if admin_user and (__sc.validateToken(admin_user[0],admin_user[1],admin.masterAdminToken) == [True, True] and admin_user[1] == "MA"):
        admins = db.query(Competitions_Table).all()
        if admins:
            return [adminSchema.get_Competitions_Data(idchapter_members=entry.idchapter_members,name=entry.name,email=entry.email,phone=entry.phone,ascemembership=entry.ascemembership, competition_name=entry.competition_name,courses=entry.courses, daily_availability=entry.daily_avail, travel_availability=entry.travel_avail, older_than_twentyfive=entry.age_gt_twtfive,heavy_driver=entry.hv_vehicle,official_driver=entry.offdriver_avail,competitions_form=entry.competitions_form,created_at=entry.created_at) for entry in admins]
        raise Exception("No data was found")
    raise Exception("Invalid Administrator")

def updateCompetitionsMembers(db: Session, user=adminSchema. Member_upate_table):
    admin_user = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(user.masterAdminToken)['username']).first()
    if admin_user:
        pass
    else:
        raise Exception('No admin found')
    raise  Exception('No data was modified')

def delete_all_competitionsMember(db:Session, admin: adminSchema.Administrator_Delete_Entry_INPUTS):
    tmp = db.query(Administrators_Table.username, Administrators_Table.admin_level, Administrators_Table.email).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if tmp:
        if __sc.validateToken(tmp[0],tmp[1],admin.masterAdminToken) == [True, True] and tmp[1] == "MA" and tmp[2] == admin.email:
            db.query(Competitions_Table).delete()
            db.commit()
            return "Table was deleted"
        raise Exception("Invalid Administrator")
    raise Exception("No data was deleted")
    
    


# tmp = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
#     if tmp is None:
#         return False
#     if __sc.validateToken(tmp[0], tmp[1], admin.masterAdminToken) == [True, True] and tmp[1] == "MA":
#         tmp = db.query(Administrators_Table.username, Administrators_Table.password, Administrators_Table.email).filter(admin.userName == Administrators_Table.username).first()
#         if tmp is None:
#             return False
#         if admin.newPasswd != None and admin.newEmail != None and admin.newPhone != None:
#             db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'password': __sc.encryptHash(admin.newPasswd.get_secret_value()), 'email':admin.newEmail, 'updated_at': admin.updatedAt, "phone": admin.newPhone})
#         elif admin.newPasswd != None and admin.newPhone == None and admin.newEmail != None:
#             db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'password': __sc.encryptHash(admin.newPasswd.get_secret_value()), 'email':admin.newEmail,'updated_at': admin.updatedAt})
#         elif admin.newPasswd != None and admin.newPhone != None and admin.newEmail == None:
#             db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'password': __sc.encryptHash(admin.newPasswd.get_secret_value()), "phone": admin.newPhone, 'updated_at': admin.updatedAt})
#         elif admin.newPasswd == None and admin.newPhone != None and admin.newEmail != None:
#             db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'email':admin.newEmail, 'updated_at': admin.updatedAt, "phone": admin.newPhone})
#         elif admin.newPasswd != None and admin.newPhone == None and admin.newEmail != None:
#             db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'email':admin.newEmail, 'updated_at': admin.updatedAt, "password": __sc.encryptHash(admin.newPasswd.get_secret_value())})
#         elif admin.newPasswd == None and admin.newPhone == None and admin.newEmail != None:
#             db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'email':admin.newEmail, 'updated_at': admin.updatedAt})
#         elif admin.newPasswd == None and admin.newPhone != None and admin.newEmail == None:
#             db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'phone':admin.newPhone, 'updated_at': admin.updatedAt})
#         else:
#             return False
#         db.commit()
#         return True
#     return False