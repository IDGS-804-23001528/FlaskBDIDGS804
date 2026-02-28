from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms import EmailField
from wtforms import validators
 
class UserForm(Form):
    id = IntegerField('id', [
        validators.number_range(min=1, max=999999, message='valor no valido')
    ])
 
    nombre = StringField('nombre', [
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(min=4, max=20, message='requiere min=4 max=20')
    ])
 
    apellidos = StringField('apellidos', [
        validators.DataRequired(message='El apellido es requerido')
    ])
 
    email = EmailField('correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Ingrese un correo valido')
    ])
 
    telefono = StringField('telefono', [
        validators.DataRequired(message='El telefono es requerido'),
        validators.length(min=7, max=15, message='telefono invalido')
    ])
 
    especialidad = StringField('especialidad', [
        validators.DataRequired(message='La especialidad es requerida'),
        validators.length(min=3, max=50, message='especialidad invalida')
    ])