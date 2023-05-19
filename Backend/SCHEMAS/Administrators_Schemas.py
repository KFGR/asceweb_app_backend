from pydantic import BaseModel as Schema,validator, root_validator, EmailStr, SecretStr
import datetime as dt
from typing import Any
import re 

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
        if len(value) != 2:
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
    
    # token: str = None

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
    newEmail: str = None
    newPhone: str = None
    newLevel: str = None
    updatedAt: dt.datetime = dt.datetime.now()

    masterAdminToken: str
    
    @validator('newPasswd', allow_reuse=True)
    def isPasswd(cls, value: SecretStr):
        if value != None:
            if " " in value.get_secret_value():
                raise ValueError("Password must not contain spaces.")
            if len(value) < 8:
                raise ValueError("Password must have at least eight (8) characters.")
            if not any(char.isupper() for char in value.get_secret_value()):
                raise ValueError("Password must contain at least one uppercase letter.")
            if not any(char.islower() for char in value.get_secret_value()):
                raise ValueError("Password must contain at least one lowercase letter.")
            if not any(char.isdigit() for char in value.get_secret_value()):
                raise ValueError("Password must contain at least one number.")
            if not any(char in ('!', '@', '#', '$', '%', '&') for char in value.get_secret_value()):
                raise ValueError("Password must contain at least one special character.")
        return value
    
    @validator('newPhone', allow_reuse=True)
    def validate_phone(cls, value: str):
        if value:
            if len(value) != 10:
                raise ValueError('Invalid Phone number')
            else:
                if not value.isdigit():
                    raise ValueError('Invalid Phone number')
                return "{}-{}-{}".format(value[:3],value[3:6],value[6:])
        return value
    
    @validator('newLevel',allow_reuse=True)
    def isAdminLevel(cls, value: str):
        if value:
            if len(value) != 2:
                raise ValueError("Invalid Admin levels")
            if not value in ('MA', 'GA'):
                raise ValueError("Invalid Admin levels")
            return value
        return value
    

    @validator('newEmail', allow_reuse=True)
    def validate_email(cls, value: str):
        if value:
            if " " in value:
                raise ValueError("No spaces allowed on email")
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                raise ValueError("Invalid email")
            if value.lower() != value:
                raise ValueError("The email must be in lower - case.")
            email_domain = value.split('@')[1]
            if email_domain.count('.com') > 1:
                raise ValueError("Invalid email")
            return value
        return value

    class Config:
        orm_mode = True



class Member_update_table(Schema):
    email: str
    newEmail: str = None
    newPhone: str = None
    newTshirt_size: str = None
    newAge: int = None
    newBachelor: str = None
    newDepartment: str = None
    newAca_years: int = None
    newMembershipPaid: str = None

    masterAdminToken: str

    @validator('*', allow_reuse=True, pre=True)
    def isEmpty(cls, value: str | dt.datetime):
        if type(value) is str and (value == "" or value == None):
            raise ValueError("None of the Fields can be empty!")
        return value
    
    @validator('email', allow_reuse=True)
    def validate_email(cls, value: str):
        if value:
            if " " in value:
                raise ValueError("No spaces allowed at the beginning or end of email")
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    raise ValueError("Invalid email")
            if value.lower() != value:
                raise ValueError("The email must be in lower - case.")
            email_domain = value.split('@')[1]
            if email_domain not in ('pupr.edu', 'students.pupr.edu'):
                raise ValueError("Invalid email")
            return value
        return value
    
    @validator('newEmail', allow_reuse=True)
    def validate_email(cls, value: str):
        if value:
            if " " in value:
                raise ValueError("No spaces allowed at the beginning or end of email")
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    raise ValueError("Invalid email")
            if value.lower() != value:
                raise ValueError("The email must be in lower - case.")
            email_domain = value.split('@')[1]
            if email_domain not in ('pupr.edu', 'students.pupr.edu'):
                raise ValueError("Invalid email")
            return value
        return value
    
    @validator('newPhone', allow_reuse=True)
    def validate_phone(cls, value: str):
        if value:
            if len(value) != 10:
                raise ValueError('Invalid Phone number')
            else:
                if not value.isdigit():
                    raise ValueError('Invalid Phone number')
                return "{}-{}-{}".format(value[:3],value[3:6],value[6:])
        return value

    @validator('newAge', allow_reuse=True)
    def validate_age(cls, value:int):
        if value:
            if value < 15:
                raise ValueError('Age should be greater than 15')
            elif value > 150:
                raise ValueError('Age should be less than 150')
            return value
        return value
    
    @validator('newTshirt_size', allow_reuse=True)
    def validate_tshirt(cls, value: str):
        if value:
            if value not in ('XS', 'S', 'M', 'L', 'XL', 'XXL'):
                raise ValueError('Invalid tshirt size')
            else:
                return value
        return value

    @validator('newBachelor', allow_reuse=True,check_fields=False)
    def validate_bachelor(cls, value: str):
        if value:
            if value[0].isspace() or value[-1].isspace():
                raise ValueError("No spaces allowed at the beginning or end of bachelor")
            if any(not v.isalpha() and not v.isspace() for v in value):
                raise ValueError("A bachelor only contains letters.")
            
            return value
        return value
        
    @validator('newDepartment', allow_reuse=True,check_fields=False)
    def validate_department(cls, value: str):
        if value:
            if value[0].isspace() or value[-1].isspace():
                raise ValueError("No spaces allowed at the beginning or end of department")
            if any(not v.isalpha() and not v.isspace() for v in value):
                raise ValueError("A department only contains letters.")
            
            return value
        return value
   
    @validator('newMembershipPaid',allow_reuse=True)
    def validate_membership(cls,value:str):
        if value:
            if " " in value:
                raise ValueError("Space is not allowed in membership input")
            if value not in ('Yes','No'):
                raise ValueError("Invalid membership input")
            return value
        return value
    class Config:
        orm_mode = True

