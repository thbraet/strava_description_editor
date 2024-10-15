from .. import home_bp


@home_bp.route('/about')
def about():
    return "This is the about page."