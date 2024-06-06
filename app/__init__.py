import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from .models import db
from .views import main_bp
from .admin import setup_admin
from .webhooks import webhook_bp

def create_app():
    # Create new Flask app instance
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    setup_admin(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(webhook_bp, url_prefix='/webhook')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
