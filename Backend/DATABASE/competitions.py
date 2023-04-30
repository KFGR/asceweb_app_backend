from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from Backend.CONFIG.connection import Base

class competitions(Base):
    """This class contains the code for the administrators table"""
    __tablename__ = 'competitions'

    #Creating the relation between the columns of each table
    idchapter_members = Column(Integer, ForeignKey('chapter_members.idchapter_members'))
    chapter_members = relationship("chapter_members", backref="competitions")
    name = Column(String(55), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    ascemembership = Column(Integer, unique=True, nullable=False)
    competition_name = Column(String(100), nullable=False)
    courses = Column(Text, nullable=False)
    daily_avail = Column(Text, nullable=False)
    travel_avail = Column(Enum('Yes','No'), nullable=False)
    age_gt_twtfive = Column(Enum('Yes','No'), nullable=False)
    offdriver_avail = Column(Enum('Yes','No'), nullable=False)
    competitions_form = Column(Enum('Yes','No'), nullable=False)


