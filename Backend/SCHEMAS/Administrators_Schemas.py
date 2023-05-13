from pydantic import BaseModel as Schema,validator, root_validator, EmailStr, SecretStr
import datetime as dt
from typing import Any


'''
    ----------------------------------------------------------------
                    SCHEMAS FOR INPUTING DATA
    ----------------------------------------------------------------
'''
'''
    Base Schema for Administrator

    It handles the inputs for userName and passwd
'''

class __Administrator_Basic_INPUTS(Schema):
    userName: str
    passwd: SecretStr

    @validator('*', allow_reuse=True, pre=True)
    def isEmpty(cls, value: str | dt.datetime):
        if type(value) is str and (value == "" or value == None):
            raise ValueError("None of the Fields can be empty!")
        return value
    
    @root_validator(allow_reuse=True, pre=True)
    def isSame(cls, values: dict):
        '''
            These two lines may be a vuln
        '''
        val1 = values.get("userName")
        val2 = values.get("passwd")

        if val1 == val2:
            raise ValueError("The User Name and password cannot be the same.")
        return values
    
    @validator('userName', allow_reuse=True)
    def isUserName(cls, value: str):
        if len(value) < 5:
            raise ValueError("The User Name must have more than four (4) characters.")
        if value[0].isspace() or value[-1].isspace():
         raise ValueError("No spaces allowed at the beginning or end of username")
        if value.isalnum() == False:
            raise ValueError("An User Name must contain alphabetic and numeric characters.")
        if value.islower() or value.isupper():
            raise ValueError("A User Name must have both upper - case and lower - case characters.")
        return value

    @validator('passwd', allow_reuse=True)
    def isPasswd(cls, value: SecretStr):
        if len(value) < 8:
            raise ValueError("The Password must have at least eight (8) characters.")
        if value.get_secret_value().islower() or value.get_secret_value().isupper():
            raise ValueError("A Password must have both upper - case and lower - case characters.")
        if all(v.isalnum() or v in ('!', '@', '#', '$', '%', '&') for v in value.get_secret_value()) == False:
            raise ValueError("A Password must have numbers, letters and symbols.")
        return value

