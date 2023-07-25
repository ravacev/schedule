from functools import wraps
from flask import redirect, flash, url_for
from flask_login import current_user
import json

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, 'isadmin', True)
        if not is_admin:
            message = 'You are not admin to view this page!'
            flash(message)
            return redirect(url_for('home'))
        else:
            pass
        return f(*args, **kws)
    return decorated_function
        
def localidades():
    
    locate = {
        'Descripción de Departamento': set(),
        'Descripción de Distrito': set(),
        'Descripción de Barrio/Localidad': set()
    }
    temp = ['dep', 'zone', 'barrio']
    keys = ['Descripción de Departamento', 'Descripción de Distrito', 'Descripción de Barrio/Localidad']
    size = len(locate)
    
    f = open('localidades_py.json')
    data = json.load(f)
    
    for item in data:
        for key in keys:
            locate[key].add(item[key])      
    f.close()
    
    return locate, keys, size, temp