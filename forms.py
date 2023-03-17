from wtforms import Form, StringField, TextField, validators
from wtforms.fields.html5 import EmailField

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
    login_form = StringField('LOGIN',
                           [
                            validators.DataRequired(message='El login es requerido.'),
                            validators.length(min=8, max=15, message='Ingrese un login valido.')
                            ]
                           )