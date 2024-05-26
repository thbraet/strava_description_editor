from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/user/<username>')
def show_user_profile(username):
    return f"User {username}"


if __name__ == '__main__':
    app.run(debug=True)
