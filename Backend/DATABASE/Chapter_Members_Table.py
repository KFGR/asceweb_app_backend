from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DATETIME
from sqlalchemy.orm import relationship
from Backend.CONFIG.connection import Base
from sqlalchemy.dialects.mysql import INTEGER
from Backend.DATABASE.Competitions_Table import Competitions_Table
class Chapter_Members_Table(Base):
    """This class represents the table that contains all the members of the student chapter"""
    __tablename__ = 'chapter_members'

    idchapter_members = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
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
    aca_years = Column(Integer, nullable=False)
    membership_paid = Column(Enum('Yes','No'), nullable=False)
    membership_until = Column(String, nullable=False)
    competitions = relationship("Competitions_Table", backref='chapter_members', foreign_keys=[Competitions_Table.idchapter_members, Competitions_Table.name, Competitions_Table.email, Competitions_Table.phone], primaryjoin="and_(Chapter_Members_Table.idchapter_members==Competitions_Table.idchapter_members, Chapter_Members_Table.name==Competitions_Table.name, Chapter_Members_Table.email==Competitions_Table.email, Chapter_Members_Table.phone==Competitions_Table.phone)")
