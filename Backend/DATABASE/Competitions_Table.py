from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from Backend.CONFIG.connection import Base

class Competitions_Table(Base):
    """This class contains the code for the administrators table"""
    __tablename__ = 'competitions'

    #Creating the relation between the columns of each table
    idchapter_members = Column(Integer, ForeignKey('chapter_members.idchapter_members'))
    name = Column(String(55), ForeignKey('chapter_members.name'))
    email = Column(String(100), ForeignKey('chapter_members.email'))
    phone = Column(String(15), ForeignKey('chapter_memebers.phone'))
    chapter_members = relationship("chapter_members", backref="competitions")
    
    ascemembership = Column(Integer, unique=True, nullable=False)
    competition_name = Column(String(100), nullable=False)
    courses = Column(Text, nullable=False)
    daily_avail = Column(Text, nullable=False)
    travel_avail = Column(Enum('Yes','No'), nullable=False)
    age_gt_twtfive = Column(Enum('Yes','No'), nullable=False)
    offdriver_avail = Column(Enum('Yes','No'), nullable=False)
    competitions_form = Column(Enum('Yes','No'), nullable=False)


