from sqlalchemy.orm import Session
from Backend.DATABASE.Administrators_Table import Administrators_Table
import Backend.SCHEMAS.Administrators_Schemas as adminSchema
from Backend.API.Security import Secuirity as sc
from pydantic import SecretStr

__sc = sc()
'''
    If working properly, functions to be moved elsewhere in the future.
'''

def getAdmins(db: Session, admin: adminSchema.Administrator_MasterAdminToken):
    tmp = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if tmp is None:
        raise Exception("No data was found")
    if __sc.validateToken(tmp[0],tmp[1],admin.masterAdminToken) == [True, True] and tmp[1] == "MA":
        entries = db.query(Administrators_Table).all()
        return [adminSchema.Administrator_GETTER(idAdministrators=entry.idadministrators,name=entry.name,userName=entry.username,password=entry.password,email=entry.email, phone=entry.phone,adminLevel=entry.admin_level, createdAt=entry.created_at, updatedAt=entry.updated_at) for entry in entries]
    raise Exception("No data was found")

def getAdminbyEmail(db: Session, email: str):
    return db.query(Administrators_Table).filter(Administrators_Table.email == email).first()
    
def getAdminbyUserName(db: Session, username: str):
    return db.query(Administrators_Table).filter(Administrators_Table.username == username).first()
    
def createAdmin(db: Session, admin: adminSchema.Administrator_CreateAccount_DB):
    tmp = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if tmp is None:
        return False
    if __sc.validateToken(tmp[0],tmp[1],admin.masterAdminToken) == [True, True] and tmp[1] == "MA":
        dbAdmin = Administrators_Table(name=admin.name, email=admin.email,phone=admin.phone, username=admin.userName, password=__sc.encryptHash(admin.passwd.get_secret_value()), admin_level=admin.adminLevel,created_at=admin.createdAt, updated_at=admin.updatedAt)
        db.add(dbAdmin)
        db.commit()
        db.refresh(dbAdmin)
        return True
    return False

def createMasterAdmin(db: Session, admin: adminSchema.Administrator_CreateAccount_DB):
        dbAdmin = Administrators_Table(name=admin.name, email=admin.email,phone=admin.phone, username=admin.userName, password=__sc.encryptHash(admin.passwd.get_secret_value()), admin_level=admin.adminLevel,created_at=admin.createdAt, updated_at=admin.updatedAt)
        db.add(dbAdmin)
        db.commit()
        db.refresh(dbAdmin)
        return True

#------------------------------------------------TOKEN FUNCTIONS
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
    """Validate username and password as well as token"""
    db_information = db.query(Administrators_Table.username, Administrators_Table.password, Administrators_Table.admin_level).filter(Administrators_Table.username == admin.userName).first()
    if db_information is not None and __sc.validateUsername(admin.userName, db_information[0]) and __sc.validateHash(admin.passwd.get_secret_value(), str(db_information[1])):
        if( admin.token == None):
            return [201, __sc.createToken({'username': admin.userName, 'admin_level':str(db_information[2])})]
        elif admin.token and __sc.validateToken(admin.userName,db_information[2],admin.token) == [True, True]:
            return [200, "Successful Authenticacion!"]
        elif admin.token and __sc.validateToken(admin.userName,db_information[2],admin.token) == [True, False]:
            return [201, __sc.createToken({'username': admin.userName, 'admin_level':db_information[2]})]
        elif admin.token and __sc.validateToken(admin.userName,db_information[2],admin.token) == [False, True]:
            return [401, "Invalid Token"]
    else:
        return [401, "Invalid Username or Password"]

def changeAdminPasswdEmail(db: Session, admin: adminSchema.Administrator_ChangePasswdEmail_DB):
    tmp = db.query(Administrators_Table.username,Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if tmp is None:
        return False
    if __sc.validateToken(tmp[0], tmp[1], admin.masterAdminToken) == [True, True] and tmp[1] == "MA":
        tmp = db.query(Administrators_Table.username, Administrators_Table.password, Administrators_Table.email).filter(admin.userName == Administrators_Table.username).first()
        if tmp is None:
            return False
        if admin.newPasswd != None and admin.newEmail != None and admin.newPhone != None:
            db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'password': __sc.encryptHash(admin.newPasswd.get_secret_value()), 'email':admin.newEmail, 'updated_at': admin.updatedAt, "phone": admin.newPhone})
        elif admin.newPasswd != None and admin.newPhone == None and admin.newEmail != None:
            db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'password': __sc.encryptHash(admin.newPasswd.get_secret_value()), 'email':admin.newEmail,'updated_at': admin.updatedAt})
        elif admin.newPasswd != None and admin.newPhone != None and admin.newEmail == None:
            db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'password': __sc.encryptHash(admin.newPasswd.get_secret_value()), "phone": admin.newPhone, 'updated_at': admin.updatedAt})
        elif admin.newPasswd == None and admin.newPhone != None and admin.newEmail != None:
            db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'email':admin.newEmail, 'updated_at': admin.updatedAt, "phone": admin.newPhone})
        elif admin.newPasswd != None and admin.newPhone == None and admin.newEmail != None:
            db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'email':admin.newEmail, 'updated_at': admin.updatedAt, "password": __sc.encryptHash(admin.newPasswd.get_secret_value())})
        elif admin.newPasswd == None and admin.newPhone == None and admin.newEmail != None:
            db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'email':admin.newEmail, 'updated_at': admin.updatedAt})
        elif admin.newPasswd == None and admin.newPhone != None and admin.newEmail == None:
            db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({'phone':admin.newPhone, 'updated_at': admin.updatedAt})
        else:
            return False
        db.commit()
        return True
    return False

# def changeAdminName(db: Session, admin: adminSchema.Administrator_ChangeName_DB):
#     tmp = db.query(Administrators_Table.name).filter(admin.userName == Administrators_Table.username).first()
#     if tmp is None:
#         return False
#     db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({"name": admin.name, "update_at": admin.updatedAt})
#     db.commit()
#     return True

# def changeAdminEmail(db: Session, admin: adminSchema.Administrator_ChangeEmail_DB):
#     tmp = db.query(Administrators_Table.email).filter(admin.userName == Administrators_Table.username).first()
#     if tmp is None:
#         return False
#     db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({"email": admin.name, "update_at": admin.updatedAt})
#     db.commit()
#     return True

# def changeAdminAll(db: Session, admin: adminSchema.Administrator_ChangeAll_DB):
#     if admin.masterAdminLevel == "MA" and admin.masterAdminLevel != None:
#         tmp = db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).first()
#         if tmp is None:
#             return False
#         db.query(Administrators_Table).filter(admin.userName == Administrators_Table.username).update({"password": __sc.encryptHash(admin.newPasswd.get_secret_value()), "name": admin.newName, "email": admin.newEmail, "admin_level": admin.newLevel, "updated_at": admin.updatedAt})
#         db.commit()
#         return True
#     return False

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

def deleteAdminAll(db:Session, admin: adminSchema.Administrator_MasterAdminToken):
    tmp = db.query(Administrators_Table.username, Administrators_Table.admin_level).filter(Administrators_Table.username == __sc.decodeToken(admin.masterAdminToken)['username']).first()
    if tmp is None:
        return False
    if __sc.validateToken(tmp[0],tmp[1],admin.masterAdminToken) == [True, True] and tmp[1] == "MA":
        db.query(Administrators_Table).filter(Administrators_Table.admin_level != "MA").delete()
        db.commit()
        return True
    return False
