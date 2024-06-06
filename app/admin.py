from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, User

def setup_admin(app):
    admin = Admin(app, name='Strava App Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
