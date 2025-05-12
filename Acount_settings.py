import emailvalitor as em
import Error_handling as er
import bank as bk
def forgot_password():
    try:
        gmail = input("Enter your email: ")
        
        if not em.is_valid_email(gmail):
            raise er.CustomError("Invalid email")
        
        query = "Select email,CNIC from Acounts where email = %s"
        values = (gmail,)
        
        cur,conn = bk.Bank.Execute_queries(query,values)
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        email,cnic = result
        
        if gmail == email:
           
            nic = input("Enter your NIC number: ")
           
            if nic == cnic:
               
                password = input("Enter new password...")
                if len(password)<6:
                    raise er.CustomError("Password must be atleast 6 char")
                
                query = "SET SQL_SAFE_UPDATES = 0"
                cur,conn = bk.Bank.Execute_queries(query)
               
                cur.close()
                conn.close()
                
                password = bk.password_encption.hash_password(password)
                
                update_queries = [
                                ("UPDATE Acounts SET password = %s WHERE CNIC = %s", (password,cnic)),
                                ("UPDATE users SET password = %s WHERE email = %s", (password,email)),
                                ]
                
                for query, vals in update_queries:
                    cur, conn = bk.Bank.Execute_queries(query, vals)
                    cur.close()
                    conn.close()
                
                print("✅Your password has been successulfy Reset")
            
            else:
                raise er.CustomError("Incorrect password")
        else:
            raise er.CustomError("Invalid Email")
    except Exception as e:
        raise er.CustomError(str(e))
def Reset_password(acount_no):
    try:
        
        old_password = input("Enter your Current password : ")
        old_password = bk.password_encption.hash_password(old_password)
        
        query = "Select password,email from Acounts where Account_No = %s"
        values = (acount_no,)
        
        cur,conn = bk.Bank.Execute_queries(query,values)
        result = cur.fetchone()
        cur.close()
        conn.close()
       
        stored_password,email= result
        new_password = input("Create New password: ")
        
        if len(new_password)<6:
            raise er.CustomError("Password must be atleast 6 char")
        
        new_password = bk.password_encption.hash_password(new_password)
        
        if new_password == stored_password:
            raise er.CustomError("You have Provided the same password again")   
        
        if stored_password == old_password:
            cur,conn = bk.Bank.Execute_queries("SET SQL_SAFE_UPDATES = 0")
            
            cur.close()
            conn.close()
            update_queries = [
                                ("UPDATE Acounts SET password = %s WHERE Account_no = %s", (new_password, acount_no)),
                                ("UPDATE users SET password = %s WHERE  = %s", (new_password, email)),]
            
            for query, vals in update_queries:
                cur, conn = bk.Bank.Execute_queries(query, vals)
                cur.close()
                conn.close()
            
            print("✅Your password has been successulfy Reset")
        else:
            raise er.CustomError("Incorrect password")
    except Exception as e:
        raise er.CustomError(str(e))
def update_email(acount_no):
    try:
        
        email = input("Enter your current Email: ")
        
        if not em.is_valid_email(email):
            raise er.CustomError("Invalid email")
        
        query = "Select email,password from Acounts where Account_No = %s"
        values = (acount_no,)
        
        cur,conn = bk.Bank.Execute_queries(query,values)
        
        results = cur.fetchone()
        
        stored_email,stored_password = results
        
        if stored_email!=email:
            raise er.CustomError("Invalid email")
        
        new_email = input("Enter new email: ")
        
        if not em.is_valid_email(email):
            raise er.CustomError("Email Format is Incorrect")
        
        if new_email == stored_email:
            raise er.CustomError("YOU have Enterd the same Email")
        
        password = input("Enter Your password to apply changes: ")
        password = bk.password_encption.hash_password(password)
        
        if password != stored_password:
            raise er.CustomError("Invalid password")
        
        
        update_queries = [
            ("Update Acounts Set email = %s Where Account_No = %s",(new_email,acount_no)),
            ("Update Users Set email = %s Where email = %s",(new_email,email)),
        ]
        
        for queries,vals in update_queries:
            cur,conn = bk.Bank.Execute_queries(queries,vals)
            cur.close()
            conn.close()
        
        print("✅Your Email successfully Updated")
    except Exception as e:
        raise er.CustomError("Something went wrong")

def update_phone_no(acount_no):
    try:
        query = "Select password,phone from Acounts where Account_No = %s"
        
        values = (acount_no,)
        cur,conn = bk.Bank.Execute_queries(query,values)
        
        result = cur.fetchone()
        
        stored_password,stored_phone = result
        new_phone = input("Enter new Phone Number: ")
        
        if len(new_phone)!=11 or not new_phone.isdigit():
            raise er.CustomError("Phone number must be 11 digits only") 
        
        if new_phone == stored_phone:
            raise er.CustomError("YOu have provide the old contact again")
        
        password = input("Enter Your password to apply changes: ")
        password = bk.password_encption.hash_password(password)
        
        if password != stored_password:
            raise er.CustomError("Invalid password")
        
        query = "Update Acounts Set phone = %s Where Account_No = %s"
        vals = (new_phone,acount_no)
        cur,conn = bk.Bank.Execute_queries(query,vals)
        cur.close()
        conn.close()
        
        print("✅Your Contact successfully Updated")
    except Exception as e:
        raise er.CustomError("Something went wrong")  
def Update_Address(acount_no):
    try:
        
        query = "Select password,address from Acounts where Account_No = %s"
        values = (acount_no,)
        
        cur,conn = bk.Bank.Execute_queries(query,values)
        result = cur.fetchone()
        
        stored_password,_ = result
        
        new_address = input("Enter you new Adress:")
        password = input("Enter you password to apply changes: ")
        
        password = bk.password_encption.hash_password(password)
        if stored_password != password:
            raise er.CustomError("Incorrect password") 
        
        query = "Update Acounts Set address = %s Where Account_No = %s"
        vals = (new_address,acount_no)
        
        cur,conn = bk.Bank.Execute_queries(query,vals)
        cur.close()
        
        conn.close()
        print("✅Your Adress has been successfully Updated")
    except Exception as e:
        print(e)

def settings(acount_no):
    while True:
        try:
            choice = input("1:Reset Password\n2:Update Email \n3:Update phone\n4:Update Adress\n5:Go back\nSelect your option: ")
            
            match choice:
                case '1':
                    Reset_password(acount_no)
                
                case '2':
                    update_email(acount_no)
                
                case '3':
                    update_phone_no(acount_no)
                
                case '4':
                    Update_Address(acount_no)
                
                case '5':
                    break
                
                case _:
                    print("Invalid Selection try again")
        except Exception as e:
            raise er.CustomError(e)
if __name__ == "__main__":
   pass