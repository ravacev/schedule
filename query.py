import mysql.connector
import datetime
from test import getSelectSchedule

class Database(object):
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='password',
            database='testing',
            consume_results=True
        )
        self.cursor = self.connection.cursor()
               
class Work(Database):  
    def __init__(self):
        super(Work, self).__init__()

    def download(self):
        self.connection.reconnect()        
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(''' CALL `GetSelectSchedule`() ''')
        result = self.cursor.fetchall()

        return result
    
    def selectWork(self): 
        self.connection.reconnect()
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(''' SELECT COUNT(*) AS count FROM work WHERE JobID = 1661573 ''')
        row = (self.cursor.fetchone())
        
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' CALL `GetSelectSchedule`() ''')
        result = list(self.cursor.fetchall())
        column = len(result[0])
        
        if len(result[0]) == 0 or row['count'] == 0:
            column = 0

        return row['count'], result, column

    def insertWork(self, values, iduser):
        self.values = values
        self.iduser = iduser
        
        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        sql = '''
            CALL InsertSchedule(%s, %s, %s, 
            %s, %s, %s,
            %s, %s, 
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s);
        '''

        val = (self.values['id_ot'], self.values['num_ticket'], self.values['name_nap'],
            self.values['issue'], self.values['fase'], self.values['coord'], 
            self.values['affect_clients'], self.values['priority'], 
            self.values['team'], self.values['cuadrilla'], self.values['dep'], 
            self.values['zone'], self.values['barrio'], self.values['status'], 
            self.values['reason'], self.values['afectacion'], self.iduser)

        self.mycursor.execute(sql, val)
        self.connection.commit()

    def deleteWork(self, TicketID, iduser):
        self.TicketID = TicketID
        self.iduser = iduser
        
        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        sql = (f'''
                UPDATE work, status SET work.UsersID = {self.iduser}, status.StatusDesc = 'ELIMINADO' 
                WHERE work.StatusCode = status.StatusCode AND work.TicketID = {self.TicketID}
            ''')

        self.mycursor.execute(sql)
        self.connection.commit()

        return

    def updateWork(self, values, iduser):
        self.values = values
        self.iduser = iduser


        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        sql = '''
            CALL PutUpdateSchedule(%s, %s, %s, 
            %s, %s, %s,
            %s, %s, 
            %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s);
        '''

        val = (self.values['id_ot'], self.values['num_ticket'], self.values['name_nap'],
            self.values['issue2'], self.values['fase2'], self.values['coord'], 
            self.values['affect_clients'], self.values['priority2'], 
            self.values['team2'], self.values['cuadrilla2'], self.values['dep2'], 
            self.values['zone2'], self.values['barrio2'], self.values['status2'], datetime.datetime.now(),
            self.values['reason2'], self.values['afectacion2'], self.iduser, values['workID'])

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
        
    def createUser(self, username, password, email, isadmin):
        self.username = username
        self.password = password
        self.email = email
        self.IsAdmin = isadmin
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

    def select_user(self):
        self.connection.reconnect()
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT UsersID, Username, Email, IsAdmin, CreatedDate FROM users WHERE username <> 'adminofs' ''')
        users = (self.cursor.fetchall())
        
        return users
    
class Searching(Database):
    def __init__(self):
        super(Searching, self).__init__()
        
    def search(self, TicketID):
        self.TicketID = TicketID
        
        self.connection.reconnect()
        self.mycursor = self.connection.cursor(dictionary=True)
        sql = ''' CALL `testing`.`SearchAll`(); '''
        val = [(self.TicketID)]
        
        self.mycursor.execute(sql)
        data = self.mycursor.fetchall()
        
        return data
        