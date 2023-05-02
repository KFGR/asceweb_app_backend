from sqlalchemy import Column, Integer, String, Enum, DATETIME
from sqlalchemy.orm import relationship
from Backend.CONFIG.connection import Base

class Administrators_Table(Base):
    """This class represents the table that contains all the members of the student chapter"""
    __tablename__ = 'administrators'

    idadministrators = Column(Integer,primary_key=True, autoincrement=True)

    name = Column(String(55), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(100), unique=True, nullable=False)
    admin_level = Column(Enum('MA','GA'), nullable=False)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)


