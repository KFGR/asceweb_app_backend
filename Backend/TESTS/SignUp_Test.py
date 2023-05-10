from sqlalchemy.orm import Session
from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
from Backend.SCHEMAS.SignUp_Schemas import set_SignUp_Data, get_SignUp_Data



def put_SignUp_Data(db: Session, user: set_SignUp_Data):
    email_exists = db.query(Chapter_Members_Table.email).filter(Chapter_Members_Table.email == user.email).first()
    if email_exists:
        print(email_exists)
        raise ValueError('Email already exists')
    
    db_members = Chapter_Members_Table(name=user.name, email=user.email, phone=user.phone, tshirt_size=user.tshirt_size, age=user.age, bachelor=user.bachelor, department=user.department, type=user.type, created_at=user.created_at, competitions_form=user.competitions_form, aca_years = user.aca_years)
    db.add(db_members)
    db.commit()
    db.refresh(db_members)
    return [200, 'Congrats {} you are now part of the ASCE PUPR Student Chapter'.format(user.name)]


def get_SignUp_Table(db: Session):
    return db.query(Chapter_Members_Table.idchapter_members, Chapter_Members_Table.name,Chapter_Members_Table.email,Chapter_Members_Table.phone,Chapter_Members_Table.tshirt_size,Chapter_Members_Table.age,Chapter_Members_Table.bachelor,Chapter_Members_Table.department,Chapter_Members_Table.type,Chapter_Members_Table.created_at,Chapter_Members_Table.competitions_form, Chapter_Members_Table.aca_years).all()