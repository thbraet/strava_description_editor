import os
from flask import Flask, render_template, request, session, url_for, redirect
import requests

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(23)  # You can also set this to a fixed value for consistency


client_secret = "18a89f0a7b2034798129851e48a65864b1f21027"
client_id = 59692

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
    authorization_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&redirect_uri={url_for('callback', _external=True)}&response_type=code&scope=read"
    
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

    session['access_token'] = response_data['access_token']
    session['refresh_token'] = response_data['refresh_token']
    
    # Use access token to get information about athlete
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    print(session)
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    profile_url = 'https://www.strava.com/api/v3/athlete'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(profile_url, headers=headers)
    profile_data = response.json()

    return f"Hello, {profile_data['firstname']} {profile_data['lastname']}!"



if __name__ == '__main__':
    app.run(debug=True)
