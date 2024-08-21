import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from .models import FoodCalories, db
from .views import main_bp
from .auth import auth_bp
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
    app.register_blueprint(auth_bp)
    app.register_blueprint(webhook_bp, url_prefix='/webhook')

    # Create database tables
    with app.app_context():
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
