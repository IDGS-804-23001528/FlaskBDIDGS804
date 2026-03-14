from flask import Blueprint

alumnos = Blueprint(
    'alumnos',
    __name__,
    template_folder='templates'
)

from . import routes