import Error_handling as error
import databasemanagemnet as db
import password_encption 
import utitlis as ut
class Bank:
    
    @classmethod
    def Add_acount(cls,acount):

        try:
            
            query = """
            INSERT INTO Acounts (name, CNIC, phone, email, address, password,balance)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (acount.name,acount.nic,acount.phone,acount.email,acount.address,acount.password,acount.balance)
            cursor,conn = cls.Execute_queries(query, values)
        
        except Exception as e: 
            raise error.CustomError("Unable to create acount")
        
        else:
            print("✅Congratulations! Your Acount Registered") 
        
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception as e:
                error.CustomError("SOmething went Wrong")
    @classmethod
    def deposit_to_acount(cls,ac_no):
          
            cursor = None
            conn = None
            
            try:
                query = "SET SQL_SAFE_UPDATES = 0"
                cursor,conn = cls.Execute_queries(query)
               
                if not cls.Acount_exists(ac_no):
                    raise error.CustomError("Account not Exits")
               
                amount = int(input("Enter Amount to deposit: "))
                if (amount)<=0:
                    raise error.CustomError("amount should be greater then 0")
               
                cls.log_transaction(ac_no,amount,"deposit",None,None)
            
            except Exception as e:
                raise error.CustomError(e)
            
            else:
                query = "UPDATE Acounts SET balance = balance+%s WHERE Account_no = %s"
                values = (amount,ac_no )
            
                cls.Execute_queries(query,values)
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()    
    @classmethod
    def withdraw_from_acount(cls,ac_no,user_pass):
        try:
            query = "SET SQL_SAFE_UPDATES = 0"
            cursor,conn = cls.Execute_queries(query)
           
            if not cls.Acount_exists(ac_no):
                raise error.CustomError("Account not Exits")
            
            amount = int(input("Enter Amount to withdraw: "))
            
            query = "SELECT balance from Acounts where Account_No = %s"
            values = (ac_no,)
            
            cursor,conn = cls.Execute_queries(query,values)
            result = cursor.fetchone()
            
            bank_balance  = float(result[0])
            cursor.close()
            conn.close()

            if (amount)<=0:
                raise error.CustomError("amount should be greater then 0")
           
            if amount>bank_balance:
                raise error.CustomError("You don't have enough funds")
            
            password = input("Enter your password to complete the process: ")
            password = password_encption.hash_password(password)
            
            if user_pass != password:
                raise error.CustomError("Invalid password")
           
            cls.log_transaction(ac_no,amount,"withdrawal",None,None)

        except Exception as e:
            raise error.CustomError(e)
        else:
           
            query = "UPDATE Acounts SET balance = balance-%s WHERE Account_no = %s"
            values = (
                amount,
                ac_no
            )
            cls.Execute_queries(query,values)
    @classmethod
    def check_balance(cls,ac_no):
        
        if not cls.Acount_exists(ac_no):
            raise error.CustomError("Account not Exits")
        
        user_pass = input("Enter your password: ")
        user_pass = password_encption.hash_password(user_pass)
        
        query = "SELECT password from Acounts where Account_No = %s"
        values = (ac_no,)
        
        cursor,conn = cls.Execute_queries(query,values)
        result  = cursor.fetchone()
        cursor.close()
        conn.close()
        
        pass1 = str(result[0])
        if user_pass != pass1:
            raise error.CustomError("Invalid Password")
        
        query = "SELECT balance from Acounts where Account_No = %s"
        values = (ac_no,)
        
        cursor,conn = cls.Execute_queries(query,values)
        result = cursor.fetchone()
        
        bank_balance  = float(result[0])
        cursor.close()
        
        conn.close()
        print(f"✅ Your Acount balance is : {bank_balance}")

    @classmethod
    def transactions(cls,ac_no):
        
        if not cls.Acount_exists(ac_no):
            raise error.CustomError("Account not Exits")
        
        query = "select * from transactions where Acount_No =%s"
        values  = (ac_no,)
       
        cursor,conn = cls.Execute_queries(query,values)
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return result  

    @classmethod
    def Execute_queries(cls, query, values=None):
        try:
            connection = db.make_connection()
            
            if db.verify_connection(connection):
                cur = connection.cursor()
               
                if values:
                    cur.execute(query,values)
                    connection.commit()
                else:
                    cur.execute(query) 
            else:
                raise error.CustomError("something went Wrong")
        
        except Exception as e:
            raise error.CustomError("Failed to connect with database")
        
        finally:
            if connection:
                return cur,connection
            

    @classmethod 
    def log_transaction(cls,ac_no,amount,txns,send_to,received_from):
        try:
            
            query = """
                    INSERT INTO transactions(Acount_No,amount,trans_type,send_to,receive) Values(%s,%s,%s,%s,%s)"""
            Values = (ac_no,amount,txns,send_to,received_from)
           
            cur,conn = cls.Execute_queries(query,Values)
        except Exception:
           raise error.CustomError("Something Went Wrong")
        
        else:
            
            if txns != "withdrawal":
                print(f"✅ Amount {amount} has been {txns} to your acount")
            elif txns == "withdrawal":
                print(f"✅ Amount {amount} has been {txns} from your acount")
            else:
                pass
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    @classmethod
    def Acount_exists(cls,ac_no):
        
        query  = 'select 1 from Acounts where Account_no = %s'
        values = (ac_no,)
        
        try:
            cursor,conn = cls.Execute_queries(query,values)
            result = cursor.fetchone()
            return result is not None
       
        finally:
            cursor.close()
            conn.close()
    @classmethod
    def Show_details(cls,ac_no,password):
        try:
           
            query = "select name,Account_No,CNIC,balance,address from Acounts where Account_No = %s"
            vals = (ac_no,)
           
            cur,conn = cls.Execute_queries(query,vals)
            results = cur.fetchall()
            cur.close()
            conn.close()
           
            name,Acountno,nic,balance,address = results[0]
            ut.printinfo(name,Acountno,nic,balance,address)
            
            while True:
                button = input("1:to Reveal information\n2:GO back\nselect your option...")
                if button == '1':
                   
                    pass1 = input("Enter your Password: ")
                    pass1 = password_encption.hash_password(pass1)
                    
                    if pass1 == password:
                        ut.printinfo(name,Acountno,nic,balance,address,True)
                    else:
                        print("Wrong password")
                elif button == '2':
                    return 0
                else:
                    print("wrong input try again")
        except Exception as e:
            raise error.CustomError(e) 
    @classmethod
    def send_money(cls,ac_no,password):
        try:
            receiver_acount_no = input("Enter receiver Acount number: ")
            
            if not cls.Acount_exists(receiver_acount_no):
                raise error.CustomError("Acount not found")
            
            query = "select name from Acounts where Account_No = %s"
            vals = (receiver_acount_no,)
            cur,conn = cls.Execute_queries(query,vals)

            result = cur.fetchone()
            acount_holder = result[0]
            
            if int(receiver_acount_no) == ac_no:
                raise error.CustomError("Receiver and Sender acounts are same")

            amount = int(input("Enter amount: "))
            if amount<=0:
                raise error.CustomError("Amount should be greater 0")
           
            query = "select balance from Acounts where Account_No = %s"
            vals = (ac_no,)
            cur,conn = cls.Execute_queries(query,vals)
            result = cur.fetchone()
            bank_balance=result[0]
           
            if amount>bank_balance:
                raise error.CustomError("YOu don't have enough funds")
            
            print(f"Receiver : {acount_holder}")
            user_pass = input("Ennter your password to complete the process or C to cancel: ")
            
            if user_pass == 'C' or user_pass == 'c':
                print("You Have Cancell transaction")
                return 0
            user_pass = password_encption.hash_password(user_pass)
            
            if user_pass != password:
                raise error.CustomError("Incorrect password.")
            
            update_queries = [("update Acounts Set balance = balance+%s where Account_No = %s",(amount,receiver_acount_no)),
                      ("update Acounts Set balance = balance-%s where Account_No = %s",(amount,ac_no))]
            
            
            for query ,vals in update_queries:
                cur,conn = cls.Execute_queries(query,vals)

            cur.close()
            conn.close()   
            
            
            cls.log_transaction(receiver_acount_no,amount,'received',None,ac_no)
            cls.log_transaction(ac_no,amount,'send',receiver_acount_no,None)
            
            print(f"✅ Amount {amount} has been send to {acount_holder} from your acount")
        
        except Exception as e:
            raise error.CustomError('Transaction failed!',e)

if __name__ == "__main__":
    pass