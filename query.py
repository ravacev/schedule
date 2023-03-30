import mysql.connector
import datetime

##mover ini de db a la clase
# connection = mysql.connector.connect(
#     host='127.0.0.1',
#     user='admin',
#     password='password',
#     database='testing',
#     autocommit=True
# )

class Database(object):
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='password',
            database='testing',
            autocommit=True
        )
        self.cursor = self.connection.cursor()
               
class Work(Database):
    
    def __init__(self):
        super(Work, self).__init__()
             
    def selectWork(self): 
        self.connection.reconnect()
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(''' SELECT COUNT(*) AS count FROM status WHERE StatusDesc = "PENDIENTE" ''')
        row = (self.cursor.fetchone())
        
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' CALL `GetSelectSchedule`() ''')
        result = list(self.cursor.fetchall())
        column = len(result[0])

        return row['count'], result, column

    def insertWork(self, values, iduser):
        sql = '''
            CALL InsertSchedule(%s, %s, %s, %s,
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
        connection.commit()
        

        return

    def deleteWork(self, TicketID, userid):
        self.TicketID = TicketID
        self.userid = userid
        
        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        sql = (f'''
                UPDATE work, status SET work.UsersID = {self.userid}, status.StatusDesc = 'ELIMINADO' 
                WHERE work.StatusCode = status.StatusCode AND work.TicketID = {self.TicketID}
            ''')

        self.mycursor.execute(sql)
        self.connection.commit()

        return

    def updateWork(self, values, username):#esta funcion es una kk
        self.values = values
        self.username = username

        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        sql = ''' SELECT UsersID FROM users WHERE username = %s '''
        val = [(self.username)]
        self.mycursor.execute(sql, val)
        iduser = list(self.mycursor.fetchone())

        if values[1] == None:
            # insertWork(values, iduser[0])
            pass
        else:
            sql = '''
                CALL PutUpdateSchedule(%s, %s, %s, %s, %s,
                %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s);
            '''
            val = (values['id_ot'], values['num_ticket'], values['name_nap'], values['issue2'], iduser['fase2'],
                values['coord'], values['affect_clients'], 
                values['priority2'], values[6], values[7], values[8], values[9], 
                values[10], values[11], values[12], 
                values[13], values[14], values[15], values[16], values[17], 
                values[18], values[19], values[20])

            self.mycursor.execute(sql, val)
            self.connection.commit()
            

class UserSetting(Database):
    def __init__(self):
        super(UserSetting, self).__init__()
    
    def authenticator(self, username):
        self.username = username
        
        self.connection.reconnect()
        self.mycursor = self.connection.cursor(dictionary=True)
        sql = ''' SELECT * FROM users WHERE Username = %s '''
        val = [(self.username)]

        self.mycursor.execute(sql, val)
        data = self.mycursor.fetchone()
        
        return data
        
    def createUser(self, username, password, email): 
        self.username = username
        self.password = password
        self.email = email
        self.IsAdmin = True
        self.CreatedDate = datetime.datetime.now()
        self.Active = True

        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        sql = '''
            INSERT INTO users (Username, Password, Email, IsAdmin, CreatedDate, Active) values (%s, %s, %s, %s, %s, %s)
        '''
        val = (self.username, self.password, self.email, self.IsAdmin, self.CreatedDate, self.Active)

        self.mycursor.execute(sql, val)
        self.connection.commit()

    def isadmin(self, username):
        self.username = username

        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        sql = ''' SELECT IsAdmin FROM users WHERE username = %s '''
        val = [(username)]

        self.mycursor.execute(sql, val)
        data = list(self.mycursor.fetchone())
        
        return data[0]