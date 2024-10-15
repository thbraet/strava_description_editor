
from .. import home_bp

@home_bp.route('/user/<username>')
def show_user_profile(username):
    return f"User {username}"