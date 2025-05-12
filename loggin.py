import databasemanagemnet as db
import emailvalitor as em
import Error_handling as er
import bank as bk
import main as mn
import acount_manage as ac
def sign_in():
    try:
        email = input("Enter your email :")
        
        query = "select email from users"
        cur,conn = bk.Bank.Execute_queries(query)
        
        results = cur.fetchall()
        Emails = [Email[0] for Email in results]
        
        cur.close()
        conn.close()
        
        if email not in Emails:
            raise er.CustomError("This email is not Registered")
        
        if em.is_valid_email(email):
            conn,cur = db_connection()
            query = "SELECT email,password,Account_No from Acounts where  email= %s"
            
            values = (email,)
            cur,conn = bk.Bank.Execute_queries(query,values)
            result = cur.fetchall()
            
            user_pass = input("Enter you password: ")
            user_pass = bk.password_encption.hash_password(user_pass)
            stored_gmail,stored_pass,acount_no = result[0]
            
            if stored_gmail == email:
                
                if user_pass == stored_pass:
                    return acount_no,stored_pass
                else:
                    raise er.CustomError("Invalid Password")
            
            else:
                raise er.CustomError("This Email is not registred")
        else:
            raise er.CustomError("This Email is not Registered")
    except Exception as e:
        raise er.CustomError(e)
    finally:
        cur.close()
        conn.close()

def db_connection():
    try:
        conn = db.make_connection()
        cur = conn.cursor()
        if conn and cur:
            return conn,cur
    except Exception as e:
        raise er.CustomError("Sever Error")
def sign_up():
    try:
        
        email = input("Enter your email :")
        
        if not em.is_valid_email(email):
            raise er.CustomError("Email is not valid")
        
        query = "select email from users"
        cur,conn = bk.Bank.Execute_queries(query)
        
        results = cur.fetchall()
        
        if email in results:
            raise er.CustomError("Email Already Registered")
        
        password = input("create password:")
        cnfrm_pass  = input("Confirm your password: ")
        
        if cnfrm_pass != password:
            raise er.CustomError("password does not match")
        
        print("✅ Successfully sign up no provide the following details")
        name,nic,phone,address = mn.get_details()
        
        password = bk.password_encption.hash_password(password)
        account = ac.Acount(name,nic,phone,email,address,password)
        
        bk.Bank.Add_acount(account) 
        query = "INSERT INTO users(email,password) VALUES(%s,%s)"
        
        VALUES = (email,password)
        cur,conn = bk.Bank.Execute_queries(query,VALUES)
        
        cur.close()
        conn.close()
        print("Please Sign in again To Continue... thank you")
    except Exception as e:
        raise er.CustomError(e)


if __name__ == "__main__":
    results = [('lucky24633@gmail.com',)]
    emails = [email[0] for email in results]
    print(emails)
    if 'lucky24633@gmail.com' in emails:
        print("yes")
      