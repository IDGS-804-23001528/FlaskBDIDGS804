from wtforms import Form, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import Optional
from wtforms import IntegerField, StringField, PasswordField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):
    id = IntegerField("Id")
    nombre=StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido")
    ])
    matricula = IntegerField("Matricula",[
        validators.DataRequired(message="El campo es requerido")
    ])
    apellidos=StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido")
    ])
    email=EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese correo válido")
    ])
    telefono=StringField("Teléfono", [
        validators.DataRequired(message="El campo es requerido")        
    ])
    especialidad=StringField("Especialidad", [
        validators.DataRequired(message="El campo es requerido")
    ])
    
class AlumnoForm(FlaskForm):
    id = IntegerField("Id")
    nombre=StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido")
    ])
    apellidos=StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido")
    ])
    email=EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese correo válido")
    ])
    telefono=StringField("Teléfono", [
        validators.DataRequired(message="El campo es requerido")        
    ])
    alumno_id=SelectField(
        "Alumno", 
        coerce=int,
        choices=[],
        validators=[validators.DataRequired()]
    )
    
class MaestroForm(Form):
    matricula = IntegerField("Matricula", [
        validators.DataRequired(message="El campo es requerido")
    ])
    nombre=StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido")
    ])
    especialidad=StringField("Especialidad", [
        validators.DataRequired(message="El campo es requerido")
    ])
    email=EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese correo válido")
    ])

class CursoForm(FlaskForm):
    id = IntegerField("Id")
    nombre=StringField(
        "Nombre", [
        validators.DataRequired(message="El campo es requerido")]        
    )
    descripcion=StringField("Descripcion", [
        validators.DataRequired(message="El campo es requerido")        
    ])
   
    maestro_id=SelectField(
        "Maestro", 
        coerce=int,
        choices=[],
        validators=[validators.DataRequired()]
    )
   
    alumno_id=SelectField(
        "Asignar alumno", 
        coerce=int,
        choices=[],
        validators=[Optional()]
    )
    
class AsignarAlumnoForm(FlaskForm): 
   
    alumno_id = SelectField(
        "Asignar alumno",
        coerce=int,
        choices=[],
        validators=[validators.DataRequired()]
    )