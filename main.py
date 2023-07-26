from flask import Flask,redirect,url_for,render_template
from flask import request
from flask import session
from flask import make_response
from flask import flash
from flask import g
from flask import send_file
from datetime import datetime
from mysql.connector.errors import Error
from models import create_password, check_password, User
from decorators import admin_required, localidades
from flask_login import login_required, LoginManager, logout_user, current_user, login_user, AnonymousUserMixin
from flask_wtf import CSRFProtect
from query import Work, UserSetting, Searching
from scripts import user_create

import pandas as pd
import smtp4, smtp2, smtp3, send_smtp
import forms, time
import json
import mysql.connector


stamp = ['workID', 'OT', 'Ticket', 'Nap', 'Inconveniente', 'Fase', 'Coordenadas', 'Ingreso', 
          'Pre Afectacion', 'Demora', 'Prioridad', 'Team', 'Cuadrilla', 
          'Departamento', 'Ciudad', 'Barrio', 'Estado', 'Resolucion', 
          'Motivo', 'Post Afectacion', 'Comentario', 'Agendamiento','Editar', 'Eliminar']

stamp_index = ['OT', 'Ticket', 'Nap', 'Inconveniente', 'Fase', 'Coordenadas', 'Ingreso', 
          'Pre Afectacion', 'Demora', 'Prioridad', 'Team', 'Cuadrilla', 
          'Departamento', 'Ciudad', 'Barrio', 'Estado', 'Resolucion', 
          'Motivo', 'Post Afectacion', 'Comentario']

stamp_mail = ['OT', 'Ticket', 'Nap', 'Inconveniente', 'Coordenadas', 'Ingreso', 'Pre Afectacion', 'Demora', 'Prioridad'
              ,'Team', 'Cuadrilla', 'Zona', 'Estado', 'Fecha de Resolucion', 'Motivo']

work_querys = Work()
user_mgm = UserSetting()
hunt = Searching()

app=Flask(__name__)

csrf_token = CSRFProtect(app)
app.secret_key = 'mysecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = user_create()

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
        row, result, column, solvedCount = work_querys.selectWork()

        if not result:
            sql_keys = list()
        else:
            sql_keys = list(result[0].keys())[1::]
            
        title = 'Agenda'
        return render_template('index.html', title=title, result=result, row=row, column=column, keys=sql_keys, stamp=stamp_index, isadmin=isadmin, solvedCount=solvedCount)
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
                validate = work_querys.insertWork(values, session['_user_id'])
                if validate == 0:
                    success_message = 'Ticket u OT duplicado.'
                    flash(success_message)
                else:
                    email_message = render_template('resume_mail.html', values=values)
                    receiver_email = user_mgm.authenticator(session['username'])
                    receiver_email = [receiver_email['Email']]
                    subject = f'Caso transferido a {values["team"]}. OT: {values["id_ot"]}, Ticket: {values["num_ticket"]}'

                    smtp2.sendEmail(email_message, receiver_email, subject)
                    # send_smtp.sendEmail(email_message, receiver_email, subject)
                    return redirect(url_for('modf'))
            if ('updateQuery' in request.form):
                values = request.form.to_dict()
                work_querys.updateWork(values, session['_user_id'])

        row, result, column, solvedCount = work_querys.modifyView()
        locate, keys, size, temp = localidades()
        
        title = 'Modificar agenda'
        return render_template('agenda.html', locate=locate, keys=keys, size=size, temp=temp, title=title, form=comment_form, result=result, row=row, column=column, stamp=stamp, admin=session['username'], solvedCount=solvedCount)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html', error = err)
    
#Modulo agenda para actualizar los casos de aintech
@app.route("/unaffectedly/",methods = ['GET', 'POST'])
@login_required
@admin_required
def unaffectedly():
    
    try:
        comment_form = forms.CommentForm(request.form)
        if ( request.method == 'POST' and comment_form.validate() ):
                
            if ('insertQuery' in request.form):
                values = request.form.to_dict()
                validate = work_querys.insertWork(values, session['_user_id'])
                if validate == 0:
                    success_message = 'Ticket u OT duplicado.'
                    flash(success_message)
                    
                else:
                    return redirect(url_for('unaffectedly'))
            if ('updateQuery' in request.form):
                values = request.form.to_dict()
                work_querys.updateWork(values, session['_user_id'])

        row, result, column = work_querys.unaffectedly()
        locate, keys, size, temp = localidades()
        
        title = 'Modificar agenda'
        return render_template('aintech_view.html', locate=locate, keys=keys, size=size, temp=temp, title=title, form=comment_form, result=result, row=row, column=column, stamp=stamp, admin=session['username'])
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html', error = err)
    
