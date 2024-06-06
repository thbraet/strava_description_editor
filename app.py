import os
from flask import Flask, render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import requests

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(23)  # You can also set this to a fixed value for consistency


client_secret = "18a89f0a7b2034798129851e48a65864b1f21027"
client_id = 59692

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///strava_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strava_id = db.Column(db.Integer, unique=True, nullable=False)
    access_token = db.Column(db.String(128), nullable=False)
    refresh_token = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html', name="Thibauld")


@app.route('/about')
def about():
    return "This is the about page."

@app.route('/user/<username>')
def show_user_profile(username):
    return f"User {username}"

@app.route('/strava')
def strava():
    # The user will see a button that links to the authorization URL
    # This URL will generate a Strava prompt to approva the app gets access for the specified scope
    # If the user approves, they will get redirected to the redirect_uri, which is the /callback path in this case.
    # If the user already granted access for a specific scope, for a specific client_id, they will not have to authorize again so make sure to store their access token!
    authorization_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&redirect_uri={url_for('callback', _external=True)}&response_type=code&scope=read_all,activity:read_all,activity:write"
    
    return render_template('strava.html', authorization_url=authorization_url)

@app.route('/callback')
def callback():
    # After authorizing, you will find a code in the URI
    # This code can be exchanged for an access token
    code = request.args.get('code')
    
    if not code:
        return "Authorization failed."
    
    
    token_url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=payload)
    
    if response.status_code != 200:
        return "Failed to retrieve access token."
    
    # Contains four fields: token_type (Bearer), expires_at, expires_in, refresh_token, access_token, athlete
    #     {
    #   "token_type": "Bearer",
    #   "expires_at": 1568775134,
    #   "expires_in": 21600,
    #   "refresh_token": "e5n567567...",
    #   "access_token": "a4b945687g...",
    #   "athlete": {
    #     #{summary athlete representation}
    #   }
    # }
    response_data = response.json()

    # Store tokens and other details in the database
    strava_id = response_data['athlete']['id']
    user = User.query.filter_by(strava_id=strava_id).first()
    if not user:
        user = User(
            strava_id=strava_id,
            access_token=response_data['access_token'],
            refresh_token=response_data['refresh_token'],
            expires_at=response_data['expires_at']
        )
        db.session.add(user)
    else:
        user.access_token = response_data['access_token']
        user.refresh_token = response_data['refresh_token']
        user.expires_at = response_data['expires_at']
    db.session.commit()

    session['strava_id'] = strava_id

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    strava_id = session.get('strava_id')
    if not strava_id:
        return redirect(url_for('strava'))

    user = User.query.filter_by(strava_id=strava_id).first()
    if not user:
        return redirect(url_for('strava'))

    headers = {'Authorization': f'Bearer {user.access_token}'}

    profile_url = 'https://www.strava.com/api/v3/athlete'
    response = requests.get(profile_url, headers=headers)
    
    if response.status_code != 200:
        return "Failed to retrieve profile information."

    profile_data = response.json()

    return f"Hello, {profile_data['firstname']} {profile_data['lastname']}!"


@app.route('/update_activity', methods=['GET', 'POST'])
def update_activity():
    if request.method == 'POST':
        activity_url = request.form['activity_url']
        activity_id = activity_url.split('/')[-1]

        strava_id = session.get('strava_id')
        if not strava_id:
            return redirect(url_for('strava'))

        user = User.query.filter_by(strava_id=strava_id).first()
        if not user:
            return redirect(url_for('strava'))

        headers = {'Authorization': f'Bearer {user.access_token}'}
        activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
        response = requests.get(activity_url, headers=headers)

        if response.status_code != 200:
            return "Failed to retrieve activity details."

        activity_data = response.json()
        elevation_gain = activity_data['total_elevation_gain']

        update_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
        update_payload = {
            'description': f"Congrats, you covered {elevation_gain} meters of elevation!"
        }
        response = requests.put(update_url, headers=headers, data=update_payload)

        if response.status_code != 200:
            return "Failed to update activity description."

        return "Activity description updated successfully!"
    return render_template('update_activity.html')

# Initialize Flask-Admin
admin = Admin(app, name='Strava App Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

if __name__ == '__main__':
    app.run(debug=True)
