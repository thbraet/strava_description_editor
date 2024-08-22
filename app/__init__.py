import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy #  an extension for Flask that adds support for SQLAlchemy, a popular Object Relational Mapper (ORM) for Python. SQLAlchemy allows you to interact with databases using Python classes instead of writing raw SQL queries.
from flask_admin import Admin # a Flask extension that adds an administrative interface to your application. It allows you to manage your database content, users, and other aspects of the application via a web-based interface.
from .models import FoodCalories, db # db is the SQLAlchemy database instance.
from .views import main_bp
from .auth import auth_bp
from .admin import setup_admin
from .webhooks import webhook_bp

# a typical factory function in Flask, used to create and configure a new instance of the Flask application.
def create_app():
    
    # Create new Flask app instance
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')

    # Initialize the SQLAlchemy database extension with the Flask app
    # making the db object (imported from .models) aware of the app context.
    db.init_app(app)
    
     # Initialize Flask-Admin and set it up with the Flask app
    setup_admin(app)

    # Register Blueprints
    # this separate s   different parts of the application (like authentication, main views, and webhooks) for better organization.
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(webhook_bp, url_prefix='/webhook')

    # Create database tables
    with app.app_context():
        # ensures that all tables defined in your SQLAlchemy models are created in the database if they don't already exist.
        db.create_all()
        
    foods_data = [
    {"food": "Scoop of ice cream", "calories_per_serving_unit": 150, "emoji": "🍦"},
    {"food": "Pizza slice", "calories_per_serving_unit": 300, "emoji": "🍕"},
    {"food": "Donut", "calories_per_serving_unit": 250, "emoji": "🍩"},
    {"food": "Regular beer", "calories_per_serving_unit": 150, "emoji": "🍺"}
    ]


    # # Insert the data into the table
    # for data in foods_data:
    #     food_entry = FoodCalories(**data)
    #     db.session.add(food_entry)
        
    # db.session.commmit()

    return app
