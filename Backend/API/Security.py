from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta
import os, jwt, pytz

class Secuirity:
     
    def __init__(self, rt: int = 1):
        try:
            if(rt < 1 or rt > 10):
                raise Exception
            else:
                self.__rt = rt
        except ValueError:
            return "The given value for rt is out-of-bounds."
        self.__SECRET_ENV_KEY = os.getenv("SECRET_KEY")

    def encryptHash(self, data: str) -> hex:
        tmp = data
        for i in range(self.__rt):
            digest = hashes.Hash(hashes.SHA256())
            digest.update(bytes(tmp, "utf-8"))
            tmp = digest.finalize().hex()
        return tmp

    def validateHash(self, data: str, hashed: hex) -> bool:
        # print(data, " ", hashed)
        return self.encryptHash(data) == hashed

    def validateUsername(self, input_username: str, db_username: str):
        if db_username == None:
            return False
        return input_username == db_username


    def __getTimeNow(self):
        """This function creates a timestamp that contain an expiration date for the JWT
            timedelta(hour=int, minute=int, second=int, microsecond=int, day=int) => puts the expiration date
            parameters of timedelta:
                days: the number of days in the duration
                seconds: the number of seconds in the duration (not including the seconds in the days parameter)
                microseconds: the number of microseconds in the duration (not including the microseconds in the seconds parameter)
                milliseconds: the number of milliseconds in the duration (equivalent to microseconds / 1000)
                minutes: the number of minutes in the duration (equivalent to seconds / 60)
                hours: the number of hours in the duration (equivalent to seconds / 3600)
                weeks: the number of weeks in the duration (equivalent to days / 7)
        """
        return datetime.now(pytz.timezone('America/Puerto_Rico')) + timedelta(days=7)

    def createToken(self, data: dict):
        """Function to create a token in JWT format"""
        token_payload = {
            'username': data['username'],
            'exp_date': self.__getTimeNow().timestamp(),
            'level': data['admin_level']
        }
        return jwt.encode(token_payload,self.__SECRET_ENV_KEY, algorithm="HS256")

    def decodeToken(self,token: str):
        """This function accepts a token and tries to decoded, if the token is invalid the exception is caught"""
        try:
            return jwt.decode(token, self.__SECRET_ENV_KEY, algorithms="HS256")
        except jwt.exceptions.PyJWTError as e:
            raise type(e)("Invalid Token") from e

    
    def validateToken(self,username:str, role:str, token:str):
        """Function to validate the payload of the token"""
        Payload = self.decodeToken(token=token)
        expiration_time = datetime.fromtimestamp(Payload['exp_date'], pytz.timezone('America/Puerto_Rico'))
        current_time = datetime.now(pytz.timezone('America/Puerto_Rico'))
        return [Payload['username'] == username and Payload['level'] == role, (expiration_time.day - current_time.day) > 1]
            

if __name__ == "__main__":
    obj = Secuirity(2)
    
    data = "Papa Franku is the Messiah."
    print("The data is ==> "+ data)
    hashedData = obj.encrypt(data)
    print("The hashed data is ==> " + hashedData)
    print("If verified, they both should be true ==> "+ str(obj.verify(data, hashedData)))

    data = "Papa Franku is not the Messiah."
    print("This is the new data ==> " + data)
    print("Let's show this heretic that this data is false ==> " + str(obj.verify(data,hashedData)))
    
