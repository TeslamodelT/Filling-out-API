from flask import Blueprint
from . import routes

loans_bp = Blueprint("loans_bp", __name__)