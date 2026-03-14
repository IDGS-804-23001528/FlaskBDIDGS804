from flask import render_template, request, Blueprint
from models import db, Cursos, Alumnos # Importación correcta en plural

# El nombre del blueprint debe ser 'inscripciones' para que coincida con url_for en layout.html
inscripciones = Blueprint('inscripciones', __name__)

@inscripciones.route("/consultas", methods=['GET'])
def index():
    # 1. Obtenemos todos los registros de la base de datos
    todos_cursos = Cursos.query.all()
    todos_alumnos = Alumnos.query.all()

    # 2. Inicializamos las variables de selección
    curso_seleccionado = None
    alumno_seleccionado = None

    # 3. Capturamos los parámetros de la URL (?curso_id=... o ?alumno_id=...)
    curso_id = request.args.get('curso_id')
    alumno_id = request.args.get('alumno_id')

    # 4. Buscamos el objeto específico si existe el ID
    if curso_id:
        curso_seleccionado = Cursos.query.get(curso_id)
    
    if alumno_id:
        alumno_seleccionado = Alumnos.query.get(alumno_id)

    # 5. Renderizado del template
    # Asegúrate de que tu archivo esté en: templates/consultas/consultar.html
    return render_template(
        "consultas/consultar.html", 
        todos_cursos=todos_cursos,
        todos_alumnos=todos_alumnos,
        curso_seleccionado=curso_seleccionado,
        alumno_seleccionado=alumno_seleccionado
    )