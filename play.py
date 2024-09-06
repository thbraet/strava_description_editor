from datetime import timedelta

from flask import app


from app import app
from app.models.models import StravaActivity


def get_activity_dates():
    # Query all activity dates ordered by date
    activities = StravaActivity.query.order_by(StravaActivity.start_date.asc()).all()

    return [activity.start_date for activity in activities]

def longest_streak(dates):
    if not dates:
        return 0

    longest_streak = 0
    current_streak = 1

    # Loop through the list of dates and compare each date with the previous one
    for i in range(1, len(dates)):
        # Check if the current date is exactly 1 day after the previous date
        if dates[i] - dates[i - 1] == timedelta(days=1):
            current_streak += 1
        else:
            # If it's not consecutive, update the longest streak if necessary and reset current streak
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1

    return max(longest_streak, current_streak)

def calculate_longest_streak():
    # Fetch the activity dates from the database
    activity_dates = get_activity_dates()
    
    print(activity_dates)
    
    # Calculate the longest streak of consecutive days
    streak = longest_streak(activity_dates)
    
    return f"The longest streak of consecutive days with activities is: {streak} days"

with app.app_context():

    calculate_longest_streak()
