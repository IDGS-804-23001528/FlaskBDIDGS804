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
 
@maestros.route('/detalles', methods=['GET', 'POST'])
def detallesmaes():
    maestro_class = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')  
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
        nombre = maes1.nombre
        apellidos = maes1.apellidos
        email = maes1.email
        especialidad = maes1.especialidad
 
    return render_template("maestros/detallesmaes.html", nombre=nombre, apellidos=apellidos, email=email, especialidad=especialidad)
 
@maestros.route('/insertarmaes', methods=['GET', 'POST'])
def Registromaes():
    maestro_class = forms.UserForm(request.form)
 
    if request.method == 'POST':
        maes = Maestros(
            nombre=maestro_class.nombre.data,
            apellidos=maestro_class.apellidos.data,
            email=maestro_class.email.data,
            especialidad=maestro_class.especialidad.data
        )
 
        db.session.add(maes)
        db.session.commit()
        return redirect(url_for('maestros.listado_maestros'))  
    return render_template("maestros/insertarmaes.html", form=maestro_class)
 
@maestros.route('/modificarmaes', methods=['GET', 'POST'])
def modificarmaes():
    create_form = forms.UserForm(request.form)
 
    if request.method == 'GET':
        id = request.args.get('id')
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
 
        create_form.id.data = maes1.matricula
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.email.data = maes1.email
        create_form.especialidad.data = maes1.especialidad
 
    if request.method == 'POST':
        id = create_form.id.data  
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
 
        maes1.nombre = str.rstrip(create_form.nombre.data)
        maes1.apellidos = create_form.apellidos.data
        maes1.email = create_form.email.data
        maes1.especialidad = create_form.especialidad.data
 
        db.session.commit()
        return redirect(url_for('maestros.listado_maestros'))
 
    return render_template("maestros/modificarmaes.html", form=create_form)
 
@maestros.route('/eliminarmaes', methods=['GET', 'POST'])
def eliminarmaes():
    create_form = forms.UserForm(request.form)
 
    if request.method == 'GET':
        id = request.args.get('id')  
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
 
        create_form.id.data = maes1.matricula
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.email.data = maes1.email
        create_form.especialidad.data = maes1.especialidad
 
    if request.method == 'POST':
        id = create_form.id.data
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
        db.session.delete(maes1)
        db.session.commit()
        return redirect(url_for('maestros.listado_maestros'))
 
    return render_template("maestros/eliminarmaes.html", form=create_form)