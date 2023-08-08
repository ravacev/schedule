import mysql.connector
import datetime
from flask import send_file
from mysql_querys import getSelectSchedule, PutUpdateSchedule, InsertStatus, InsertNap, InsertCrew, InsertWork, InsertZone, getResumeSelect
from mysql_querys import getReportSem, searchTK, searchNAP, searchOT, getSumN, searchDT, getSelectN1, getSelectN, searchAll, getModifyView, sumModifyView, sumReportStatus, getReportStatus
from mysql_querys import getPostergadoView, sumPostergadoView, getAintechView, sumAintechView, getReportGen, work_type_per_case, work_type_per_team
from models import check_password, create_password
import pandas as pd
from logs import writeLog


class Database(object):
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='password',
            database='schedule',
            consume_results=True
        )
        self.cursor = self.connection.cursor()
               
class Work(Database):  
    def __init__(self):
        super(Work, self).__init__()

    def download(self, option):
        self.option = option
        
        self.connection.reconnect()        
        self.cursor = self.connection.cursor(dictionary=True)
        
        if self.option == '1':
            self.cursor.execute(getSelectSchedule)
        elif self.option == '2':
            self.cursor.execute(getSelectN1)
        elif self.option == '3':
            self.cursor.execute(getSelectN)
        elif self.option == '4':
            self.cursor.execute(getReportSem)
        elif self.option == '5':
            self.cursor.execute(getReportGen)

        result = self.cursor.fetchall()
        df = pd.DataFrame(result)
        df.to_csv('reporte.csv')
    
        return send_file('reporte.csv', as_attachment=True)

    def modifyView(self): 
        self.connection.reconnect()
        self.cursor = self.connection.cursor()
        self.cursor.execute(sumModifyView)
        row = list(self.cursor.fetchone())
        row.extend(self.cursor.fetchone())
        solvedCount = row[1]
        self.connection.close()
        
        self.connection.reconnect()
        self.cursor = self.connection.cursor(dictionary=True)
        # self.cursor = self.connection.cursor()

        self.cursor.execute(getModifyView)
        result = list(self.cursor.fetchall())
        
        if row is None:
            column = 0
        else:
            column = len(result[0])

        return sum(row), result, column, solvedCount
    
    def unaffectedly(self): 
        self.connection.reconnect()
        self.cursor = self.connection.cursor()
        self.cursor.execute(sumAintechView)
        row = list(self.cursor.fetchone())
        self.connection.close()
        
        self.connection.reconnect()
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(getAintechView)
        result = list(self.cursor.fetchall())
        
        if sum(row) == 0:
            column = 0
        else:
            column = len(result[0])

        return sum(row), result, column
    
    def PostergadoView(self): 
        self.connection.reconnect()
        self.cursor = self.connection.cursor()
        self.cursor.execute(sumPostergadoView)
        row = list(self.cursor.fetchone())[0]
        self.connection.close()
        
        self.connection.reconnect()
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(getPostergadoView)
        result = list(self.cursor.fetchall())
        
        if row == 0:
            column = 0
        else:
            column = len(result[0])

        return row, result, column
    
    def selectWork(self): 
        self.connection.reconnect()
        self.cursor = self.connection.cursor()
        self.cursor.execute(sumReportStatus)
        row = list(self.cursor.fetchone())
        # row.extend(self.cursor.fetchone())
        next = self.cursor.fetchone()
        if next is None:
            solvedCount = 0
        else:
            row.extend(next)
            solvedCount = row[1]
        self.connection.close()
        
        self.connection.reconnect()
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(getReportStatus)
        result = (self.cursor.fetchall())
        # column = len(result[0])
        
        if sum(row) == 0:
            column = 0
        else:
            column = len(result[0])

        return sum(row), result, column, solvedCount
    
    def email_send(self): 
        self.connection.reconnect()
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(getResumeSelect)
        resume = list(self.cursor.fetchall())
        
        self.connection.reconnect()
        self.cursor = self.connection.cursor()
        
        self.cursor.execute(getSumN)
        row = list(self.cursor.fetchone())
        next = self.cursor.fetchone()
        if next is None:
            pass
        else:
            row.extend(next)
        self.connection.close()
        
        self.connection.reconnect()
        
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(getSelectN)
        result = list(self.cursor.fetchall())
        
        if sum(row) == 0:
            column = 0
        else:
            column = len(result[0])

        return sum(row), result, column, resume

    def insertWork(self, values, iduser):
        self.values = values
        self.iduser = iduser
        
        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        
        # Validate duplicate values
        ticket = self.values['num_ticket'].strip()
        jobid = self.values['id_ot'].strip()

        self.cursor.execute(f''' SELECT IF(TicketID = {ticket} OR JobID = {jobid}, True, False) FROM work WHERE TicketID = {ticket} OR JobID = {jobid};''')
        val = self.cursor.fetchone()
        
        if val is None:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            
            if self.values['cierre']:
                self.values['status'] = 'Solucionado'

                if self.values['agendamiento'] == '':
                    self.values['agendamiento'] = self.values['cierre']
                
            #Insert Status Table
            val = (self.values['status'], self.values['reason'], self.values['priority'], self.values['afectacion'], self.values['comentario'])
            self.mycursor.execute(InsertStatus, val)
            self.connection.commit()
            
            #Insert Crew Table
            if self.values['team'] == "1":
                self.values['team'] = 'Nucleo'
            elif self.values['team'] == "2":
                self.values['team'] = 'Hansa'
            elif self.values['team'] == "3":
                self.values['team'] = 'Hansa INT'
            elif self.values['team'] == "4":
                self.values['team'] = 'Bulls'
            elif self.values['team'] == "5":
                self.values['team'] = 'Dunkel'
            else:
                self.values['team'] = 'Aintech'
            
            val = (self.values['team'], self.values['cuadrilla'])
            self.mycursor.execute(InsertCrew, val)
            self.connection.commit()
            
            #Insert Zone Table
            val = (self.values['dep'], self.values['zone'], self.values['barrio'])
            self.mycursor.execute(InsertZone, val)
            self.connection.commit()
            
            #Insert Nap Table
            val = (self.values['name_nap'].strip(), self.values['name_nap'].strip(), self.values['fase'], self.values['issue'],  self.values['coord'])
            self.mycursor.execute(InsertNap, val)
            self.connection.commit()
            
            if self.values['agendamiento'] == '':
                self.values['agendamiento'] = None
            else:
                self.values['agendamiento'] = self.values['agendamiento'] + ' ' + time 
                
            if self.values['cierre'] == '':
                self.values['cierre'] = None
            else:
                self.values['cierre'] = self.values['cierre'] + ' ' + time
                
            self.values['datePicker'] = self.values['datePicker'] + ' ' + time 
            
            #Insert Work Table
            val = (self.values['num_ticket'].strip(), self.values['id_ot'].strip(), self.values['affect_clients'], self.values['datePicker'], self.values['cierre'], self.values['agendamiento'], self.iduser)
            writeLog(self.values, self.iduser, 'add')
            self.mycursor.execute(InsertWork, val)
            self.connection.commit()
            
            return 1
        else:
            return 0
        

    def deleteWork(self, TicketID, iduser):
        self.TicketID = TicketID
        self.iduser = iduser
        
        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        sql = ('''
                UPDATE work, status SET work.UsersID = %s, status.StatusDesc = 'ELIMINADO' 
                WHERE work.StatusCode = status.StatusCode AND work.TicketID = %s
            ''')
        val = (self.iduser, self.TicketID)

        writeLog(self.TicketID, self.iduser, 'delete')
        self.mycursor.execute(sql, val)
        self.connection.commit()

    def updateWork(self, values, iduser):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.values = values
        self.iduser = iduser

        self.connection.reconnect()
        self.mycursor = self.connection.cursor()
        sql = PutUpdateSchedule
        
        if self.values['team2'] == "1":
            self.values['team2'] = 'Nucleo'
        elif self.values['team2'] == "2":
            self.values['team2'] = 'Hansa'
        elif self.values['team2'] == "3":
            self.values['team2'] = 'Hansa INT'
        elif self.values['team2'] == "4":
            self.values['team2'] = 'Bulls'
        elif self.values['team2'] == "5":
            self.values['team2'] = 'Dunkel'
        else:
            self.values['team2'] = 'Aintech'
            
        if self.values['agendamiento2'] == '':
            self.values['agendamiento2'] = None
        else:
            self.values['agendamiento2'] = self.values['agendamiento2'] + ' ' + time 
        
        if self.values['cierre2'] == '':
            self.values['cierre2'] = None
        else:
            self.values['cierre2'] = self.values['cierre2'] + ' ' + time 

        if self.values['cierre2']:
            self.values['status2'] = 'Solucionado'

            if self.values['agendamiento2'] == '':
                self.values['agendamiento2'] = self.values['cierre2']
            
        val = (self.values['id_ot'].strip(), self.values['num_ticket'].strip(), self.values['name_nap'].strip(),
            self.values['issue2'], self.values['fase2'], self.values['coord'], 
            self.values['affect_clients'], self.values['priority2'], 
            self.values['team2'], self.values['cuadrilla2'], self.values['dep2'], 
            self.values['zone2'], self.values['barrio2'], self.values['status2'], self.values['cierre2'], self.values['agendamiento2'],
            self.values['reason2'], self.values['afectacion2'], self.values['comentario2'], self.iduser, values['workID'])

        writeLog(self.values, self.iduser, 'update')
        self.mycursor.execute(sql, val)
        self.connection.commit()
        
    def chartjs(self):
        self.connection.reconnect()
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(work_type_per_case)
        anual_per_case = self.cursor.fetchall()
        
        self.connection.reconnect()
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(work_type_per_team)
        month_per_team = self.cursor.fetchall()
        
        return anual_per_case, month_per_team

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
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(''' SELECT UsersID, Username, Email, IsAdmin AS 'Admin' FROM users WHERE username <> 'adminofs' ''')
        users = (self.cursor.fetchall())
        
        return users
    
    def update_user(self, values):
        self.values = values
        
        self.connection.reconnect()
        self.cursor = self.connection.cursor()
        
        self.cursor.execute(f''' UPDATE users SET Username = {self.values['username']} WHERE UsersID = {self.values['UsersID']} ''')
        self.connection.commit()
    
    def change_pass(self, username, oldpass, newpass):
        self.username = username
        self.oldpass = oldpass
        self.newpass = newpass
        
        self.connection.reconnect()
        self.cursor = self.connection.cursor()
        
        sql = ''' SELECT Password FROM users WHERE username = %s '''
        val = [(self.username)]
        self.cursor.execute(sql, val)
        oldhash = (self.cursor.fetchone())
        
        validate = check_password(oldhash[0], self.oldpass)
        if validate is True:
            sql = ''' UPDATE users SET Password = %s WHERE Username = %s '''
            val = (self.newpass, self.username)

            self.cursor.execute(sql, val)
            self.connection.commit()
            
    
class Searching(Database):
    def __init__(self):
        super(Searching, self).__init__()
        
    def search(self, valuePt):
        self.valuePt = valuePt
        
        self.connection.reconnect()
        self.mycursor = self.connection.cursor(dictionary=True)
        val = [(self.valuePt)]
        
        self.mycursor.execute(searchTK, val)
        data = list(self.mycursor.fetchall())
        
        if bool(data) is False:
            self.mycursor.execute(searchOT, val)
            data = list(self.mycursor.fetchall())
            
        if bool(data) is False:
            self.mycursor.execute(searchNAP, val)
            data = list(self.mycursor.fetchall())
            
        if bool(data) is False:
            self.mycursor.execute(searchDT, val)
            data = list(self.mycursor.fetchall())
        
        return data