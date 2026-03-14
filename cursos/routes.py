import forms
from models import db, Cursos, Maestros, Alumnos, Inscripcion
from . import cursos
from flask import render_template, request, redirect, url_for, flash

@cursos.route("/cursos", methods=["GET", "POST"])
def listado():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestros]
    
    curso = Cursos.query.all()
    return render_template("cursos/listadoCur.html", form=create_form, curso=curso, maestros=maestros)

@cursos.route("/cursos/insertar", methods=["GET", "POST"])
def insertar():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestros]
    
    if request.method == 'POST' and create_form.validate_on_submit():
        curso = Cursos(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )
        db.session.add(curso)
        db.session.commit()
        return redirect(url_for("cursos.listado"))
        
    return render_template("cursos/insertar.html", form=create_form, maestros=maestros)

@cursos.route("/cursos/detalles", methods=["GET"])
def detalles():
    id_curso = request.args.get('id')
    curso = Cursos.query.get(id_curso)
    if not curso:
        return redirect(url_for('cursos.listado'))
        
    alumnos = db.session.query(Alumnos)\
        .join(Inscripcion, Alumnos.id == Inscripcion.alumno_id)\
        .filter(Inscripcion.curso_id == id_curso)\
        .all()
    maestro = Maestros.query.filter_by(matricula=curso.maestro_id).first()
    
    return render_template("cursos/detalles.html", id=id_curso, nombre=curso.nombre, maestro=maestro, alumnos=alumnos)

@cursos.route("/cursos/asignar", methods=["GET", "POST"])
def asignar():
    id_curso = request.args.get('id') or request.form.get('curso_id')
    curso = Cursos.query.get(id_curso)
    form = forms.AsignarAlumnoForm(request.form)
    
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in Alumnos.query.all()]

    if form.validate_on_submit():
        alumno = Alumnos.query.get(form.alumno_id.data)
        if alumno and alumno not in curso.alumnos:
            curso.alumnos.append(alumno)
            db.session.commit()
        return redirect(url_for("cursos.asignar", id=id_curso))

    return render_template("cursos/asignar.html", form=form, id=id_curso, alumnos=curso.alumnos)

@cursos.route("/cursos/modificar", methods=["GET", "POST"])
def modificar():
    id_curso = request.args.get('id') or request.form.get('id')
    curso = Cursos.query.get(id_curso)
    create_form = forms.CursoForm(request.form)
    
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestros]

    if request.method == "GET" and curso:
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id

    if request.method == 'POST' and create_form.validate_on_submit():
        if curso:
            curso.nombre = create_form.nombre.data
            curso.descripcion = create_form.descripcion.data
            curso.maestro_id = create_form.maestro_id.data
            db.session.commit()
        return redirect(url_for("cursos.listado"))

    return render_template("cursos/modificar.html", form=create_form, id=id_curso, maestros=maestros)

@cursos.route("/cursos/eliminar", methods=["GET", "POST"])
def eliminar():
    id_curso = request.args.get('id') or request.form.get('id')
    curso = Cursos.query.get(id_curso)
    create_form = forms.CursoForm(request.form)
    
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestros]

    if request.method == "GET" and curso:
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id

    if request.method == "POST" and curso:
        Inscripcion.query.filter_by(curso_id=id_curso).delete()
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for("cursos.listado"))
        
    return render_template("cursos/eliminar.html", form=create_form, id=id_curso, maestros=maestros)


@cursos.route("/cursos/desasignar", methods=["POST"])
def desasignar():
    id_curso = request.form.get('curso_id')
    id_alumno = request.form.get('alumno_id')
    
    curso = Cursos.query.get(id_curso)
    alumno = Alumnos.query.get(id_alumno)
    
    if curso and alumno:
        if alumno in curso.alumnos:
            curso.alumnos.remove(alumno)
            db.session.commit()
            
    return redirect(url_for("cursos.asignar", id=id_curso))