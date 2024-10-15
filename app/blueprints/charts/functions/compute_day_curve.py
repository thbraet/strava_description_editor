# Function to compute the active curve for a given day's activity
from datetime import timedelta

import numpy as np
import pandas as pd


def compute_day_curve(row, activity_time):
    # Convert start and end times to timestamps (seconds since epoch)
    start = activity_time.at[row, 'start_time'].timestamp()
    end = activity_time.at[row, 'end_time'].timestamp()
    wday = activity_time.at[row, 'wday']  # Get the weekday of the activity
    
    # Generate a sequence of times from 00:00 to 23:59 at one-minute intervals
    time_range = pd.date_range("00:00:00", "23:59:58", freq='1T').to_pydatetime()
    
    # Create a DataFrame to store the minute-by-minute data
    result = pd.DataFrame({'time': time_range})
    
    # Create a column for the end time of each minute (for time interval comparisons)
    result['end_time'] = result['time'] + timedelta(minutes=1)
    
    # Mark the minutes when the activity was active: 1 for active, 0 for not active
    result['active'] = np.where((result['time'].astype(np.int64) // 10**9 > start) & 
                                (result['end_time'].astype(np.int64) // 10**9 < end), 1, 0)
    # Assign the weekday to each row
    result['wday'] = wday
    return result