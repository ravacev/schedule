import mysql.connector
from matplotlib import pyplot as plt
import numpy as np
# class Database:
#     def __init__(self):
#         self.connection = mysql.connector.connect(
#             host='127.0.0.1',
#             user='admin',
#             password='password',
#             database='testing',
#             autocommit=True
#         )
# #         self.cursor = self.connection.cursor()
        
#     def execute_query(self, query, params=None):
#         self.cursor.execute(query, params)
#         self.connection.commit()
#         return self.cursor.fetchone()
    
#     def __del__(self):
#         self.cursor.close()
#         self.connection.close()
        
# result = Database.execute_query('''SELECT * FROM users''')
# print(result)

# class Persona():
    
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
        
#     def mostrarDatos(self):
#         return print(f'{self.username}:{self.password}')
        
# class User(Persona):
    
#     def __init__(self, username, password):
#         super().__init__(username, password)
        
# usuario = User('Nicolas', 'Nicolas')

# print(usuario.mostrarDatos())

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='password',
            database='testing',
            autocommit=True
        )
        
        self.cursor = self.connection.cursor()
        # self.cursor = self.connection.cursor()
    
    # def execute_query(self, query, params=None):
    #     self.cursor.execute(query, params)
    #     return self.cursor.fetchall()

class test(Database):
    
    def __init__(self):
        super(test, self).__init__()
    
    def execute(self):
        # self.cursor = self.connection.cursor(dictionary=True)
        # self.cursor.execute('SELECT * FROM users')
        # row = self.cursor.fetchall()
        
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(''' SELECT COUNT(*) AS count FROM status WHERE StatusDesc = "PENDIENTE" ''')
        row = (self.cursor.fetchone())
        
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' CALL `GetSelectSchedule`() ''')
        result = list(self.cursor.fetchall())

        return row['count'], result

class Usermanager(Database):
    def __init__(self):
        super(Usermanager, self).__init__()
        
    def authenticate(self, username):
        self.username = username
        
        self.cursor = self.connection.cursor(dictionary=True)
        sql = (''' SELECT * FROM users WHERE Username = %s''')
        val = [(username)]
        
        self.cursor.execute(sql, val)
        item = (self.cursor.fetchone())
        
        return item
    
b = np.matrix([[1, 2], [3, 4]])
b_asarray = np.asarray(b)
    
np.random.seed(19680801)  # seed the random number generator.
data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
data['b'] = data['a'] + 10 * np.random.randn(50)
data['d'] = np.abs(data['d']) * 100

fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
ax.scatter('a', 'b', c='c', s='d', data=data)
ax.set_xlabel('entry a')
ax.set_ylabel('entry b')
plt.show()