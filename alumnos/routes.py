import forms 
from models import db, Alumnos, Cursos, Inscripcion
from . import alumnos
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

@alumnos.route("/alumnos", methods=["GET", "POST"])
def listado():
    create_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()
    return render_template("alumnos/listadoAlumn.html", form=create_form, alumno=alumno)

@alumnos.route("/alumnos/insertar", methods=["GET", "POST"])
def insertar():
    create_form = forms.UserForm2(request.form)
    if request.method == "POST":
        alumno = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,                       
            email=create_form.email.data,
            telefono=create_form.telefono.data
        )
        db.session.add(alumno)
        db.session.commit()
        flash("Alumno registrado con éxito", "success")
        return redirect(url_for("alumnos.listado"))
    return render_template("alumnos/insertar.html", form=create_form)

@alumnos.route("/alumnos/detalles", methods=["GET", "POST"])
def detalles():
    id = request.args.get('id')
    alumn = Alumnos.query.get(id)
    
    # Usamos la relación directa si está definida en models.py, 
    # si no, mantenemos tu consulta manual:
    cursos = db.session.query(Cursos)\
        .join(Inscripcion, Cursos.id == Inscripcion.curso_id)\
        .filter(Inscripcion.alumno_id == id)\
        .all()
        
    return render_template("alumnos/detalles.html", 
                         id=id, 
                         nombre=alumn.nombre, 
                         apellidos=alumn.apellidos, 
                         email=alumn.email, 
                         telefono=alumn.telefono, 
                         cursos=cursos)

@alumnos.route("/alumnos/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm2(request.form)
    id = request.args.get('id') if request.method == "GET" else create_form.id.data
    alumn = Alumnos.query.get(id)

    if request.method == "GET":
        create_form.id.data = alumn.id 
        create_form.nombre.data = alumn.nombre
        create_form.apellidos.data = alumn.apellidos
        create_form.email.data = alumn.email
        create_form.telefono.data = alumn.telefono
        
    if request.method == "POST":
        alumn.nombre = create_form.nombre.data
        alumn.apellidos = create_form.apellidos.data
        alumn.email = create_form.email.data        
        alumn.telefono = create_form.telefono.data        
        db.session.commit()
        flash("Datos actualizados correctamente", "success")
        return redirect(url_for("alumnos.listado"))
        
    return render_template("alumnos/modificar.html", form=create_form, id=id)

@alumnos.route("/alumnos/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm2(request.form)
    id = request.args.get('id') if request.method == "GET" else create_form.id.data
    alumn = Alumnos.query.get(id)
    
    if request.method == "GET":
        create_form.id.data = alumn.id 
        create_form.nombre.data = alumn.nombre
        create_form.apellidos.data = alumn.apellidos
        create_form.email.data = alumn.email
        create_form.telefono.data = alumn.telefono
        
    if request.method == "POST":
        # VALIDACIÓN: Verificar si el alumno tiene inscripciones antes de intentar borrar
        tiene_inscripciones = Inscripcion.query.filter_by(alumno_id=id).first()
        
        if tiene_inscripciones:
            flash(f"No se puede eliminar a {alumn.nombre} porque está inscrito en un curso. Debes eliminar su inscripción primero.", "danger")
            return redirect(url_for("alumnos.listado"))

        try:
            db.session.delete(alumn)
            db.session.commit()
            flash("Alumno eliminado satisfactoriamente", "success")
            return redirect(url_for("alumnos.listado"))
        except IntegrityError:
            db.session.rollback()
            flash("Error de integridad: No se pudo eliminar el registro.", "danger")
            return redirect(url_for("alumnos.listado"))
            
    return render_template("alumnos/eliminar.html", form=create_form, id=id)