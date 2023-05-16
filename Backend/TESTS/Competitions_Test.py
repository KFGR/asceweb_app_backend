from sqlalchemy.orm import Session
from Backend.DATABASE.Competitions_Table import Competitions_Table
from Backend.SCHEMAS.Competitions_Schema import set_Competitions_Data
from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
from sqlalchemy import or_, exists
from fastapi import HTTPException

# def put_Competition_Dataa(db: Session, user: set_Competitions_Data):
#     # db_user = db.query(Chapter_Members_Table).filter(email= user.email, phone = user.phone).first()
#     db_user = db.query(Chapter_Members_Table).filter(or_(Chapter_Members_Table.email == user.email, Chapter_Members_Table.phone == user.phone)).first()
#     # print("db_query",bool(db.query(Competitions_Table).filter(or_(Competitions_Table.email == user.email, Competitions_Table.phone == user.phone)).first()))
#     print(db_user)
#     print('hola')
#     if db_user:
#         if db_user.email == user.email:
#             raise Exception('Email already exists')
#         if db_user.phone == user.phone:
#             raise Exception('Phone already exists')
#     else:
#         print("nope")
#         # db_members = Competitions_Table(name=user.name, email=user.email, phone=user.phone, tshirt_size=user.tshirt_size, age=user.age, bachelor=user.bachelor, department=user.department, type=user.type, created_at=user.created_at, competitions_form=user.competitions_form, aca_years = user.aca_years)
#         # db.add(db_members)
#         # db.commit()
#         # db.refresh(db_members)
#         # return 'Congrats {} you are now part of the ASCE PUPR Student Chapter'.format(user.name)
#     return False
def ValidateExist(db:Session, user: set_Competitions_Data):
    """Returns false if user does not exist, else raise exception if username, phone or email exist"""
    db_profile = db.query(Competitions_Table).filter(or_(Competitions_Table.email == user.email,Competitions_Table.phone == user.phone, Competitions_Table.ascemembership == user.ascemembership)).first()
    if db_profile:
        print(type(db_profile.email), type(user.email))
        if db_profile.email == user.email:
            raise HTTPException(status_code=422, detail='Email already exist')
        if db_profile.ascemembership == user.ascemembership:
            raise  HTTPException(status_code=422, detail='ASCE membership already exist')
    else:
        return False
    
def put_Competition_Data(db:Session, user:set_Competitions_Data):
    """
    1. Validates that the user exists in chapter_members table
    2. Validates that the user in chapter_members table column is not Yes: creates the user in competitions table, else raise exception to let know the user that it is already registered
    3. Validates that the competitions form is not Yes: creates the competitions form in competitions form table, else raise exception to let know the competitions form that is already registered
    """
    if not ValidateExist(db,user=user):
        member_exist = db.query(Chapter_Members_Table).filter(Chapter_Members_Table.name == user.name, Chapter_Members_Table.email == user.email).first()
        print(member_exist.email)
        if member_exist and member_exist.competitions_form != 'Yes' and member_exist.name == user.name and member_exist.email == user.email:        
            db_competitions = Competitions_Table(idchapter_members=member_exist.idchapter_members, name=member_exist.name, email=member_exist.email,phone=member_exist.phone, ascemembership=user.ascemembership, courses=user.courses, daily_avail=user.daily_availability, travel_avail=user.travel_availability,age_gt_twtfive=user.older_than_twentyfive, hv_vehicle=user.heavy_driver, offdriver_avail=user.official_driver, competitions_form=user.competitions_form, competition_name=user.competition_name, created_at=user.created_at, experiences=user.experiences, travel_june=user.travel_june, asce_member=user.asce_member)
            db.add(db_competitions)
            db.commit()
            db.refresh(db_competitions)
            member_exist.competitions_form = 'Yes'
            db.commit()
            db.refresh(member_exist)
            return "Congrats {} you are now in list to participate for a competition.".format(user.name)
        raise HTTPException(status_code=404, detail="No member found")
    raise HTTPException(status_code=409, detail="Already in list of competition")