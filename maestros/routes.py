from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from . import maestros
from config import DevelopmentConfig
import forms
from models import db, Alumnos, Maestros
 
@maestros.route("/maestros", methods=['POST', 'GET'])
@maestros.route("/index")
def listado_maestros():
    create_form = forms.UserForm(request.form)
    maestro = Maestros.query.all()
    return render_template("maestros/listadoMaes.html", form=create_form, maestro=maestro)
 
@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"perfil de {nombre}"
 