from flask import Flask,redirect,url_for,render_template
from flask import request
from flask import session
from flask import make_response
from flask import flash
from flask import g
from datetime import datetime
from mysql.connector.errors import Error
from models import create_password, check_password, User
from decorators import admin_required
from flask_login import login_required, LoginManager, logout_user, current_user, login_user, AnonymousUserMixin
from flask_wtf import CSRFProtect
from query import Work, UserSetting, Searching
from scripts import user_create

import pandas as pd
import smtp, smtp2
import forms
import json
import mysql.connector


stamp = ['OT', 'Ticket', 'Nap', 'Inconveniente', 'Fase', 'Coordenadas', 'Ingreso', 
          'Clientes Afectados', 'Demora', 'Prioridad', 'Team', 'Cuadrilla', 
          'Departamento', 'Zona', 'Barrio', 'Estado', 'Fecha de resolucion', 
          'Motivo', 'Afectacion', 'Eliminar', 'Editar']

stamp_index = ['OT', 'Ticket', 'Nap', 'Inconveniente', 'Fase', 'Coordenadas', 'Ingreso', 
          'Clientes Afectados', 'Demora', 'Prioridad', 'Team', 'Cuadrilla', 
          'Departamento', 'Zona', 'Barrio', 'Estado', 'Fecha de resolucion', 
          'Motivo', 'Afectacion']

work_querys = Work()
user_mgm = UserSetting()
hunt = Searching()

app=Flask(__name__)
csrf_token = CSRFProtect(app)
app.secret_key = 'mysecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = user_create.users
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    # if 'username' in session and request.endpoint in ['login']:
    #     return redirect(url_for('home'))
    pass
    
@app.after_request
def after_request(response):
    return response

#Menu principal de la app, unicamente visualizacion
@app.route('/')
@login_required
def home():
    username = session.get('username')
    isadmin = user_mgm.isadmin(username)
    try:
        row, result, column = work_querys.selectWork()

        title = 'Agenda'
        return render_template('index.html', title=title, result=result, row=row, column=column, stamp=stamp_index, isadmin=isadmin)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')

#Modulo agenda para agregar los casos
@app.route("/agenda/",methods = ['GET', 'POST'])
@login_required
@admin_required
def modf():
    try:
        comment_form = forms.CommentForm(request.form)
        if ( request.method == 'POST' and comment_form.validate() ):
                
            if ('insertQuery' in request.form):
                values = request.form.to_dict()
                work_querys.insertWork(values, session['_user_id'])
                
                return redirect(url_for('modf'))
            if ('updateQuery' in request.form):
                values = request.form.to_dict()
                work_querys.updateWork(values, session['_user_id'])
        

        row, result, column = work_querys.selectWork()
        title = 'Modificar agenda'
        return render_template('agenda.html', title=title, form=comment_form, result=result, row=row, column=column, stamp=stamp, admin=session['username'])
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html', error = err)

#Modulo Login
@app.route("/login/", methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    if (request.method == 'POST' and login_form.validate()):
        try:
            username = login_form.username.data
            password = login_form.password.data
            for user in users:
                if user.username == username and check_password(user.password, password):
                    login_user(user)
                    session['username'] = username
                    session['isadmin'] = bool(user_mgm.isadmin(username))
                    success_message = 'Bienvenido {}'.format(username)
                    flash(success_message)
                    
                    return redirect(url_for('home'))
        except:
            error_message = 'Usuario o password no validos!'
            flash(error_message)
            
    title = 'Login'
    return render_template('login.html', form=login_form, title=title)

#Modulo Logout
@app.route("/logout/")
@login_required
def logout():
    if 'username' in session:
        session.pop('username')
        session.clear()
    if 'id' in session:
        session.pop('id')
        session.clear()
    if 'password' in session:
        session.pop('password')
        session.clear()
    return redirect(url_for('login'))

#Modulo para extraer dato por JSON para DELETE
@app.route("/agenda/<string:jobData>", methods=['POST'])
@login_required
@admin_required
@csrf_token.exempt
def modfDelete(jobData):
    jobData = json.loads(jobData)
    work_querys.deleteWork(jobData[1], session['_user_id'])

    return redirect(url_for('modf'))

# @app.route("/cookie")
# def cookie():
#     response = make_response(render_template('cookie.html'))
#     response.set_cookie('custome_cookie', 'Nicolas')
#     return response

#Modulo enviar correo de la agenda
@app.route("/sendSchedule")
@login_required
@admin_required
def sendSchedule():

    row, result, column = work_querys.selectWork()
    
    email_message = render_template('sendSchedule.html', result=result, row=row, column=column)
    smtp2.sendEmail(email_message)
    return redirect(url_for('modf'))

@app.route("/update")
@login_required
@csrf_token.exempt
def ajax_login():
    return render_template('update.html')

@app.route("/admin")
@login_required
@admin_required
def admin():
    users = user_mgm.select_user()
    tlusers = ['Username', 'Email', 'Admin', 'Created Date', 'Eliminar', 'Editar']
    
    row = len(users)
    column = len(tlusers) - 1
    
    return render_template('admin.html', tlusers=tlusers, users=users, row=row, column=column)

@app.route("/admin/create", methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    try:
        create_form = forms.RegisterForm(request.form)
        if (request.method == 'POST' and create_form.validate()):
            
            username = create_form.username.data
            password = create_password(create_form.password.data)
            email = create_form.email.data
            isadmin = request.form.get('admin')
            
            user_mgm.createUser(username, password, email, isadmin)
            success_message = 'Su usuario ha sido creado {}'.format(username)
            flash(success_message)
            
            return redirect(url_for('admin'))
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html', error = err)
            
    title = 'Login'
    return render_template('create.html', form=create_form, title=title)

@app.context_processor
def base():
    form = forms.SearchForm()
    return dict(form=form)

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = forms.SearchForm(request.form)
    if (request.method == 'POST' and form.validate()):
        value = request.form.to_dict()
        data = hunt.search(value['searched'])

        data = list(filter(lambda item: str(item['Ticket']) == (value['searched']), data))

        row = len(data)
        return render_template('search.html', form=form, data=data, row=row)
        
    return render_template('search.html', form=form)

@app.route("/download")
def download():
    
    result = work_querys.download()
    
    print(result)
    
    df = pd.DataFrame(result)
    df.to_csv('out.csv')
    
    return redirect(url_for('modf'))
    
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    csrf_token.init_app(app)
    
    app.run(port=8000)