def check_visibility(activity_data):
    """
    Checks if the activity should be hidden based on the activity type and duration.

    Conditions:
        - Hide runs that last less than 30 minutes.
        - Hide bike rides that last less than 1 hour.
        - Hide walks that last less than 2 hours.
    
    Parameters:
        activity_data (dict): The data of the activity.
    
    Returns:
        bool: True if the activity should be hidden, False otherwise.
    """

    
    # Get the type of activity (Run, Ride, Walk, etc.)
    activity_type = activity_data.get('sport_type', '')
    
    # Get the moving time (in seconds)
    moving_time = activity_data.get('moving_time', 0)
    
    # Convert time thresholds to seconds for comparison
    run_threshold = 40 * 60       # 30 minutes in seconds
    ride_threshold = 80 * 60      # 1 hour in seconds
    walk_threshold = 120 * 60     # 2 hours in seconds
    
   
    # Hide runs if moving time is less than 30 minutes
    if activity_type == 'Run' and moving_time < run_threshold:
        return True
    
    # Hide bike rides if moving time is less than 1 hour
    if activity_type == 'Ride' and moving_time < ride_threshold:
        return True

    # Hide walks if moving time is less than 2 hours
    if activity_type == 'Walk' and moving_time < walk_threshold:
        return True

    # Get all segments visited during the activity
    segment_efforts = activity_data.get('segment_efforts', [])
    
    # Check if the segment to hide is in the activity's segment efforts
    segment_hides_activity = any(segment['segment']['id'] == 10448145 for segment in segment_efforts)
    if segment_hides_activity:
        return True
    
    
    # If none of the conditions are met, don't hide the activity
    return False