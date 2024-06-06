import os
from flask import Flask, render_template, request, session, url_for, redirect
import requests

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(24)  # You can also set this to a fixed value for consistency


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
    # Generate the authorization URL (replace with your actual implementation)
    authorization_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&redirect_uri={url_for('callback', _external=True)}&response_type=code&scope=read,activity:read_all"
    
    print(authorization_url)

    return render_template('strava.html', authorization_url=authorization_url)

@app.route('/callback')
def callback():
    print("Callback")
    print(requests.args)
    code = request.args.get('code')
    print(code)
    token_url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=payload)
    response_data = response.json()
    print(response_data)
    print(response_data["access_token"])
    session['access_token'] = response_data['access_token']
    session['refresh_token'] = response_data['refresh_token']
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    print("Before print")
    print(session)
    print("After print")
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
