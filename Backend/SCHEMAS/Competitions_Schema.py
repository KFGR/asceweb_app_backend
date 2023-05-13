from pydantic import BaseModel as Schema, validator, root_validator, EmailStr, SecretStr
from datetime import datetime
import pytz
from typing import Any


class __Members_Inputs(Schema):
    """Private class to validate all inputs from the signup form"""
    name: str
    email: str
    phone: str
    ascemembership: str
    competition_name: str
    courses: str
    daily_availability: str
    travel_availability: str
    older_than_twentyfive: str
    heavy_driver: str
    official_driver: str

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
        
    @validator('ascemembership', allow_reuse=True)
    def validate_ascemembership(cls, value: str):
        if " " in value:
            raise ValueError("No spaces allowed on ascemembership number")
        if len(value) > 55:
            raise ValueError("Invalid membership")
        if value.isalnum() == False:
            raise ValueError("An User Name must contain alphabetic and numeric characters.")
        """Validar para caracteres"""
        return value

    # @validator('bachelor', allow_reuse=True,check_fields=False)
    # def validate_bachelor(cls, value: str):
    #     if value[0].isspace() or value[-1].isspace():
    #         raise ValueError("No spaces allowed on bachelor")
    #     if any(not v.isalpha() for v in value):
    #         raise ValueError("Invalid bachelors name")
    #     else:
    #         return value
        
    # @validator('department', allow_reuse=True,check_fields=False)
    # def validate_department(cls, value: str):
    #     if value[0].isspace() or value[-1].isspace():
    #         raise ValueError("No spaces allowed on department")
    #     if any(not v.isalpha() for v in value):
    #         raise ValueError("Invalid department name")
    #     else:
    #         return value
        
    @validator('competition_name: str', allow_reuse=True,check_fields=False)
    def validate_competition(cls, value: str):
        if value[0].isspace() or value[-1].isspace():
            raise ValueError("No spaces allowed on competitions name")
        if any(not v.isalpha() for v in value):
            raise ValueError("Invalid department name")
        else:
            return value
        
    # @validator('travel_availability', allow_reuse=True)
    # def validate_travel_avail(cls, value: str):
    #     if value != 'Yes' or value != 'No':
    #         raise ValueError('Invalid tshirt size')
    #     return value
        
    # @validator('older_than_twentyfive', allow_reuse=True)
    # def validate_older(cls, value: str):
    #     if value not in ('Yes', 'No'):
    #         raise ValueError('Invalid tshirt size')
    #     return value
        
    @validator('heavy_driver', allow_reuse=True)
    def validate_heavy_duty(cls, value: str):
        if value not in ('Yes', 'No'):
            raise ValueError('Invalid answer')
        else:
            return value

    @validator('official_driver', allow_reuse=True)
    def validate_offdriver(cls, value: str):
        if value not in ('Yes', 'No'):
            raise ValueError('Invalid answer')
        else:
            return value

class set_Competitions_Data(__Members_Inputs):
    """Setter to be used to enter signup data to database"""
    created_at: datetime = datetime.now(pytz.timezone('America/Puerto_Rico'))
    competitions_form: str = "Yes"

    class Config:
        orm_mode = True

class get_Competitions_Data(Schema):
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



class output(Schema):
    status_code: Any
    body: Any