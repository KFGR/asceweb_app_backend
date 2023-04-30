from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from Backend.CONFIG.connection import Base

class administrators(Base):
    """This class represents the table that contains all the members of the student chapter"""
    __tablename__ = 'administrators'

    idadministrators = Column(Integer,primary_key=True, autoincrement=True)
    #Creating the relation between the columns of each table
    idchapter_members = Column(Integer, ForeignKey('chapter_members.idchapter_members'))
    chapter_members = relationship("chapter_members", backref="administrators")

    name = Column(String(55), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(100), unique=True, nullable=False)
    admin_level = Column(Enum('MA','GA'), nullable=False)
    created_at = Column(DateTime, nullable=False)


