import mysql.connector
import datetime

##mover ini de db a la clase
mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='admin',
    password='password',
    database='testing',
    autocommit=True
)

class BaseDB(object):
    def __init__(self):
        mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='password',
        database='testing',
        autocommit=True
        )

class Work(BaseDB):
    def __init__(self):
        #inicializar coneccion a la db desde aqui#
        super(Work, self).__init__()
        
    def __del__(self):
        self.connector.close()
        
    def selectWork(self):
        
        mydb.connect()

        mycursor = self.connector.cursor()

        mycursor.execute(''' select COUNT(*) from status where state_order = "PENDIENTE" ''')
        
        row = list(mycursor.fetchone())


        mycursor.execute(''' CALL `GetSelectSchedule`() ''')
        

        result = list(mycursor.fetchall())
        
        mydb.close()
        
        return row, result

    def insertWork(self, values, username):
        mydb.connect()

        mycursor = mydb.cursor()
        
        sql = ''' SELECT idusers FROM users WHERE username = %s '''
        
        val = [(username)]
        
        mycursor.execute(sql, val)

        iduser = list(mycursor.fetchone())

        sql = '''
            CALL PutInsertSchedule(%s, %s, %s, %s,
            %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s);
        '''

        val = (values[0], values[1], values[2], iduser[0],
            values[3], values[4], 
            values[5], values[6], values[7], values[8], values[9], 
            values[10], values[11], values[12], 
            values[13], values[14], values[15], values[16], values[17], 
            values[18], values[19], values[20])

        mycursor.execute(sql, val)
        mydb.commit()
        
        mydb.close()

        return

    def deleteWork(self, num_ticket, username):
        mydb.connect()

        mycursor = mydb.cursor()
        sql = '''CALL `DeleteAllSchedule`(%s);'''
        val = [(num_ticket)]

        mycursor.execute(sql, val)
        mydb.commit()
        
        mydb.close()

        return

    def updateWork(self, values, username):#esta funcion es una kk
        mydb.connect()

        mycursor = mydb.cursor()
        
        sql = ''' SELECT idusers FROM users WHERE username = %s '''
        
        val = [(username)]
        
        mycursor.execute(sql, val)

        iduser = list(mycursor.fetchone())

        if values[1] == None:
            insertWork(values, iduser[0])
        else:
            sql = '''
                CALL PutUpdateSchedule(%s, %s, %s, %s, %s,
                %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s);
            '''
            val = (values['id_ot'], values[1], values[1], values[2], iduser[0],
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

class UserManager(BaseDB):
    def __init__(self):
        super(UserManager, self).__init__()
    
    def authenticator(self, username):
        
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
        
    def createUser(self, username, password, email): 
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
        
    def isadmin(self, username):
    
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