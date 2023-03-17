from flask import Flask,redirect,url_for,render_template
import forms
import query
from flask import request
from flask import session
import smtp, smtp2
import json
from datetime import datetime
import mysql.connector

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='admin',
    password='password',
    database='schedule',
    autocommit=True
)

#Menu principal de la app, unicamente visualizacion
app=Flask(__name__)
@app.route('/')
def home():

    try:

        result = query.selectWork.result
        row = query.selectWork.row

        title = 'Agenda'
        return render_template('index.html', title=title, result=result, row=row[0], column=len(result[0]))
    except:
        return render_template('error.html')

#Modulo agenda para agregar los casos
@app.route("/agenda/",methods = ['GET', 'POST'])
def modf():

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
            
            # query.insertWork(values)
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
            
            print('asdas')

            result = query.updateWork(values)

            print(result)
            
    mydb.connect()
            
    mycursor = mydb.cursor()

    result = mycursor.execute(''' CALL `schedule`.`GetSelectSchedule`() ''')
    
    result = list(mycursor.fetchall())
    row = query.selectWork.row

    title = 'Modificar agenda'


    return render_template('agenda.html', title=title, form=comment_form, result=result, row=row[0], column=len(result[0]))

#Modulo para extraer dato por JSON para DELETE
@app.route("/agenda/<string:jobData>", methods=['POST'])
def modfDelete(jobData):
    jobData = json.loads(jobData)
    data = jobData
    print()

    print(data)

    print()

    # query.deleteWork(jobData[1])

    return redirect('/agenda/')

#Modulo logins
@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        session['username'] = login_form.username.data
    return render_template('login.html', form=login_form)

# @app.route("/cookie")
# def cookie():

#Modulo enviar correo de la agenda
@app.route("/sendSchedule")
def sendSchedule():

    result = query.selectWork.result
    row = query.selectWork.row

    email_message = render_template('sendSchedule.html', result=result, row=row[0], column=len(result[0]))
    smtp2.sendEmail(email_message)
    return redirect('/')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(host='127.0.0.1',port=8000,debug=True)