from pydantic import BaseModel as Schema, ValidationError, validator, root_validator, EmailStr, SecretStr
from datetime import datetime
import pytz
from typing import Any


class __Members_Inputs(Schema):
    """Private class to validate all inputs from the signup form"""
    name: str
    email: str
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
     if len(value.split()) != 2:
         raise ValueError("Name must contain only one firstname and one lastname")
     if value[0].isspace() or value[-1].isspace():
         raise ValueError("No spaces allowed at the beginning or end of name")
     if any(v[0].islower() for v in value.split()):
         raise ValueError("All parts of any name should contain upper - case characters.")
     if any(not v.isalpha() and not v.isspace() for v in value):
         raise ValueError("A name only contains letters.")
     return value
    
    @validator('email', allow_reuse=True)
    def validate_email(cls, value: str):
        if " " in value:
            raise ValueError("No spaces allowed on email")
        if value.lower() != value:
            raise ValueError("The email must be in lower - case.")
        email_domain = value.split('@')[1]
        if email_domain != 'students.pupr.edu':
            raise ValueError("Invalid email")
        return value
    
    @validator('phone', allow_reuse=True)
    def validate_phone(cls, value: str):
        if " " in value:
            raise ValueError("No spaces allowed on phone")
        if len(value) > 10 or len(value) < 10:
            raise ValueError('Not a phone number')
        else:
            phone_pattern = set('!@#$%^&*()_+-=`~<>,.?/:;"{}[]\'')
            if any(char in phone_pattern for char in value):
                raise ValueError('Invalid phone number')
            return "{}-{}-{}".format(value[:3],value[3:6],value[6:])
    
    @validator('age', allow_reuse=True)
    def validate_age(cls, value:int):
        if value < 15:
            raise ValidationError('Age should be greater than 15')
        elif value > 150:
            raise ValidationError('Age should be less than 150')
        return value
    
    @validator('tshirt_size', allow_reuse=True)
    def validate_tshirt(cls, value: str):
        if value not in ('XS', 'S', 'M', 'L', 'XL', 'XXL'):
            raise ValidationError('Invalid tshirt size')
        else:
            return value

    @validator('bachelor', allow_reuse=True,check_fields=False)
    def validate_bachelor(cls, value: str):
        if value[0].isspace() or value[-1].isspace():
            raise ValueError("No spaces allowed on bachelor")
        if any(not v.isalpha() for v in value):
            raise ValueError("Invalid bachelors name")
        else:
            return value
        
    @validator('department', allow_reuse=True,check_fields=False)
    def validate_department(cls, value: str):
        if value[0].isspace() or value[-1].isspace():
            raise ValueError("No spaces allowed on department")
        if any(not v.isalpha() for v in value):
            raise ValueError("Invalid department name")
        else:
            return value
 
    
class set_SignUp_Data(__Members_Inputs):
    """Setter to be used to enter signup data to database"""
    type: str = "Member"
    created_at: datetime = datetime.now(pytz.timezone('America/Puerto_Rico'))
    competitions_form: str = "No"
    membership_until: str = "Not paid"
    membership_paid: str = "No"

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
    membership_until: str
    membership_paid: str

    class Config:
            orm_mode = True
