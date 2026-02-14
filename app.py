from flask import Flask, render_template,request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
 
from models import db
from models import Alumnos
 
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
 
 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route("/", methods=['GET', 'POST'])
@app.route("/index")
def index():
    create_form = forms.UserForm(request.form)
    
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumno=alumno)
 
@app.route("/Alumnos")
def alumnos():
    return render_template("Alumnos.html")
 
if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
 
    with app.app_context():
        db.create_all()
 
    app.run(debug=True)
 