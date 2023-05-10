from pydantic import BaseModel as Schema, ValidationError, validator, root_validator, EmailStr, SecretStr
from datetime import datetime
import pytz
from typing import Any


class __Members_Inputs(Schema):
    """Private class to validate all inputs from the signup form"""
    name: str
    email: EmailStr
    phone: str
    tshirt_size: str
    age: int
    bachelor: str
    department: str
    aca_years: int

    @validator('*', allow_reuse=True, pre=True)
    def isEmpty(cls, value: str | datetime):
        if type(value) is str and (value == "" or value == None):
            raise ValueError("None of the Fields can be empty!")
        return value
    
    @validator('name', allow_reuse=True)
    def isName(cls, value: str):
     if any(v[0].islower() for v in value.split()):
         raise ValueError("All parts of any name should contain upper - case characters.")
     if any(not v.isalpha() and not v.isspace() for v in value):
         raise ValueError("A name only contains letters.")
     return value
    
    @validator('email', allow_reuse=True)
    def validate_email(cls, value: EmailStr):
        email_domain = value.split('@')[1]
        if email_domain not in ('pupr.edu', 'students.pupr.edu'):
            raise ValidationError("Invalid email")
        return value
    
    @validator('age', allow_reuse=True)
    def validate_age(cls, value:int):
        if value < 15:
            raise ValidationError('Age should be greater than 15')
        return value
    
    @validator('phone', allow_reuse=True)
    def validate_phone(cls, value: str):
        phone_pattern = set('!@#$%^&*()_+-=`~<>,.?/:;"{}[]\'')
        if any(char in phone_pattern for char in value):
            raise ValidationError('Invalid phone number')
        return "{}-{}-{}".format(value[:3],value[3:6],value[6:])
    



    
class set_SignUp_Data(__Members_Inputs):
    """Setter to be used to enter signup data to database"""
    type: str = "Member"
    created_at: datetime = datetime.now(pytz.timezone('America/Puerto_Rico'))
    competitions_form: str = "No"

    class Config:
        orm_mode = True

class get_SignUp_Data(Schema):
    """Getter to be used to return signup data from database"""
    name: str
    email: EmailStr
    phone: str
    tshirt_size: str
    age: int
    bachelor: str
    department: str
    type: str 
    created_at: datetime
    competitions_form: str
    aca_years: int

    class Config:
            orm_mode = True

class output_Schema(Schema):
    status_code: Any
    body: Any


class output(Schema):
    status_code: Any
    body: Any
