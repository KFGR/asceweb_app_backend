# from sqlalchemy.orm import Session
# from Backend.DATABASE.Competitions_Table import Competitions_Table
# from Backend.SCHEMAS.Competitions_Schema import set_Competitions_Data
# from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
# from sqlalchemy import or_


# def put_Competition_Data(db: Session, user: set_Competitions_Data):
#     # db_user = db.query(Chapter_Members_Table).filter(email= user.email, phone = user.phone).first()
#     db_user = db.query(Chapter_Members_Table).filter(or_(Chapter_Members_Table.email == user.email, Chapter_Members_Table.phone == user.phone)).first()

#     print(db_user)
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

