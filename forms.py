from wtforms import Form, StringField, TextField, validators
from wtforms import PasswordField, SelectField, DateTimeField, SubmitField
from wtforms.fields.html5 import EmailField, IntegerField
from flask_wtf import FlaskForm
import datetime
from wtforms.validators import DataRequired

class CommentForm(Form):
    id_ot = StringField('OT',[
                            validators.DataRequired(message='La ot es requerida.'),
                            validators.length(min=7, max=10, message='Ingrese una OT valida.')
                        ])
    
    num_ticket = StringField('Ticket',[
                            validators.DataRequired(message='El ticket es requerido.'),
                            validators.length(min=6, max=10, message='Ingrese un ticket valido.')
                            ])
    
    affect_clients = TextField('Afectacion',[
                            validators.DataRequired(message='La afectacion es requerida.'),
                            validators.length(min=0, max=5, message='Ingrese una afectacion valida.')
                        ])
    
    coord = TextField('Coordenadas',[
                            validators.DataRequired(message='La coordenada es requerida.'),
                            validators.length(min=0, max=30, message='Ingrese una coordenada valida.')
                        ])
    
    name_nap = StringField('NAP',[
                            validators.DataRequired(message='El NAP es requerido.'),
                            validators.length(min=7, max=45, message='Ingrese un NAP valido.')
                        ])
    
    phase = SelectField(u'Fase', choices=[
                            ('1', 'Fase 1'), ('2', 'Fase 2'), ('3', 'Fase 3'), ('4', 'Fase 4'), ('5', 'Fase 5'), ('6', 'Edificio'), ('7', 'Ampliacion')
                        ])
    
    issue = SelectField(u'Inconveniente', choices=[
                            ('1', 'Corte de FO'), ('2', 'Adecuacion en zona'), ('3', 'Alta atenuacion'), ('4', 'Puertos danados'), ('5', 'Sin enfrentador')
                        ])
   
    priority = SelectField(u'Prioridad', choices=[
                            ('1', 'Prioridad 1'), ('2', 'Prioridad 2'), ('3', 'Prioridad 3'), ('4', 'Prioridad 4'), ('5', 'Prioridad 5')
                        ])
    
    status = SelectField(u'Estado', choices=[
                            ('1', 'Pendiente'), ('2', 'Solucionado'), ('3', 'En camino'), ('4', 'Trabajando'), ('5', 'Cancelado'), ('6', 'Postergado')
                        ])
    
    dateDone = DateTimeField('Date/Done', format='%d-%m-%Y %H:%M:%S', default=datetime.datetime.now())

    dateDemand = DateTimeField('Ingreso', format='%d-%m-%Y %H:%M:%S', default=datetime.datetime.now(), render_kw={'disabled':''})

    reason = SelectField(u'Motivo', choices=[
                            ('1', 'Corte de SFC'), ('2', 'Negligencia'), ('3', 'Poda de Arbol'), ('4', 'Adecuacion'), ('5', 'Buffer danados'), ('6', 'Cambio de columna'), 
                            ('7', 'Falla/Deterioro'), ('8', 'Pelo roto'), ('9', 'Quemazon'), ('10', 'Robo'), ('11', 'Sabotaje'), ('12', 'Sin Inconvenientes'), ('13', 'Vehiculo de gran porte')
                        ])
    
    downUsers = IntegerField('Afectacion', validators=[
                        ])
    
    team = SelectField(u'Team', choices=[
                            ('1', 'Nucleo'), ('2', 'Hansa'), ('3', 'Dunkel'), ('4', 'Bulls')
                        ])
    
    cuadrilla = SelectField(u'Cuadrilla')
    
    dep = TextField('Departamento',[
                        validators.DataRequired(message='El departamento es requerido.'),
                        validators.length(min=0, max=45, message='Ingrese un barrio valido.')
                    ])
        
    zona = TextField('Zona',[
                    validators.DataRequired(message='La zona es requerida.'),
                    validators.length(min=0, max=45, message='Ingrese una zona valida.')
                ])
            
    barrio = TextField('Barrio',[
                validators.DataRequired(message='El barrio es requerido.'),
                validators.length(min=0, max=45, message='Ingrese un barrio valido.')
            ])
    
    insertQuery = SubmitField(label='Cargar')
    
    
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