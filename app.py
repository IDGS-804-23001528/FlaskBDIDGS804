from flask import Flask, render_template,request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from maestros.routes import maestros
import forms

from flask_migrate import Migrate
 
from models import db
from models import Alumnos
 
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros)
db.init_app(app)
migrate = Migrate(app,db)
csrf=CSRFProtect()
 
@app.route("/",methods=['GET','POST'])
@app.route("/index")
def index():
    create_form=forms.UserForm(request.form)
    alumno=Alumnos.query.all()
    return render_template("index.html",form=create_form,alumno=alumno)
 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
 
@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    alumno_class=forms.UserForm(request.form)
    if request.method=='POST':
        alum=Alumnos(nombre=alumno_class.nombre.data,
               apellidos=alumno_class.apellidos.data,
               email=alumno_class.email.data,
               telefono=alumno_class.telefono.data)
        
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("Alumnos.html", form=alumno_class)
 
@app.route('/detalles', methods=['GET', 'POST'])
def detalles():
    alumno_class=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alumn1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        nombre=alumn1.nombre
        apellidos=alumn1.apellidos
        email=alumn1.email
        telefono=alumn1.telefono
    return render_template("detalles.html", nombre=nombre, apellidos=apellidos, email=email, telefono=telefono)
 
 
@app.route('/modificar', methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)
 
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = alumn1.id
        create_form.nombre.data = alumn1.nombre
        create_form.apellidos.data = alumn1.apellidos
        create_form.email.data = alumn1.email
        create_form.telefono.data = alumn1.telefono
 
    if request.method == 'POST':
        id = create_form.id.data
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alumn1.nombre = str.rstrip(create_form.nombre.data)
        alumn1.apellidos = create_form.apellidos.data
        alumn1.email = create_form.email.data
        alumn1.telefono = create_form.telefono.data
        db.session.commit()
        return redirect(url_for('index'))
 
    return render_template("modificar.html", form=create_form)
 
@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
 
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = alumn1.id
        create_form.nombre.data = alumn1.nombre
        create_form.apellidos.data = alumn1.apellidos
        create_form.email.data = alumn1.email
        create_form.telefono.data = alumn1.telefono
 
    if request.method == 'POST':
        id = create_form.id.data
        alumn = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        db.session.delete(alumn)
        db.session.commit()
        return redirect(url_for('index'))
 
    return render_template("eliminar.html", form=create_form)
 
 
 
if __name__ == '__main__':
    csrf.init_app(app)
 
    with app.app_context():
        db.create_all()
 
    app.run(debug=True)