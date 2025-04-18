from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from .routes.call_routes import call_bp
    from .routes.ticket_routes import ticket_bp
    
    app.register_blueprint(call_bp, url_prefix='/api/calls')
    app.register_blueprint(ticket_bp, url_prefix='/api/tickets')
    
    return app
