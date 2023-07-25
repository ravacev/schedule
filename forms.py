from wtforms import Form, StringField, TextField, validators, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm

class CommentForm(Form):
    id_ot = StringField('OT',
                           [
                            validators.DataRequired(message='La ot es requerida.'),
                            validators.length(min=7, max=10, message='Ingrese una OT valida.')
                            ]
                           )
    num_ticket = StringField('Ticket',
                            [
                            validators.DataRequired(message='El ticket es requerido.'),
                            validators.length(min=6, max=10, message='Ingrese un ticket valido.')
                            ]
                            )
    affect_clients = TextField('Afectacion',
                            [
                            validators.DataRequired(message='La afectacion es requerida.'),
                            validators.length(min=0, max=5, message='Ingrese una afectacion valida.')
                            ]
                            )
    coord = TextField('Coordenadas',
                            [
                            validators.DataRequired(message='La coordenada es requerida.'),
                            validators.length(min=0, max=30, message='Ingrese una coordenada valida.')
                            ]
                            )
    name_nap = StringField('NAP',
                           [
                            validators.DataRequired(message='El NAP es requerido.'),
                            validators.length(min=7, max=45, message='Ingrese un NAP valido.')
                            ]
                           )
   
class LoginForm(Form):
    username = StringField('username',
                           [
                            validators.DataRequired(message='El username es requerido.'),
                            validators.length(min=4, max=35, message='Ingrese un username valido.')
                            ]
                           )
    password = PasswordField('password',
                           [
                            validators.DataRequired(message='La contrasena es requerida.'),
                            validators.length(min=4, max=35, message='Ingrese una contrasena valida.')
                            ]
                           )
    
class RegisterForm(Form):
    username = StringField('username',
                           [
                            validators.DataRequired(message='El username es requerido.'),
                            validators.length(min=4, max=35, message='Ingrese un username valido.')
                            ]
                           )
    password = PasswordField('password',
                           [
                            validators.DataRequired(message='La contrasena es requerida.'),
                            validators.length(min=4, max=35, message='Ingrese una contrasena valida.')
                            ]
                           )
    email = EmailField('email',
                           [
                            validators.DataRequired(message='El email es requerido'),
                            validators.length(min=4, max=35, message='Ingrese una contrasena valida.')
                            ]
                           )
    
class ChangeForm(Form):
    username = StringField('username',
                           [
                            validators.DataRequired(message='El username es requerido.'),
                            validators.length(min=4, max=35, message='Ingrese un username valido.')
                            ]
                           )
    oldpassword = PasswordField('oldpassword',
                           [
                            validators.DataRequired(message='La contrasena es requerida.'),
                            validators.length(min=4, max=35, message='Ingrese una contrasena valida.')
                            ]
                           )
    newpassword = PasswordField('newpassword',
                        [
                        validators.DataRequired(message='La contrasena es requerida.'),
                        validators.length(min=4, max=35, message='Ingrese una contrasena valida.')
                        ]
                        )
    
class SearchForm(Form):
    searched = StringField('Searched', 
                           [
                               validators.length(min=2, max=35)
                           ])
    submit = SubmitField('Submit')