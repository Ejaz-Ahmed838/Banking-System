import os
def printinfo(name, Acountno, nic, balance, address, reveal=False):
    Acountno = str(Acountno)
    nic = str(nic)
    
    if not reveal:
        print("Name: ", name)
        print(f"Account NO: {'*' * (len(Acountno) - 4) + Acountno[-4:]}")
        print(f"CNIC: {'*' * (len(nic) - 4) + nic[-4:]}")
        print("Address: ", address)
        print("Balance: ", balance)
    else:
        print("Name: ", name)
        print("Account NO:", Acountno)
        print("CNIC: ", nic)
        print("Address: ", address)
        print("Balance: ", balance)
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system("clear")
if __name__ == "__main__":
    pass