#Modulo agenda para actualizar los casos postergados
@app.route("/postponed/",methods = ['GET', 'POST'])
@login_required
@admin_required
def postponed():
    
    try:
        comment_form = forms.CommentForm(request.form)
        if ( request.method == 'POST' and comment_form.validate() ):
                
            if ('insertQuery' in request.form):
                values = request.form.to_dict()
                validate = work_querys.insertWork(values, session['_user_id'])
                if validate == 0:
                    success_message = 'Ticket u OT duplicado.'
                    flash(success_message)
                    
                else:
                    return redirect(url_for('modf'))
            if ('updateQuery' in request.form):
                values = request.form.to_dict()
                work_querys.updateWork(values, session['_user_id'])

        row, result, column = work_querys.PostergadoView()
        locate, keys, size, temp = localidades()
        
        title = 'Postergados'
        return render_template('postponed.html', locate=locate, keys=keys, size=size, temp=temp, title=title, form=comment_form, result=result, row=row, column=column, stamp=stamp, admin=session['username'])
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
                if user.username == username and check_password(user.password, password) and user.active is True:
                    
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
    
    work_querys.deleteWork(jobData[2], session['_user_id'])
    
    return redirect(url_for('modf'))

# Modulo enviar correo de la agenda
@app.route("/sendSchedule")
@login_required
@admin_required
def sendSchedule():

    row, result, column, resume = work_querys.email_send()
    
    receiver_email = ["AgendayConfirmacion@personal.com.py","InternetCorporativo@personal.com.py",
            "MesadeayudaDEC@personal.com.py","OPERADORES_DE_HOJA_DE_RUTA@personal.com.py",
            "OPERADORES_DE_SOPORTE@personal.com.py","CC_INTERNET@personal.com.py",
            "Soluciones_Tecnologicas@personal.com.py","OFS_Red@personal.com.py"]
    
    subject = 'Agenda OFS'
    
    if not result:
        mail_keys = list()
    else:
        mail_keys = list(result[0].keys())

    send_time = datetime.now()
    send_time = send_time.strftime("%d/%m/%Y, %H:%M:%S")
    
    email_message = render_template('sendSchedule.html', resume=resume, result=result, row=row, column=column, stamp=stamp_mail, send_time=send_time, keys=mail_keys)
    smtp2.sendEmail(email_message, receiver_email, subject)
    # send_smtp.sendEmail(email_message, receiver_email, subject)
    return redirect(url_for('modf'))

@app.route("/update")
@login_required
@csrf_token.exempt
def ajax_login():
    return render_template('update.html')

#Modulo para visualizar los usuarios de la base de datos
@app.route("/admin")
@login_required
@admin_required
def admin():
    users = user_mgm.select_user()
    tlusers = ['Username', 'Email', 'Admin', 'Created Date', 'Eliminar', 'Editar']
    
    row = len(users)
    column = len(tlusers) - 1
    
    return render_template('admin.html', tlusers=tlusers, users=users, row=row, column=column)

#Modulo para crear usuarios
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
            
            global users
            users = user_create()
            
            return redirect(url_for('admin'))
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html', error = err)
            
    title = 'Login'
    return render_template('create.html', form=create_form, title=title)

#Modulo para cambio de contraseña del usuario
@app.route("/change", methods=['GET', 'POST'])
def change_pass():
    try:
        change_form = forms.ChangeForm(request.form)
        if (request.method == 'POST' and change_form.validate()):
            
            username = change_form.username.data
            oldpassword = change_form.oldpassword.data
            newpassword = create_password(change_form.newpassword.data)
            
            user_mgm.change_pass(username, oldpassword, newpassword)
            success_message = 'Su contraseña ha sido modificada con exito {}'.format(username)
            flash(success_message)
            
            global users
            users = user_create()     
            
            return redirect(url_for('login'))
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html', error = err)
            
    title = 'Login'
    return render_template('changePass.html', form=change_form, title=title)

@app.context_processor
def base():
    form = forms.SearchForm()
    return dict(form=form)

# Modulo para busqueda por Ticket, OT, NAP y Fecha
@app.route("/search", methods=['GET', 'POST'])
def search():
    form = forms.SearchForm(request.form)
    username = session.get('username')
    isadmin = user_mgm.isadmin(username)
    if (request.method == 'POST' and form.validate()):
        value = request.form.to_dict()
        finded = hunt.search(value['searched'])

        row = len(finded)
        return render_template('search.html', form=form, finded=finded, row=row, isadmin=isadmin)
        
    return render_template('search.html', form=form, isadmin=isadmin)

# Crea un objeto csv para reportes
@app.route("/download", methods=["GET", "POST"])
def download():
    option = request.form.get('report')
    
    if request.method == 'POST': 
        return work_querys.download(option)

    return render_template('reports.html')

# Formulario para cargar datos
@app.route("/charge", methods=["GET", "POST"])
def charge():
    return render_template('charge.html')
    
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    csrf_token.init_app(app)
    
    
    app.run(port=8000)