from flask import render_template
from ..functions.get_activities_dataframe import get_activities_dataframe
from ..functions.plot_calendar import plot_calendar
from ...auth.functions import get_authenticated_user
from .. import charts_bp


@charts_bp.route('/calendar')
def calendar():
    """
    This route renders a page with a button to authorize the app with Strava.
    Clicking the button redirects the user to Strava's authorization page.
    """
    # Construct the URL for Strava's authorization endpoint
    user, redirect_response = get_authenticated_user()
    if redirect_response:
        return redirect_response

    activities_df = get_activities_dataframe()

    # Call the plot_calendar function to generate the calendar heatmap
    plot_calendar(activities_df)

    return render_template('image.html')
