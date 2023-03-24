from models import User
import query
import mysql.connector

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='admin',
    password='password',
    database='testing',
    autocommit=True
)

class user_create():
    mydb.connect()

    mycursor = mydb.cursor(dictionary=True)

    sql = ''' SELECT * FROM users '''

    mycursor.execute(sql)

    account = mycursor.fetchall()
    
    test = account
    users = []
    
    for value in range(len(test)):
        users.append(User(id = test[value]['idusers'], username = test[value]['username'], password = test[value]['password'], email = test[value]['email'], isadmin = bool(test[value]['isadmin'])))
        # users.insert(value, test[value]['idusers'], test[value]['username'], test[value]['password'], test[value]['email'], test[value]['isadmin'])
    
    mydb.close()