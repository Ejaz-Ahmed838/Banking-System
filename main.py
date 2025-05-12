import acount_manage as ac
import bank as bk
import Error_handling as error
from tabulate import tabulate
import pandas as pd
import loggin as login
import Acount_settings as ac_set
import utitlis as ut
import time

def get_details():
    name = input("Enter full name: ").capitalize()
    nic = input("Enter NIC (13 digits): ")
    phone = input("Enter phone (11 digits): ")
    address = input("Enter address: ")
    return (name,nic,phone,address)

def display_menu():
    ut.clear_console()
    print("\nBanking System Menu:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. View Transactions")
    print("5. show details")
    print("6. Acount Settings")
    print("7. Send Money")
    print("8. log out")

def main(ac_no,password):
        
        while True:
            try:
                
                ut.clear_console()
                display_menu()
                choice = input("Enter your choice: ")
                
                match choice:
                    case '1':
                        
                        ut.clear_console()
                        bk.Bank.deposit_to_acount(ac_no)
                        button = input("press Enter to continuee......")
                    
                    case '2':
                        
                        ut.clear_console()
                        bk.Bank.withdraw_from_acount(ac_no,password)
                        button = input("press Enter to continuee......")
                    
                    case '3':
                        
                        ut.clear_console()
                        bk.Bank.check_balance(ac_no)
                        button = input("press Enter to continuee......")
                    
                    case '4':
                        ut.clear_console()
                        print("\n                             <--------------YOUR TRANSACTIONS------------->")
                        result = bk.Bank.transactions(ac_no)
                        
                        df = pd.DataFrame(result)
                        df = df.rename(columns={
                               0: 'Transaction ID',
                               1: 'Account No',
                               2: 'Amount',
                               3: 'Transaction Type',
                               4: 'Date',
                               5:'Send to',
                               6:'Receive from'
                        })
                        pd.set_option("display.float_format", lambda x: f"{x:.0f}")
                        df["Receive from"] = df["Receive from"].fillna("...").astype(str)
                        df["Send to"] = df["Send to"].fillna("...").astype(str)
                        if df.empty:
                            print("No transactions")
                        else:
                            print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
                        button = input("press Enter to continuee......")
                    case '5':
                        
                        ut.clear_console()
                        bk.Bank.Show_details(ac_no,password)
    
                    
                    case '6':
                       
                        ut.clear_console()
                        ac_set.settings(ac_no)
                    
                    case '7':
                        ut.clear_console()
                        bk.Bank.send_money(ac_no,password)
                        button = input("press Enter to continuee......")
                    
                    case '8':
                       
                        ut.clear_console()
                        print("Loading....")
                        time.sleep(3)
                        log_in_menu()
                    
                    case _:
                        print("Invalid selection try again")
            
            except Exception as e:
                print(error.CustomError(f"❌Error!. {e}"))
                button = input("press Enter to continuee......")


def log_in_menu():
    while True:
        try:
            ut.clear_console()
            button = input("1.Sign in \n2.Sign up\n3.Forgot Password\n4.Quit\nSelect your option..")
            if button =='1':  
                ut.clear_console() 
                ac_no,password = login.sign_in()
                main(ac_no,password)
            elif button == '2':
                ut.clear_console()
                login.sign_up()
            elif button == '3':
                ut.clear_console()
                ac_set.forgot_password()
            elif button == '4':
                quit()
            else:
                print("Invalid Input try agian")
        except Exception as e:
            print(error.CustomError(f"❌Error!. {e}"))
            button = input("press Enter to continuee......")     
if __name__ == "__main__":
    print("Wellcome To our Bank App")
    log_in_menu()
    