import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='admin',
    password='password',
    database='schedule',
    autocommit=True
)

class selectWork():
    
    mydb.connect()

    mycursor = mydb.cursor()

    mycursor.execute(''' select COUNT(*) from status where state_order = "PENDIENTE" ''')
    
    row = list(mycursor.fetchone())


    mycursor.execute(''' CALL `schedule`.`GetSelectSchedule`() ''')
    

    result = list(mycursor.fetchall())
    
    mydb.close()



def insertWork(values):

    mydb.connect()

    mycursor = mydb.cursor()

    sql = '''
        CALL PutInsertSchedule(%s, %s, %s,
        %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s);
    '''

    val = (values[0], values[1], values[2], 
           values[3], values[4], 
           values[5], values[6], values[7], values[8], values[9], 
           values[10], values[11], values[12], 
           values[13], values[14], values[15], values[16], values[17], 
           values[18], values[19], values[20])

    mycursor.execute(sql, val)
    mydb.commit()


    mydb.close()

    return

def deleteWork(num_ticket):

    mydb.connect()

    mycursor = mydb.cursor()

    sql = 'CALL `schedule`.`DeleteAllSchedule`(%s);'
    val = [(num_ticket)]

    mycursor.execute(sql, val)
    mydb.commit()


    mydb.close()

    return

def updateWork(values):
        
    mydb.connect()

    mycursor = mydb.cursor()


    if values[1] == None:
        insertWork(values)
    else:
        sql = '''
            CALL PutUpdateSchedule(%s, %s, %s, %s,
            %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s);
        '''
        val = (values[0], values[1], values[1], values[2],
            values[3], values[4], 
            values[5], values[6], values[7], values[8], values[9], 
            values[10], values[11], values[12], 
            values[13], values[14], values[15], values[16], values[17], 
            values[18], values[19], values[20])

        mycursor.execute(sql, val)
        mydb.commit()

        sql = ''' select num_ticket from work where num_ticket = %s '''

        val = [(values[1])]

        mycursor.execute(sql, val)

        row = list(mycursor.fetchone())


    mydb.close()

    return row

def authenticator(username):
    
    mydb.connect()

    mycursor = mydb.cursor()

    sql = '''
        select * from users where username = %s
    '''
    
    val = [(username)]

    mycursor.execute(sql, val)
    
    data = list(mycursor.fetchone())

    mydb.close()
    
    return data
    
def createUser(username, password, email):
    
    mydb.connect()

    mycursor = mydb.cursor()
    
    time = datetime.datetime.now()
    flag = False
    
    sql = '''
        insert into users (username, password, email, isadmin, created_date) values (%s, %s, %s, %s, %s)
    '''
    
    val = (username, password, email, flag, time)

    mycursor.execute(sql, val)
    mydb.commit()


    mydb.close()
    
def isadmin(username):
    
    mydb.connect()

    mycursor = mydb.cursor()

    sql = '''
        select isadmin from users where username = %s
    '''
    
    val = [(username)]

    mycursor.execute(sql, val)
    
    data = list(mycursor.fetchone())

    mydb.close()
    
    return data[0]

def test(username, password):
    
    mydb.connect()

    mycursor = mydb.cursor()

    sql = ''' SELECT idusers, username, password FROM users WHERE username = %s AND password = %s '''

    val = [(username, password)]

    mycursor.execute(sql, val)

    account = dict(mycursor.fetchone())

    mydb.close()

    return account
