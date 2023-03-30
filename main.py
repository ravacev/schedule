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
import smtp, smtp2
import query
from query import Work, UserSetting
import forms
import json
import mysql.connector

from scripts import user_create

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='admin',
    password='password',
    database='testing',
    autocommit=True
)

stamp = ['OT', 'Ticket', 'Nap', 'Inconveniente', 'Fase', 'Coordenadas', 'Ingreso', 
          'Clientes Afectados', 'Demora', 'Prioridad', 'Team', 'Cuadrilla', 
          'Departamento', 'Zona', 'Barrio', 'Estado', 'Fecha de resolucion', 
          'Motivo', 'Afectacion', 'Eliminar', 'Editar']

work_querys = Work()
user_mgm = UserSetting()
# user_querys = User()  

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
        row, result = work_querys.selectWork()

        title = 'Agenda'
        return render_template('index.html', title=title, result=result, row=row, column=len(result[0]), stamp=stamp, isadmin=isadmin)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')

#Modulo agenda para agregar los casos
@app.route("/agenda/",methods = ['GET', 'POST'])
# @login_required
# @admin_required
def modf(): 
    try:
        comment_form = forms.CommentForm(request.form)
        if ( request.method == 'POST' and comment_form.validate() ):
                
            if ('insertQuery' in request.form):
            
                values = []

                values.append(request.form.get('id_ot'))

                values.append(request.form.get('num_ticket'))

                values.append(request.form.get('affect_clients'))

                date = datetime.now().strftime('%Y-%m-%d')

                values.append(date)

                values.append(request.form.get('cierre'))
                if values[4] == '': values[4] = None

                values.append(request.form.get('status'))

                values.append(request.form.get('reason'))

                values.append(request.form.get('priority'))

                values.append(request.form.get('afectacion'))

                values.append(None)

                values.append(request.form.get('dep'))

                values.append(request.form.get('zone'))

                values.append(request.form.get('barrio'))

                values.append(request.form.get('name_nap'))

                values.append(request.form.get('name_nap'))

                values.append(request.form.get('fase'))

                values.append(request.form.get('issue'))

                values.append(request.form.get('coord'))

                values.append(None)

                values.append(request.form.get('team'))

                values.append(request.form.get('cuadrilla'))

                i = 0

                for item in values:
                    if item == 'None':
                        values[i] = None

                    i += 1
                
                values = request.form.to_dict()
                print(values)
                # work_querys.insertWork(values, session['_user_id'])
                return redirect(url_for('modf'))
                
            if ('updateQuery' in request.form):
                # form_keys = [ 'id_ot', 'num_ticket', 'affect_clients', 'date', 'status2',
                #                 'reason2', 'priority2', 'afectacion2', 'dep2', 'zone2',
                #                 'barrio2', 'name_nap', 'fase2', 'issue2', 'coord', 'team2', 'cuadrilla2'
                # ]

                # val = {}

                # for f in request.form.keys():
                #     val.setdefault(f, request.form.get(f))
                
                values = request.form.to_dict()
                print(values)
                # result = work_querys.updateWork(values, session['_user_id'])
                return redirect(url_for('modf'))

        row, result, column = work_querys.selectWork()
        
        title = 'Modificar agenda'
        return render_template('agenda.html', title=title, form=comment_form, result=result, row=row, column=column, stamp=stamp)
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
    # print(jobData)
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

    row, result = work_querys.selectWork()

    email_message = render_template('sendSchedule.html', result=result, row=row, column=len(result[0]))
    smtp2.sendEmail(email_message)
    return redirect('/')

@app.route("/ajax-login", methods=['POST'])
@login_required
def ajax_login():
    print(request.form)
    username = request.form['username']
    response = {'status': 200, 'username': username, 'id': 1}
    
    return json.dumps(response)

@app.route("/create", methods=['GET', 'POST'])
def create_user():
    
    create_form = forms.RegisterForm(request.form)
    if (request.method == 'POST' and create_form.validate()):
        
        username = create_form.username.data
        password = create_password(create_form.password.data)
        email = create_form.email.data
        
        user_mgm.createUser(username, password, email)
        success_message = 'Su usuario ha sido creado {}'.format(username)
        flash(success_message)
        
        return redirect(url_for('login'))
    title = 'Login'
        
    return render_template('create.html', form=create_form, title=title)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    csrf_token.init_app(app)
    
    app.run(port=8000)