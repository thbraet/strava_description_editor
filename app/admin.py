from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .extensions import db
from .models.models import FoodCalories, User, StravaActivity

def setup_admin(app):
    
    # Create instance of Admin class
    admin = Admin(app, name='Strava App Admin')
    
    # Add model views
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(StravaActivity, db.session))
    admin.add_view(ModelView(FoodCalories, db.session))
