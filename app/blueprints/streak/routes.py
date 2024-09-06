from datetime import timedelta
from app.models.models import StravaActivity
from . import streak_bp


def get_activity_dates():
    """
    Retrieves all activity start dates from the database, ordered by date.
    """
    # Query all activities ordered by start date
    activities = StravaActivity.query.order_by(StravaActivity.start_date.asc()).all()

    # Return a list of start dates
    return [activity.start_date for activity in activities]

def longest_streak(dates):
    """
    Calculates the longest streak of consecutive days with activities from a list of dates.
    """
    if not dates:
        return 0
    
    # Sort the dates in ascending order
    dates = sorted(dates, reverse=False)

    longest_streak = 0
    current_streak = 1

    # Loop through the list of dates and compare each date with the previous one
    for i in range(1, len(dates)):
        # Check if the current date is the day after the previous date
        if dates[i-1].date() + timedelta(days=1) == dates[i].date():
            current_streak += 1
        elif dates[i-1].date() == dates[i].date():
            current_streak += 0
        else:
            # If dates are not consecutive, update the longest streak if needed and reset current streak
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1

    # Return the longest streak, considering the last streak in the list
    return max(longest_streak, current_streak)

@streak_bp.route('/longest_streak')
def calculate_longest_streak():
    """
    Calculates and returns the longest streak of consecutive days with activities.
    """
    # Fetch the activity dates from the database
    activity_dates = get_activity_dates()
        
    # Calculate the longest streak of consecutive days with activities
    streak = longest_streak(activity_dates)
    
    # Return a message with the longest streak in days
    return f"The longest streak of consecutive days with activities is: {streak} days"