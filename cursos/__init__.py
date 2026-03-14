from flask import Blueprint

cursos = Blueprint(
    'cursos',
    __name__,
    template_folder='templates'
)

from . import routes