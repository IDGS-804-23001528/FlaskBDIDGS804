import forms
from models import db, Maestros
from . import maestros 
from flask import app, render_template, request, redirect, url_for, flash

@maestros.route("/maestros", methods=["GET", "POST"])
def listado():
    create_form = forms.UserForm2(request.form)
    maestros_list = Maestros.query.all()
    return render_template("maestros/listadoMaes.html", form=create_form, maestros=maestros_list)

@maestros.route("/maestros/insertar", methods=["GET", "POST"])
def insertar():
    create_form = forms.UserForm2(request.form)
    if request.method == "POST":
        master = Maestros(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data
        )
        db.session.add(master)
        db.session.commit()
        return redirect(url_for("maestros.listado"))
    return render_template("maestros/insertar.html", form=create_form)

@maestros.route("/maestros/detalles", methods=["GET"])
def detalles():
    matricula = request.args.get('matricula')
    maester = Maestros.query.filter_by(matricula=matricula).first_or_404()
    return render_template("maestros/detalles.html", 
                           matricula=maester.matricula, 
                           nombre=maester.nombre, 
                           apellidos=maester.apellidos,
                           email=maester.email, 
                           especialidad=maester.especialidad)

@maestros.route("/maestros/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm2(request.form)
    matricula = request.args.get('matricula') or create_form.matricula.data
    master = Maestros.query.filter_by(matricula=matricula).first_or_404()

    if request.method == "GET":
        create_form.matricula.data = master.matricula 
        create_form.nombre.data = master.nombre
        create_form.apellidos.data = master.apellidos
        create_form.email.data = master.email
        create_form.especialidad.data = master.especialidad

    if request.method == "POST":
        master.nombre = create_form.nombre.data
        master.apellidos = create_form.apellidos.data
        master.email = create_form.email.data         
        master.especialidad = create_form.especialidad.data         
        db.session.commit()
        return redirect(url_for("maestros.listado"))
    
    return render_template("maestros/modificar.html", form=create_form, matricula=matricula)

@maestros.route("/maestros/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm2(request.form)
    matricula = request.args.get('matricula') or create_form.matricula.data
    master = Maestros.query.filter_by(matricula=matricula).first_or_404()

    if request.method == "GET":
        create_form.matricula.data = master.matricula 
        create_form.nombre.data = master.nombre
        create_form.apellidos.data = master.apellidos
        create_form.email.data = master.email
        create_form.especialidad.data = master.especialidad

    if request.method == "POST":
        # VALIDACIÓN: Evita el IntegrityError si tiene cursos
        if hasattr(master, 'cursos') and master.cursos:
            flash(f"Error: No se puede eliminar a {master.nombre} porque tiene cursos asignados.", "danger")
            return redirect(url_for("maestros.listado"))

        db.session.delete(master)
        db.session.commit()
        flash("Maestro eliminado exitosamente.", "success")
        return redirect(url_for("maestros.listado"))
        
    return render_template("maestros/eliminar.html", form=create_form, matricula=matricula)

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"