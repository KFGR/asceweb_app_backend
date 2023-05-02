from pydantic import BaseModel as Schema, ValidationError, validator, root_validator, EmailStr, SecretStr
import datetime as dt


'''
    ----------------------------------------------------------------
                    SCHEMAS FOR INPUTING DATA
    ----------------------------------------------------------------
'''
'''
    Base Schema for Administrator

    It handles the inputs for userName and passwd
'''

class __Administrator_Basic_IN(Schema):
    userName: SecretStr
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
            raise ValueError("The User Name and passwdord cannot be the same.")
        return values
    
    @validator('userName', allow_reuse=True)
    def isUserName(cls, value: SecretStr):
        if len(value) < 5:
            raise ValueError("The User Name must have more than four (4) characters.")
        if value.get_secret_value().isalnum() == False:
            raise ValueError("An User Name must contain alphabetic and numeric characters.")
        if value.get_secret_value().islower() or value.get_secret_value().isupper():
            raise ValueError("A User Name must have both upper - case and lower - case characters.")
        return value

    @validator('passwd', allow_reuse=True)
    def isPasswd(cls, value: SecretStr):
        if len(value) < 8:
            raise ValueError("The Password must have at least eight (8) characters.")
        if value.get_secret_value().islower() or value.get_secret_value().isupper():
            raise ValueError("A Password must have both upper - case and lower - case characters.")
        if not(value.get_secret_value().isalnum()):
            raise ValueError("A Password must have numbers and letters.")
        return value

'''
    Subclass of Base Administrator Class for the creation of accounts

    It does not validate emails, sinde EmailStr does that.
'''
class Administrator_CreateAccount_IN(__Administrator_Basic_IN):    #   ACCOUNT CREATING INPUTS
    name: str
    email: EmailStr
    adminLevel: str
    createdAt: dt.datetime = dt.datetime.now()
    updatedAt: dt.datetime = dt.datetime.now()

    @validator('name', allow_reuse=True)
    def isName(cls, value: str):
     if any(v[0].islower() for v in value.split()):
         raise ValueError("All parts of any name should contain upper - case characters.")
     if any(v.isalpha() for v in value.split()) == False:
         raise ValueError("A name only contains letters.")
     return value
    
    @validator('adminLevel', allow_reuse=True)
    def isAdminLevel(cls, value: str):
        if len(value) <= 0 or len(value) > 2:
            raise ValueError("The admin level value must have two (2) characters at all times.")
        if not(value == "MA" or value == "GA"):
            raise ValueError("The admin level value does not have any of the accepted values.")
        return value
    
    class Config:
        orm_mode = True

'''
    Subclass of Base Administrator Account for Login
    
    Only require userName and passwd
'''
class Administrator_LoginAccount_IN(__Administrator_Basic_IN):
    
    updatedAt: dt.datetime = dt.datetime.now()
    
    class Config:
        orm_mode = True


'''
    Do not know if this is to be used; however this is for inputting the ID of an admin account.
    The next class is to return the values of such account.
'''
class Administrator_AskID(Schema):
    idAdministrators: int

    @validator('idAdministrators', allow_reuse=True)
    def isIDAdmin(cls, value: int):
        if value < 0:
            raise ValueError("The given value of Admin ID is negative.")
        if value > 4294967295:
            raise ValueError("The given value of Admin ID is out of bounds.")
        return value
        
    class Config:
        orm_mode = True

'''
    ----------------------------------------------------------------------------
                            Response Models
    ----------------------------------------------------------------------------
'''

class Administrator_CreateAccount_OUT(Schema):
    userName: SecretStr
    passwd: SecretStr
    name: str
    email: EmailStr
    adminLevel: str
    createdAt: dt.datetime
    updatedAt: dt.datetime

    class Config:
        orm_mode = True

'''
    These are all the values that should be returned if an admin account is returnd.
'''
class Administrator_LookAccount_OUT(Schema):
    idAdministrators: int
    userName: str
    password: str
    name: str
    email: EmailStr
    adminLevel: str
    createdAt: dt.datetime
    updatedAt: dt.datetime

    class Config:
        orm_mode = True

class Administrator_LoginAccount_OUT(Schema):
    userName: SecretStr
    password: SecretStr

    class Config:
        orm_mode = True


if __name__ == "__main__":
    '''
        First local test to check if all values to create an admin account are parsed correctly.
    '''
    try:
        admin1 = Administrator_CreateAccount_IN(userName="Pepe112", passwd="Everyone313", name="Pepe The Frog", email="pepe@gmail.com", adminLevel="GA")
        admin2 = Administrator_CreateAccount_IN(userName="Pepe221", passwd="12", name=" ", email="datapp.com", adminLevel="LA")
        #   looking = Administrator_LookAccount(idAdministrators=-1)
    except ValidationError as e:
        print(e)