from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import FoodCalories, db, User, StravaActivity

def setup_admin(app):
    admin = Admin(app, name='Strava App Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(StravaActivity, db.session))
    admin.add_view(ModelView(FoodCalories, db.session))
