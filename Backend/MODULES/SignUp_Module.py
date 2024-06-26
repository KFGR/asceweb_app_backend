from sqlalchemy.orm import Session
from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
from Backend.SCHEMAS.SignUp_Schemas import set_SignUp_Data
from sqlalchemy import or_
from fastapi import HTTPException
    
def validateUsername(email: str):
    username = email.split('@')[0]
    if len(username.split('_')) == 2:
        username = email.split('@')[0]
    if len(username.split('_')) == 2:
        username_name, username_number = username.split('_')
        if not username_name.isalpha(): 
            raise ValueError("Username name only contains letters")
        if not username_number.isdigit():
            raise ValueError("Username number only contains numbers")
        return int(username_number)
    raise ValueError("Invalid email username")

def ValidateExist(db:Session, user: set_SignUp_Data):
    """Returns false if user does not exist, else raise exception if username, phone or email exist"""
    db_profile = db.query(Chapter_Members_Table).filter(or_(Chapter_Members_Table.email == user.email,Chapter_Members_Table.phone == user.phone)).first()
    if db_profile:
        if db_profile.email == user.email:
            raise HTTPException(status_code=409, detail='Email already exist')
        if db_profile.phone == user.phone:
            raise  HTTPException(status_code=409, detail='Phone already exist')
    else:
        return False
    

def put_SignUp_Data(db: Session, user: set_SignUp_Data):
    if not ValidateExist(db,user=user):
        db_members = Chapter_Members_Table(idchapter_members=validateUsername(user.email),name=user.name, email=user.email, phone=user.phone, tshirt_size=user.tshirt_size, age=user.age, bachelor=user.bachelor, department=user.department, type=user.type, created_at=user.created_at, competitions_form=user.competitions_form, aca_years = user.aca_years, membership_paid=user.membership_paid, membership_until=user.membership_until)
        db.add(db_members)
        db.commit()
        db.refresh(db_members)
        return "Congrats {} you are now a member of the ASCE-PUPR student chapter".format(user.name)
    raise HTTPException(status_code=409, detail="Already in list of competition")
    
# def put_SignUp_Data(db: Session, user: set_SignUp_Data):
#     if not ValidateExist(db,user=user):
#         db_members = Chapter_Members_Table(name=user.name, email=user.email, phone=user.phone, tshirt_size=user.tshirt_size, age=user.age, bachelor=user.bachelor, department=user.department, type=user.type, created_at=user.created_at, competitions_form=user.competitions_form, aca_years = user.aca_years, membership_paid=user.membership_paid, membership_until=user.membership_until)
#         db.add(db_members)
#         db.commit()
#         db.refresh(db_members)
#         return "Congrats {} you are now a member of the ASCE-PUPR student chapter".format(user.name)
#     raise HTTPException(status_code=409, detail="Already in list of competition")