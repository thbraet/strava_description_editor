
from .. import streak_bp
from ..functions.get_activity_dates import get_activity_dates
from ..functions.longest_streak import longest_streak


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