class Competitions_update_table(Schema):
    email: str
    newEmail: str = None
    newPhone: str = None
    newAscemember: str = None
    newAscemembership: str = None
    newCompetition_name: str = None
    newCourses: str = None
    newDaily_availability: str = None
    newTravel_availability: str = None
    newOlder_than_twentyfive: str = None
    newHeavy_driver: str = None
    newOfficial_driver: str = None
    newTravel_june: str = None
    newCompetitions_form: str = None
    newExperiences: str = None

    masterAdminToken: str
    @validator('*', allow_reuse=True, pre=True)
    def isEmpty(cls, value: str | dt.datetime):
        if type(value) is str and (value == "" or value == None):
            raise ValueError("None of the Fields can be empty!")
        return value

    @validator('newEmail', allow_reuse=True)
    def validate_email(cls, value: str):
        if value:
            if " " in value:
                raise ValueError("No spaces allowed on email")
            if value.lower() != value:
                raise ValueError("The email must be in lower - case.")
            email_domain = value.split('@')[1]
            if email_domain != 'students.pupr.edu':
                raise ValueError("Invalid email")
            return value
        return value
    
    @validator('newPhone', allow_reuse=True)
    def validate_phone(cls, value: str):
        if value:
            if " " in value:
                raise ValueError("No spaces allowed on phone")
            if len(value) > 10 or len(value) < 10:
                raise ValueError('Not a phone number')
            else:
                phone_pattern = set('!@#$%^&*()_+-=`~<>,.?/:;"{}[]\'')
                if any(char in phone_pattern for char in value):
                    raise ValueError('Invalid phone number')
                return "{}-{}-{}".format(value[:3],value[3:6],value[6:])
        return value
        
    
    @validator('newCompetition_name: str', allow_reuse=True,check_fields=False)
    def validate_competition(cls, value: str):
        if value:
            if value[0].isspace() or value[-1].isspace():
                raise ValueError("No spaces allowed on competitions name")
            if any(not v.isalpha() for v in value):
                raise ValueError("Invalid department name")
            else:
                return value
        return value
        
    @validator('newHeavy_driver', allow_reuse=True)
    def validate_heavy_duty(cls, value: str):
        if value:
            if value not in ('Yes', 'No'):
                raise ValueError('Invalid answer')
            else:
                return value
        return value

    @validator('newOfficial_driver', allow_reuse=True)
    def validate_offdriver(cls, value: str):
        if value:
            if value not in ('Yes', 'No'):
                raise ValueError('Invalid answer')
            else:
                return value
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

class Administrator_list_delete(Schema):
    masterAdminToken: str
    emails: list

    @validator('*', allow_reuse=True, pre=True)
    def isEmpty(cls, value: str | dt.datetime):
        if type(value) is str and (value == "" or value == None):
            raise ValueError("None of the Fields can be empty!")
        return value

    @validator('emails', allow_reuse=True)
    def validate_emails(cls, value: list):
        if not value:
            raise ValueError("Emails list cannot be empty")
        
        if len(value.emails) < 1:
            raise ValueError("Provide a list of emails")
        
        for email in value:
            if not email.strip():
                raise ValueError("Emails cannot be empty strings")

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

    """validaciones de las variables"""

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

class Member_update(Schema):
    email: str
    newEmail: str = None
    newPhone: str = None
    newTshirt_size: str = None
    newAge: int = None
    newBachelor: str = None
    newDepartment: str = None
    newAca_years: int = None
    newMembershipPaid: str = None

    masterAdminToken: str
    class Config:
        orm_mode = True

class Competitions_update(Schema):
    email: str
    newEmail: str = None
    newPhone: str = None
    newAscemember: str = None
    newAscemembership: str = None
    newCompetition_name: str = None
    newCourses: str = None
    newDaily_availability: str = None
    newTravel_availability: str = None
    newOlder_than_twentyfive: str = None
    newHeavy_driver: str = None
    newOfficial_driver: str = None
    newTravel_june: str = None
    newCompetitions_form: str = None
    newExperiences: str = None


    class Config:
        orm_mode = True

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
    travel_june: str
    experiences: str
    asce_member: str

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