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
    
    if response.status_code != 200:
        return "Failed to retrieve profile information."

    profile_data = response.json()

    return f"Hello, {profile_data['firstname']} {profile_data['lastname']}!"


@app.route('/update_activity', methods=['GET', 'POST'])
def update_activity():
    if request.method == 'POST':
        activity_url = request.form['activity_url']
        # Extract activity ID from URL
        activity_id = activity_url.split('/')[-1]

        access_token = session.get('access_token')
        if not access_token:
            return redirect(url_for('strava'))

        # Fetch activity details
        activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(activity_url, headers=headers)

        if response.status_code != 200:
            return "Failed to retrieve activity details."

        activity_data = response.json()
        elevation_gain = activity_data['total_elevation_gain']

        # Update activity description
        update_url = f'https://www.strava.com/api/v3/activities/{activity_id}'
        update_payload = {
            'description': f"Congrats, you covered {elevation_gain} meters!"
        }
        response = requests.put(update_url, headers=headers, data=update_payload)

        if response.status_code != 200:
            return "Failed to update activity description."

        return "Activity description updated successfully!"
    return render_template('update_activity.html')



if __name__ == '__main__':
    app.run(debug=True)
