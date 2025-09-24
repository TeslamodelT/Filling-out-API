from flask import Flask
from .extensions import ma, limiter, cache
from application.models import db
from application.blueprints.members import members_bp
from application.blueprints.books import books_bp
from application.blueprints.loans import loans_bp
from application.blueprints.items import items_bp
from application.blueprints.orders import orders_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    #initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    #register blueprints
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(loans_bp, url_prefix='/loans')
    app.register_blueprint(items_bp, url_prefix='/items')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    
    return app