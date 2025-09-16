from flask import Blueprint
from . import routes

books_bp = Blueprint("books_bp", __name__)