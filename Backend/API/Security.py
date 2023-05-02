from cryptography.hazmat.primitives import hashes

class Secuirity:
     
    def __init__(self, rt: int = 1):
        try:
            if(rt < 1 or rt > 10):
                raise Exception
            else:
                self.__rt = rt
        except ValueError:
            print("The given value for rt is out-of-bounds.")

    def encrypt(self, data: str) -> hex:
        tmp = data
        for i in range(self.__rt):
            digest = hashes.Hash(hashes.SHA256())
            digest.update(bytes(tmp, "utf-8"))
            tmp = digest.finalize().hex()
        return tmp

    def verify(self, data: str, hashed: hex) -> bool:
        return self.encrypt(data) == hashed


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
    
