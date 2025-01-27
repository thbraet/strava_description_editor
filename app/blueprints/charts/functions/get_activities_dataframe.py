import pandas as pd
from ....models.strava.detailed_activity import DetailedActivity
from ....extensions import db

def get_activities_dataframe():
    # Query the StravaActivity model to get the start_date and distance
    activities = db.session.query(DetailedActivity.start_date, DetailedActivity.distance).all()

    # Convert the query results to a pandas DataFrame
    activities_df = pd.DataFrame(activities, columns=["Activity Date", "Distance"])

    # Return the DataFrame
    return activities_df