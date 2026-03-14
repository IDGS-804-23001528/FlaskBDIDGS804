from flask import Blueprint

consultas = Blueprint(
    'consultas',
    __name__,
    template_folder='templates'
)

from . import routes