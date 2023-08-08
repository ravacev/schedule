from datetime import datetime
import os
# os.chdir(path='/var/log/nginx')

def writeLog(logs, iduser, action):
    f = open('schedule.action.log', 'a')
    message = f'''Rule: {action} --> (Data: {str(logs)}
    User: {iduser}
    {datetime.now()})\n'''
        
    f.write(message)
    f.close()
    
def temp_file(debug_text):
    f = open('debug.txt', 'w')
    message = f'''---> {debug_text} '''
    
    f.write(message)
    f.close()