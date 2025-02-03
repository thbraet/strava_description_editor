from .. import home_bp

@home_bp.route('/user/<username>')
def show_user_profile(username):
    """
    Display the user profile page.

    Args:
        username (str): The username of the user whose profile is to be displayed.

    Returns:
        str: A string containing the username.
    """
    # Return a simple string with the username
    return f"User {username}"