# When a directory contains an __init__.py file, Python treats the directory as a package.
# The code in the __init__.py file is executed when the package or one of its modules is imported.

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy #  an extension for Flask that adds support for SQLAlchemy, a popular Object Relational Mapper (ORM) for Python. SQLAlchemy allows you to interact with databases using Python classes instead of writing raw SQL queries.
from flask_admin import Admin # a Flask extension that adds an administrative interface to your application. It allows you to manage your database content, users, and other aspects of the application via a web-based interface.
from .extensions import db # db is the SQLAlchemy database instance.
from .blueprints.home import home_bp
from .blueprints.auth import auth_bp
from .blueprints.webhooks import webhook_bp
from .blueprints.get_activities import activities_bp
from .admin import setup_admin
from flask_session import Session


# a typical factory function in Flask, used to create and configure a new instance of the Flask application.
# webA factory function is a function that is responsible for creating and returning instances of a class or an object.
def create_app(config_name='default'):
    
    # Create new Flask app instance
    app = Flask(__name__)

    #GENERAL CONFIGURATION
    # Load configuration
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.Config')
    
    # SESSION INITIALIZATION
    # The Session class integrates server-side session storage into Flask.
    # initializes the session system in the Flask app.
    Session(app)

    # DATABASE INITIALIZATION
    # Initialize the SQLAlchemy database extension with the Flask app
    # making the db object (imported from .models) aware of the app context.
    db.init_app(app)
    
    # ADMIN INITIALIZATION
     # Initialize Flask-Admin and set it up with the Flask app
    setup_admin(app)

    # REGISTER BLUEPRINTS
    # this separates different parts of the application (like authentication, main views, and webhooks) for better organization.
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(webhook_bp, url_prefix='/webhook')
    app.register_blueprint(activities_bp)

    # Create database tables
    with app.app_context():
        # ensures that all tables defined in your SQLAlchemy models are created in the database if they don't already exist.
        db.create_all()
        

    # db.session.commmit()

    return app
