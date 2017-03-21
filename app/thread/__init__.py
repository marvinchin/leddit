from flask import Blueprint

thread = Blueprint('thread', __name__)

from . import views
