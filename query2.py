from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from main import mysql

class test():
    cursor = mysql.connection.cursor()

    cursor.execute(''' select COUNT(*) from status where state_order = "PENDIENTE" ''')
    
    row = list(cursor.fetchone())
    
    cursor.execute(''' CALL `schedule`.`GetSelectSchedule`() ''')
    
    result = list(cursor.fetchall())