'''
    Subclass of Base Administrator Class for the creation of accounts

    It does not validate emails, sinde EmailStr does that.
'''
class Administrator_CreateAccount_INPUTS(__Administrator_Basic_INPUTS):    #   ACCOUNT CREATING INPUTS
    """SETTER para validar inputs y luego enviar a la base de datos"""
    name: str
    email: EmailStr
    phone: str
    adminLevel: str
    createdAt: dt.datetime = dt.datetime.now()
    updatedAt: dt.datetime = dt.datetime.now()

    masterAdminToken: str

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
    def validate_email(cls, value: EmailStr):
        if value.lower() != value:
            raise ValueError("The email must be in lower - case.")
        email_domain = value.split('@')[1]
        if email_domain.count('.com') > 1:
            raise ValueError("Invalid email")
        return value
    
    @validator('phone', allow_reuse=True)
    def validate_phone(cls, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Invalid Phone number')
        return "{}-{}-{}".format(value[:3],value[3:6],value[6:])

    @validator('adminLevel',allow_reuse=True)
    def isAdminLevel(cls, value: str):

        if (len(value) <= 0 or len(value) > 2):
            raise ValueError("Invalid Admin levels")
        if not(value == "MA" or value == "GA"):
            raise ValueError("Invalid Admin levels")
        return value
    
    class Config:
        orm_mode = True

'''
    Subclass of Base Administrator Account for Login
    
    Only require userName and passwd
'''
class Administrator_LoginAccount_INPUTS(__Administrator_Basic_INPUTS):
    
    token: str = None

    @validator('userName', allow_reuse=True)
    def isUserName(cls, value: str):
        if len(value) < 5:
            raise ValueError("Invalid username or password")
        if value.isalnum() == False:
            raise ValueError("Invalid username or password")
        if value.islower() or value.isupper():
            raise ValueError("Invalid username or password")
        return value

    @validator('passwd', allow_reuse=True)
    def isPasswd(cls, value: SecretStr):
        if len(value) < 8:
            raise ValueError("Invalid username or password")
        if value.get_secret_value().islower() or value.get_secret_value().isupper():
            raise ValueError("Invalid username or password")
        if all(v.isalnum() or v in ('!', '@', '#', '$', '%', '&') for v in value.get_secret_value()) == False:
            raise ValueError("Invalid username or password")
        return value
    class Config:
        orm_mode = True

class Administrator_ChangePasswdEmail_INPUTS(Schema):
    userName: str
    newPasswd: SecretStr = None
    newEmail: EmailStr = None
    newPhone: str = None
    newLevel: str = None
    updatedAt: dt.datetime = dt.datetime.now()

    masterAdminToken: str
    
    @validator('userName', allow_reuse=True)
    def isUserName(cls, value: str):
        if len(value) < 5:
            raise ValueError("The User Name must have more than four (4) characters.")
        if value.isalnum() == False:
            raise ValueError("An User Name must contain alphabetic and numeric characters.")
        if value.islower() or value.isupper():
            raise ValueError("A User Name must have both upper - case and lower - case characters.")
        return value
    
    @validator('newPasswd', allow_reuse=True)
    def isPasswd(cls, value: SecretStr):
        if value != None:
            if len(value) < 8:
                raise ValueError("The New Password must have at least eight (8) characters.")
            if value.get_secret_value().islower() or value.get_secret_value().isupper():
                raise ValueError("A New Password must have both upper - case and lower - case characters.")
            if all(v.isalnum() or v in ('!', '@', '#', '$', '%', '&') for v in value.get_secret_value()) == False:
                raise ValueError("A New Password must have numbers, letters and symbols.")
        return value
    
    @validator('newPhone', allow_reuse=True)
    def validate_phone(cls, value: str):
        if value != None:
            if len(value) > 10 or len(value) < 10:
                raise ValueError('Invalid Phone number')
            else:
                phone_pattern = set('!@#$%^&*()_+-=`~<>,.?/:;"{}[]\'')
                if any(char in phone_pattern for char in value):
                    raise ValueError('Invalid Phone number')
                return "{}-{}-{}".format(value[:3],value[3:6],value[6:])
        return value
    class Config:
        orm_mode = True



class Member_upate_table(Schema):
    name: str 
    email: EmailStr = None
    phone: str = None
    tshirt_size: str = None
    age: int = None
    bachelor: str = None
    department: str = None
    aca_years: int = None
    masterAdminToken: str

    @validator('*', allow_reuse=True, pre=True)
    def isEmpty(cls, value: str | dt.datetime):
        if type(value) is str and (value == "" or value == None):
            raise ValueError("None of the Fields can be empty!")
        return value
    
    @validator('name', allow_reuse=True)
    def isName(cls, value: str):
     if len(value.split()) != 2:
         raise ValueError("Invalid Name")
     if value[0].isspace() or value[-1].isspace():
         raise ValueError("No spaces allowed at the beginning or end of name")
     if any(v[0].islower() for v in value.split()):
         raise ValueError("Uppercase letter must be in name")
     if any(not v.isalpha() and not v.isspace() for v in value):
         raise ValueError("A name only contains letters.")
     return value
    
    @validator('email', allow_reuse=True)
    def validate_email(cls, value: EmailStr):
        if value.lower() != value:
            raise ValueError("The email must be in lower - case.")
        email_domain = value.split('@')[1]
        if email_domain not in ('pupr.edu', 'students.pupr.edu'):
            raise ValueError("Invalid email")
        return value
    
    @validator('age', allow_reuse=True)
    def validate_age(cls, value:int):
        if value < 15:
            raise ValueError('Age should be greater than 15')
        elif value > 150:
            raise ValueError('Age should be less than 150')
        return value
    
    @validator('phone', allow_reuse=True)
    def validate_phone(cls, value: str):
        if len(value) > 10 or len(value) < 10:
            raise ValueError('Not a phone number')
        else:
            phone_pattern = set('!@#$%^&*()_+-=`~<>,.?/:;"{}[]\'')
            if any(char in phone_pattern for char in value):
                raise ValueError('Invalid phone number')
            return "{}-{}-{}".format(value[:3],value[3:6],value[6:])
    
    @validator('tshirt_size', allow_reuse=True)
    def validate_tshirt(cls, value: str):
        if value not in ('XS', 'S', 'M', 'L', 'XL', 'XXL'):
            raise ValueError('Invalid tshirt size')
        else:
            return value

    @validator('bachelor', allow_reuse=True)
    def validate_bachelor(cls, value: str):
        print(value)
        if any(not v.isalpha() for v in value):
            raise ValueError("Invalid bachelors name")
        else:
            return value
        
    @validator('department', allow_reuse=True)
    def validate_department(cls, value: str):
        if any(not v.isalpha() for v in value):
            raise ValueError("Invalid department name")
        else:
            return value
    class Config:
        orm_mode = True

class Competitions_upate_table(Schema):
    email: str = None
    phone: str = None
    ascemembership: str = None
    competition_name: str = None
    courses: str = None
    travel_availability: str = None
    older_than_twentyfive: str = None
    heavy_driver: str = None
    official_driver: str = None
    competitions_form: str = None

    @validator('*', allow_reuse=True, pre=True)
    def isEmpty(cls, value: str | dt.datetime):
        if type(value) is str and (value == "" or value == None):
            raise ValueError("None of the Fields can be empty!")
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
    
    @validator('competition_name: str', allow_reuse=True,check_fields=False)
    def validate_competition(cls, value: str):
        if value[0].isspace() or value[-1].isspace():
            raise ValueError("No spaces allowed on competitions name")
        if any(not v.isalpha() for v in value):
            raise ValueError("Invalid department name")
        else:
            return value
        
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
    class Config:
        orm_mode = True

class Administrator_Delete_Entry_INPUTS(Schema):
    masterAdminToken: str
    email: EmailStr

    @validator('*', allow_reuse=True, pre=True)
    def isEmpty(cls, value: str | dt.datetime):
        if type(value) is str and (value == "" or value == None):
            raise ValueError("None of the Fields can be empty!")
        return value
    class Config:
        orm_mode = True

class Administrator_MasterAdminToken(Schema):
    masterAdminToken: str

    @validator('*', allow_reuse=True, pre=True)
    def isEmpty(cls, value: str | dt.datetime):
        if type(value) is str and (value == "" or value == None):
            raise ValueError("None of the Fields can be empty!")
        return value
    class Config:
        orm_mode = True

'''
    ----------------------------------------------------------------------------
                            Response Models
    ----------------------------------------------------------------------------
    This data is to be outputed to table
'''

class Administrator_CreateAccount_DB(Schema):
    """SETTER Para la base de datos"""
    userName: str
    passwd: SecretStr
    name: str
    email: EmailStr
    phone: str
    adminLevel: str
    createdAt: dt.datetime
    updatedAt: dt.datetime

    masterAdminToken: str

    class Config:
        orm_mode = True

'''
    These are all the values that should be returned if an admin account is returnd.
'''
class Administrator_GETTER(Schema): 
    """Send data to frontend dashboard table"""
    idAdministrators: int
    userName: str
    password: str
    name: str
    email: EmailStr
    phone: str
    adminLevel: str
    createdAt: dt.datetime
    updatedAt: dt.datetime

    class Config:
        orm_mode = True

class Administrator_LoginAccount_DB(Schema):
    """ GET to validate information username and password from database"""
    userName: str
    passwd: SecretStr
    token: str = None

    class Config:
        orm_mode = True

class Administrator_ChangePasswdEmail_DB(Schema):
    userName: str
    newPasswd: SecretStr = None
    newEmail: EmailStr = None
    newPhone: str = None
    updatedAt: dt.datetime

    masterAdminToken: str

    class Config:
        orm_mode = True

# class Administrator_ChangeName_DB(Schema):
#     userName: str
#     name: str
#     updatedAt: dt.datetime

#     masterAdminToken: str

#     class Config:
#         orm_mode = True

# class Administrator_ChangeEmail_DB(Schema):
#     userName: str
#     email: str
#     updatedAt: dt.datetime

#     masterAdminToken: str

#     class Config:
#         orm_mode = True

# class Administrator_ChangeAll_DB(Schema):
#     userName: str
    
#     newPasswd: SecretStr
#     newName: str
#     newEmail: str
#     newLevel: str
#     updatedAt: dt.datetime

#     masterAdminToken: str

#     class Config:
#         orm_mode = True



class get_SignUp_Data(Schema):
    """Getter to be used to return signup data from database"""
    idchapter_members: str
    name: str
    email: EmailStr
    phone: str
    tshirt_size: str
    age: int
    bachelor: str
    department: str
    type: str 
    created_at: dt.datetime
    competitions_form: str
    aca_years: int
    membership_paid: str
    membership_until: str


    class Config:
            orm_mode = True


class get_Competitions_Data(Schema):
    """Getter to be used to return signup data from database"""
    idchapter_members: int
    name: str
    email: EmailStr
    phone: str
    ascemembership: str
    competition_name: str
    courses: str
    daily_availability: str
    travel_availability: str
    older_than_twentyfive: str
    heavy_driver: str
    official_driver: str
    created_at: dt.datetime
    competitions_form: str 

    class Config:
            orm_mode = True


class Output_return(Schema):
    status_code: Any
    body: Any

    class Config:
        orm_mode = True

class Administrator_Validate_User(Schema):
    """Schema to send a dictionary when validating a user in login"""
    status_code: Any
    body: Any

    class Config:
        orm_mode = True

if __name__ == "__main__":
    '''
        First local test to check if all values to create an admin account are parsed correctly.
    '''
    try:
        admin1 = Administrator_CreateAccount_INPUTS(userName="Pepe112", passwd="Every#one313", name="Pepe The Frog", email="pepe@gmail.com", adminLevel="GA")
        admin2 = Administrator_CreateAccount_INPUTS(userName="Pepe221", passwd="12pPpppppppp", name=" ", email="datapp.com", adminLevel="LA")
        #   looking = Administrator_LookAccount(idAdministrators=-1)
    except ValueError as e:
        print(e)