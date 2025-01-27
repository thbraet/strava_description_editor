from flask import render_template, session

from .. import home_bp


@home_bp.route('/')
def home():    
    return render_template('index.html', name="<INSERT NAME>")
