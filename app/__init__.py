from flask import Flask

# Import models
from app.models.strava.detailed_athlete import DetailedAthlete
from .models.strava.user_tokens import UserTokens

# Import Flask-Admin
from flask_admin import Admin

# Import additional models and extensions
from .models.strava.detailed_activity import DetailedActivity 
from .extensions import db 
from .blueprints.home import home_bp
from .blueprints.auth import auth_bp
from .blueprints.webhooks import webhook_bp
from .blueprints.activities import activities_bp
from .blueprints.streak import streak_bp
from .blueprints.charts import charts_bp
from flask_session import Session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

def create_app(config_name='default'):
    """
    Create and configure the Flask application.

    Args:
        config_name (str): The configuration name to use. Defaults to 'default'.

    Returns:
        Flask: The configured Flask application instance.
    """
    
    # Create new Flask app instance
    app = Flask(__name__)

    # Load configuration based on the provided config_name
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.Config')
    
    # Initialize Flask-Session
    Session(app)
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize Flask-Admin
    admin = Admin(app, name='Strava App Admin')
    
    # Add views to Flask-Admin for managing UserTokens, DetailedActivity, and DetailedAthlete models
    admin.add_view(ModelView(UserTokens, db.session))
    admin.add_view(ModelView(DetailedActivity, db.session))
    admin.add_view(ModelView(DetailedAthlete, db.session))

    # Register blueprints for different parts of the application
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(streak_bp)
    app.register_blueprint(charts_bp)

    # Create all database tables within the app context
    with app.app_context():
        db.create_all()

    return app
