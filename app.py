from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template('strava.html')

if __name__ == '__main__':
    app.run(debug=True)
