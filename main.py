from flask import Flask,redirect,url_for,render_template
from flask import request
from flask import session
from flask import make_response
from flask import flash
from flask import g
from datetime import datetime
from mysql.connector.errors import Error
from models import create_password, check_password


from config import DevelopmentConfig

from flask_wtf import CSRFProtect
import smtp, smtp2
import query
import forms
import json
import mysql.connector

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='admin',
    password='password',
    database='schedule',
    autocommit=True
)

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf_token = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['modf']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login']:
        return redirect(url_for('home'))
    
        
@app.after_request
def after_request(response):
    # print(g.test)
    return response

#Menu principal de la app, unicamente visualizacion
@app.route('/')
def home():
    
    # custome_cookie = request.cookies.get('custome_cookie', 'Undefined')
    # print (custome_cookie)
    
    # print(g.test)

    try:
        mydb.connect()

        mycursor = mydb.cursor()

        mycursor.execute(''' select COUNT(*) from status where state_order = "PENDIENTE" ''')
        
        row = list(mycursor.fetchone())

        mycursor.execute(''' CALL `schedule`.`GetSelectSchedule`() ''')
        
        result = list(mycursor.fetchall())
        
        mydb.close()

        title = 'Agenda'
        return render_template('index.html', title=title, result=result, row=row[0], column=len(result[0]))
    except:
        return render_template('error.html')

#Modulo agenda para agregar los casos
@app.route("/agenda/",methods = ['GET', 'POST'])
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
                
                query.insertWork(values)
                
            if ('updateQuery' in request.form):
            
                values = []

                values.append(request.form.get('id_ot'))

                values.append(request.form.get('num_ticket'))

                values.append(request.form.get('affect_clients'))

                date = datetime.now().strftime('%Y-%m-%d')

                values.append(date)

                values.append(request.form.get('cierre'))
                if values[4] == '': values[4] = None

                values.append(request.form.get('status2'))

                values.append(request.form.get('reason2'))

                values.append(request.form.get('priority2'))

                values.append(request.form.get('afectacion2'))

                values.append(None)

                values.append(request.form.get('dep2'))

                values.append(request.form.get('zone2'))

                values.append(request.form.get('barrio2'))

                values.append(request.form.get('name_nap'))

                values.append(request.form.get('name_nap'))

                values.append(request.form.get('fase2'))

                values.append(request.form.get('issue2'))

                values.append(request.form.get('coord'))

                values.append(None)

                values.append(request.form.get('team2'))

                values.append(request.form.get('cuadrilla2'))
                
                i = 0

                for item in values:
                    if item == 'None':
                        values[i] = None
                        
                    i += 1
                
                result = query.updateWork(values)

        mydb.connect()

        mycursor = mydb.cursor()

        mycursor.execute(''' select COUNT(*) from status where state_order = "PENDIENTE" ''')
        
        row = list(mycursor.fetchone())

        mycursor.execute(''' CALL `schedule`.`GetSelectSchedule`() ''')
        
        result = list(mycursor.fetchall())
        
        mydb.close()

        title = 'Modificar agenda'


        return render_template('agenda.html', title=title, form=comment_form, result=result, row=row[0], column=len(result[0]))
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')
    
#Modulo Login
@app.route("/login/", methods=['GET', 'POST'])
def login():
    
    login_form = forms.LoginForm(request.form)
    if (request.method == 'POST' and login_form.validate()):
        username = login_form.username.data
        password = login_form.password.data
        
        data = query.authenticator(username)
        print(data[3])
        password  = check_password(data[3], password)
        
        print(password)
        
        if data[1] is not None and password:
            session['username'] = login_form.username.data
            success_message = 'Bienvenido {}'.format(username)
            flash(success_message)
            
            return redirect(url_for('home'))
        else:
            error_message = 'Usuario o password no validos!'
            flash(error_message)
        
    title = 'Login'
        
    return render_template('login.html', form=login_form, title=title)

#Modulo Logout
@app.route("/logout/")
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

#Modulo para extraer dato por JSON para DELETE
@app.route("/agenda/<string:jobData>", methods=['POST'])
def modfDelete(jobData):
    jobData = json.loads(jobData)
    data = jobData
    print()

    print(data)

    print()

    query.deleteWork(jobData[1])

    return redirect('/agenda/')

@app.route("/cookie")
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('custome_cookie', 'Nicolas')
    return response

#Modulo enviar correo de la agenda
@app.route("/sendSchedule")
def sendSchedule():

    result = query.selectWork.result
    row = query.selectWork.row

    email_message = render_template('sendSchedule.html', result=result, row=row[0], column=len(result[0]))
    smtp2.sendEmail(email_message)
    return redirect('/')

@app.route("/ajax-login", methods=['POST'])
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
        
        query.createUser(username, password, email)
        success_message = 'Su usuario ha sido creado {}'.format(username)
        flash(success_message)
        
        return redirect(url_for('login'))
    title = 'Login'
        
    return render_template('create.html', form=create_form, title=title)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    csrf_token.init_app(app)
    
    app.run(port=8000)