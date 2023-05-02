from sqlalchemy.orm import Session
from Backend.DATABASE.Administrators_Table import Administrators_Table
import Backend.SCHEMAS.Administrators_Schemas as adminSchema
from Backend.API.Security import Secuirity as sc

__sc = sc()
'''
    If working properly, functions to be moved elsewhere in the future.
'''

def getAdmins(db: Session):
    entries = db.query(Administrators_Table).all()
    return [adminSchema.Administrator_LookAccount_OUT(idAdministrators=entry.idadministrators,name=entry.name,userName=entry.username,password=entry.password,email=entry.email,adminLevel=entry.admin_level, createdAt=entry.created_at, updatedAt=entry.updated_at) for entry in entries]

def getAdminbyEmail(db: Session, email: str):
    return db.query(Administrators_Table).filter(Administrators_Table.email == email).first()

def getAdminbyUserName(db: Session, username: str):
    return db.query(Administrators_Table).filter(Administrators_Table.username == username).first()

def createAdmin(db: Session, admin: adminSchema.Administrator_CreateAccount_OUT):
    dbAdmin = Administrators_Table(name=admin.name, email=admin.email, username=admin.userName.get_secret_value(), password=__sc.encrypt(admin.passwd.get_secret_value()), admin_level=admin.adminLevel,created_at=admin.createdAt, updated_at=admin.updatedAt)
    db.add(dbAdmin)
    db.commit()
    db.refresh(dbAdmin)
    return admin

def loginAdmin(db: Session, admin: adminSchema.Administrator_LoginAccount_OUT) -> bool:
    entries = db.query(Administrators_Table).all()
    for entry in entries:
        if(__sc.verify(admin.passwd.get_secret_value(),entry.password) == True):
            return True
    return False