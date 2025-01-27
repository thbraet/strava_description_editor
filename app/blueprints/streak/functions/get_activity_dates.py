from ....models.strava.detailed_activity import DetailedActivity

def get_activity_dates():
    """
    Retrieves all activity start dates from the database, ordered by date.
    """
    # Query all activities ordered by start date
    activities = DetailedActivity.query.order_by(DetailedActivity.start_date.asc()).all()

    # Return a list of start dates
    return [activity.start_date for activity in activities]