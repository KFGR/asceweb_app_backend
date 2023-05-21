# from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text, DATETIME
# from sqlalchemy.orm import relationship
# from Backend.CONFIG.connection import Base
# from sqlalchemy.dialects.mysql import INTEGER
# # from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
# class Competitions_Table(Base):
#     """This class contains the code for the administrators table"""
#     __tablename__ = 'competitions'

#     #Creating the relation between the columns of each table
#     idchapter_members = Column(INTEGER(unsigned=True),  ForeignKey('chapter_members.idchapter_members'),primary_key=True)
#     name = Column(String(55), ForeignKey('chapter_members.name'))
#     email = Column(String(100), ForeignKey('chapter_members.email'))
#     phone = Column(String(15), ForeignKey('chapter_members.phone'))

#     ascemembership = Column(String, unique=True, nullable=False)
#     competition_name = Column(String(100), nullable=False)
#     courses = Column(Text, nullable=False)
#     daily_avail = Column(Text, nullable=False)
#     experiences = Column(Text, nullable=False)
#     asce_member = Column(Enum('Yes','No'), nullable=False)
#     travel_avail = Column(Enum('Yes','No'), nullable=False)
#     travel_june = Column(Enum('Yes','No'), nullable=False)
#     age_gt_twtfive = Column(Enum('Yes','No'), nullable=False)
#     hv_vehicle = Column(Enum('Yes','No'), nullable=False)
#     offdriver_avail = Column(Enum('Yes','No'), nullable=False)
#     competitions_form = Column(Enum('Yes','No'), nullable=False)
#     created_at = Column(DATETIME, nullable=False)



from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text, DATETIME, Index
from sqlalchemy.orm import relationship
from Backend.CONFIG.connection import Base
from sqlalchemy.dialects.mysql import INTEGER
# from Backend.DATABASE.Chapter_Members_Table import Chapter_Members_Table
class Competitions_Table(Base):
    """This class contains the code for the administrators table"""
    __tablename__ = 'competitions'

    #Creating the relation between the columns of each table
    idchapter_members = Column(INTEGER(display_width=6,unsigned=True),  ForeignKey('chapter_members.idchapter_members'),primary_key=True)
    name = Column(String(55))
    email = Column(String(100), ForeignKey('chapter_members.email'))
    phone = Column(String(15), ForeignKey('chapter_members.phone'))

    ascemembership = Column(String(50), unique=True, nullable=False)
    competition_name = Column(String(100), nullable=False)
    courses = Column(Text, nullable=False)
    daily_avail = Column(Text, nullable=False)
    experiences = Column(Text, nullable=False)
    asce_member = Column(Enum('Yes','No'), nullable=False)
    travel_avail = Column(Enum('Yes','No'), nullable=False)
    travel_june = Column(Enum('Yes','No'), nullable=False)
    age_gt_twtfive = Column(Enum('Yes','No'), nullable=False)
    hv_vehicle = Column(Enum('Yes','No'), nullable=False)
    offdriver_avail = Column(Enum('Yes','No'), nullable=False)
    competitions_form = Column(Enum('Yes','No'), nullable=False)
    created_at = Column(DATETIME, nullable=False)
    # chapter_member = relationship("Chapter_Members_Table", backref="competitions")
    # __table_args__ = (
    #     Index('idx_chapter_members_fk', name, email, phone),
    # )





