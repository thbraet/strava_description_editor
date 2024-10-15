from datetime import timedelta


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
