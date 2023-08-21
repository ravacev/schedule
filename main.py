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
from calendar import month_name
from logs import temp_file

import pandas as pd
import smtp4, smtp2, smtp3, send_smtp
import forms, time
import json
import mysql.connector


# SQL Keywords for printing list titles and values
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
# 

# Initialized objects for printing values, managament users and search results respectively 
work_querys = Work()
user_mgm = UserSetting()
hunt = Searching()
# 

app=Flask(__name__)

csrf_token = CSRFProtect(app)
app.secret_key = 'mysecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Script to initialize user model with User Mixin and function to load user model
users = user_create()

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None
# 

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

# Main menu to show the values of the tasks
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
# 

# Module to handle tasks and views
@app.route("/agenda/",methods = ['GET', 'POST'])
@login_required
@admin_required
def modf():
    
    try:
        comment_form = forms.CommentForm(request.form)
        if ( request.method == 'POST' and comment_form.validate() ):
            
            # If statement to Insert or Update query parameters
            if ('insertQuery' in request.form):
                
                # Extract values from POST method to dictionary and then validate if the task is already in the database
                values = request.form.to_dict()
                validate = work_querys.insertWork(values, session['_user_id'])
                
                if validate == 0:
                    success_message = 'Ticket u OT duplicado.'
                    flash(success_message)
                else:
                    # Send email notification when insert a new task via smtp mail service
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
            # 

        row, result, column, solvedCount = work_querys.modifyView()
        
        # Charge the values for the list of City, State and Downtown
        locate, keys, size, temp = localidades()
        
        title = 'Modificar agenda'
        return render_template('agenda.html', locate=locate, keys=keys, size=size, temp=temp, title=title, form=comment_form, result=result, row=row, column=column, stamp=stamp, admin=session['username'], solvedCount=solvedCount)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html', error = err)
# 
    
# Module to handle the case with 'Aintech' partner
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
# 
    
# Module to handle 'Postponed' cases where the Partner is not 'Aintech'
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
# 

# Module to login user with password and reset password
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
# 

# Logout module user
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
# 

# Delete task with a JSON call via http request
@app.route("/agenda/<string:jobData>", methods=['POST'])
@login_required
@admin_required
@csrf_token.exempt
def modfDelete(jobData):
    jobData = json.loads(jobData)
    
    work_querys.deleteWork(jobData[2], session['_user_id'])
    
    return redirect(url_for('modf'))
# 

# Send schedule via email with smtp
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
# 

# In development
@app.route("/update")
@login_required
@csrf_token.exempt
def ajax_login():
    return render_template('update.html')
# 

# View registered users in application and update their values
@app.route("/admin", methods=["GET", "POST"])
@login_required
@admin_required
def admin():
    users = user_mgm.select_user()
    keys = ['UsersID', 'Username', 'Email', 'Admin', 'Editar', 'Eliminar']
    
    try:
        if ( request.method == 'POST' ):
                
            if ('updateQuery' in request.form):
                values = request.form.to_dict()
                user_mgm.update_user(values)
    
                return redirect(url_for('admin'))

        return render_template('admin.html', keys=keys, users=users)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html', error = err)
#

# Create a new user and password for application
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
#

# Change password for all users in the database
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
            
            # Reload models for users in User Mixin
            global users
            users = user_create()     
            
            return redirect(url_for('login'))
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html', error = err)
            
    title = 'Login'
    return render_template('changePass.html', form=change_form, title=title)
# 

@app.context_processor
def base():
    form = forms.SearchForm()
    return dict(form=form)

# Search tasks by Ticket, OT, NAP and Date
@app.route("/search", methods=['GET', 'POST'])
def search():
    
    form = forms.SearchForm(request.form)
    username = session.get('username')
    isadmin = user_mgm.isadmin(username)
    
    if (request.method == 'POST' and form.validate()):
        value = request.form.to_dict()
        finded = hunt.search(value['searched'])
        
        print(finded)

        row = len(finded)
        return render_template('search.html', form=form, finded=finded, row=row, isadmin=isadmin)
        
    return render_template('search.html', form=form, isadmin=isadmin)
# 

# Create an object in csv format to reports
@app.route("/download", methods=["GET", "POST"])
def download():
    option = request.form.get('report')
    
    if request.method == 'POST': 
        return work_querys.download(option)

    return render_template('reports.html')
# 

# In development
@app.route("/charge", methods=["GET", "POST"])
def charge():
    return render_template('charge.html')
# 

# Charts view for dinamically reports
@app.route("/charts")
def charts():
    
    anual_per_case, month_per_team = work_querys.chartjs()
    month_lookup = list(month_name)
    case_lookup = ['Correctivo', 'Preventivo']
    
    # Define plot data for anual case
    keys = anual_per_case[0].keys()

    anual = dict().fromkeys(keys)
    anual.update({'len_chart': None})
    
    for i, key in enumerate(keys, 0):
        anual[key] = [anual_per_case[i][key] for i in range(len(anual_per_case))]
        
        if key == 'type_case':
            anual[key] = list(set(anual_per_case[i][key] for i in range(len(anual_per_case))))
            anual[key] = sorted(anual[key], key=case_lookup.index)
            
        if key == 'month_name':
            anual[key] = list(set(anual_per_case[i][key] for i in range(len(anual_per_case))))
            anual[key] = sorted(anual[key], key=month_lookup.index)
    len_chart = int(len(anual['count_total']) / len(anual['type_case']))
    anual.update({'len_chart': len_chart})
    
    # Define plot data for month case
    keys = month_per_team[0].keys()
    
    team_lookup = ['Aintech', 'Bulls', 'Dunkel', 'Hansa', 'Hansa INT', 'Nucleo']

    month = dict().fromkeys(keys)
    
    for i, key in enumerate(keys, 0):
        month[key] = [month_per_team[i][key] for i in range(len(month_per_team))]
        
        if key == 'type_case':
            month[key] = list(set(month_per_team[i][key] for i in range(len(month_per_team))))
            month[key] = sorted(month[key], key=case_lookup.index)
            
        if key == 'month_name':
            month[key] = list(set(month_per_team[i][key] for i in range(len(month_per_team))))
            
        if key == 'team':
            month[key] = list(set(month_per_team[i][key] for i in range(len(month_per_team))))
            month[key] = sorted(month[key], key=team_lookup.index)
            
    temp_file(month)
        
    # Return the components to the HTML template
    return render_template(
        template_name_or_list='charts_view.html',
        anual=anual,
        month=month
    )
# 
    
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    csrf_token.init_app(app)
    
    
    app.run(port=8000)