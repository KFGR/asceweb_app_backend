from sqlalchemy.orm import Session
from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
from Backend.SCHEMAS.SignUp_Schemas import set_SignUp_Data
from sqlalchemy import or_


def ValidateExist(db:Session, user: set_SignUp_Data):
    """Returns false if user does not exist, else raise exception if username, phone or email exist"""
    db_profile = db.query(Chapter_Members_Table).filter(or_(Chapter_Members_Table.email == user.email,Chapter_Members_Table.phone == user.phone)).first()
    if db_profile:
        print(type(db_profile.email), type(user.email))
        if db_profile.email == user.email:
            raise ValueError('Email already registered')
        if db_profile.phone == user.phone:
            raise  ValueError('Phone already registered')
    else:
        return False

def put_SignUp_Data(db: Session, user: set_SignUp_Data):
    if not ValidateExist(db,user=user):
        db_members = Chapter_Members_Table(name=user.name, email=user.email, phone=user.phone, tshirt_size=user.tshirt_size, age=user.age, bachelor=user.bachelor, department=user.department, type=user.type, created_at=user.created_at, competitions_form=user.competitions_form, aca_years = user.aca_years, membership_paid=user.membership_paid, membership_until=user.membership_until)
        db.add(db_members)
        db.commit()
        db.refresh(db_members)
        return 'Congrats {} you are now part of the ASCE PUPR Student Chapter'.format(user.name)
    raise Exception("Already registered in a the student chapter")