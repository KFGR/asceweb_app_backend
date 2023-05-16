from sqlalchemy.orm import Session
from Backend.DATABASE.Competitions_Table import Competitions_Table
from Backend.SCHEMAS.Competitions_Schema import set_Competitions_Data
from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
from sqlalchemy import or_, exists
from fastapi import HTTPException


def ValidateExist(db:Session, user: set_Competitions_Data):
    """Returns false if user does not exist, else raise exception if username, phone or email exist"""
    db_profile = db.query(Competitions_Table).filter(or_(Competitions_Table.email == user.email, Competitions_Table.ascemembership == user.ascemembership)).first()
    if db_profile:
        print(type(db_profile.email), type(user.email))
        if db_profile.email == user.email:
            raise HTTPException(status_code=409, detail='Email already exist')
        if db_profile.ascemembership == user.ascemembership:
            raise  HTTPException(status_code=409, detail='ASCE membership already exist')
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