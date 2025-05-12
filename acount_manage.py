import emailvalitor as em
import Error_handling as error
class Acount:
    def __init__(self,name,nic,phone,email,address,password,balance=0):
        self.name = name
        self.nic = nic
        self.balance = balance
        self.phone = phone
        self.email = email
        self.password = password
        self.address = address

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name:str):
        if not name.replace(' ','').isalpha():
            raise error.CustomError("Name should only contain alphabets")
        self.__name = name
    
    @property
    def nic(self):
        return self.__nic
    @nic.setter
    def nic(self,nic:str):
        if len(nic)!= 13 or not nic.isdigit():
            raise error.CustomError("Nic should be 13 digits only")
        self.__nic = nic
   
    @property
    def address(self):
        return self.__address
    @address.setter
    def address(self,address):
        if not address:
            raise error.CustomError("please provide address")
        self.__address = address
    
    @property
    def phone(self):
        return self.__phone
    @phone.setter
    def phone(self,phone):
        if len(phone)!= 11 or not phone.isdigit():
            raise error.CustomError("Phone should be 11 digits")
        self.__phone = phone
    
    
    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self,email):
        if not em.is_valid_email(email):
            raise error.CustomError("Email is not valid")
        self.__email = email

    
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self,password):
        if len(password)<6:
            raise error.CustomError("password must be atleast 6 characters")
        self.__password = password
    
    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self,balance):
        if balance<0:
            raise error.CustomError("balance can't be negative")
        self.__balance = balance


if __name__ ==  "__main__":
    pass

