from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig


from maestros.routes import maestros
from alumnos.routes import alumnos
from cursos.routes import cursos
from consultas.routes import inscripciones # Importamos el objeto blueprint

import forms
from models import db, Alumnos, Maestros, Cursos # Cursos en plural

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Registro de Blueprints
app.register_blueprint(maestros)
app.register_blueprint(alumnos)
app.register_blueprint(cursos)
app.register_blueprint(inscripciones)

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/", methods=["GET", "POST"])
@app.route("/principal")
def index():
    create_form = forms.UserForm2(request.form)
    alumnos_list = Alumnos.query.all()
    return render_template("principal.html", form=create_form, alumno=alumnos_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()