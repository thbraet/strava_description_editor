from flask import  redirect, render_template, request, send_from_directory, session, url_for
import logging
import requests
import pandas as pd

from app.blueprints.auth.routes import get_authenticated_user
from app.blueprints.charts.calendar import plot_calendar

from ...models.models import StravaActivity, User
from ...extensions import db
from . import charts_bp

def get_activities_dataframe():
    # Query the StravaActivity model to get the start_date and distance
    activities = db.session.query(StravaActivity.start_date, StravaActivity.distance).all()

    # Convert the query results to a pandas DataFrame
    activities_df = pd.DataFrame(activities, columns=["Activity Date", "Distance"])

    # Return the DataFrame
    return activities_df

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

@charts_bp.route('/charts/<path:filename>')
def serve_chart(filename):
    # Serve files from the specified directory
    return send_from_directory('/home/thbraet/strava_description_editor/app/blueprints/charts/charts/', filename)

  