from models import User
import query
import mysql.connector

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='admin',
    password='password',
    database='schedule',
    autocommit=True
)

def user_create():
    mydb.connect()

    mycursor = mydb.cursor(dictionary=True)

    sql = ''' SELECT * FROM users '''

    mycursor.execute(sql)

    account = mycursor.fetchall()
    
    test = account
    users = []
    
    for value in range(len(test)):
        users.append(User(id = test[value]['UsersID'], username = test[value]['Username'], password = test[value]['Password'], email = test[value]['Email'], isadmin = bool(test[value]['IsAdmin']), active = bool(test[value]['Active'])))
    
    mydb.close()
    
    return users