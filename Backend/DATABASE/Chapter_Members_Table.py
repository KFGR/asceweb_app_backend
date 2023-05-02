from sqlalchemy import Column, Integer, String, Enum, DATETIME
from sqlalchemy.orm import relationship
from Backend.CONFIG.connection import Base

class Chapter_Members_Table(Base):
    """This class represents the table that contains all the members of the student chapter"""
    _tablename_ = 'chapter_members'

    idchapter_members = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(55), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    tshirt_size = Column(Enum('S','M','L','XL'), nullable=False)
    age = Column(Integer, nullable=False)
    bachelor = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    type = Column(Enum('Member','Admin'), nullable=False) #Por defaul debe ser Members
    created_at = Column(DATETIME, nullable=False)
    competitions_form = Column(Enum('Yes','No'), nullable=False)

