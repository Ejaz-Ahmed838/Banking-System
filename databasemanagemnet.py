import Error_handling as error
import mysql.connector as mysql

def make_connection():
    '''establish the connection to database'''
    try:
        connection = mysql.connect(
        user = "root",
        password = "ejaz8283838@",
        host = "localhost",
        database = "bank"
        )
    except mysql.Error as e:
        raise error.CustomError("Database connection failed")
    else:
        return connection
def verify_connection(connection):
    if connection and connection.is_connected():
        return True
    else:
        return False
def create_cursor(connection):
    """Create and return a cursor object"""
    if connection and connection.is_connected():
        return connection.cursor()
    else:
        raise error.CustomError("Cursor creation failed")

if __name__ == "__main__":
    connection = make_connection()
    verify_connection(connection)
    cursor = create_cursor(connection)
    if cursor:
        print("✅ Cursor successfully created")
