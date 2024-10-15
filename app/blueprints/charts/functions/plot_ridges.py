# Function to create a ridgeline plot for Strava activities by weekdays
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from .compute_day_curve import compute_day_curve


def plot_ridges(data):
    # Process data to compute the start and end times for each activity (grouped by 'id')
    activity_time = data.groupby('id').agg({'time': [min, max]}).reset_index()
    activity_time.columns = ['id', 'start', 'end']  # Flatten multi-index columns
    
    # Convert the start and end times to just hours, minutes, and seconds (ignore the date)
    activity_time['start_time'] = pd.to_datetime(activity_time['start'].dt.strftime('%H:%M:%S'), format='%H:%M:%S')
    activity_time['end_time'] = pd.to_datetime(activity_time['end'].dt.strftime('%H:%M:%S'), format='%H:%M:%S')
    
    # Calculate the weekday from the 'start' time (Monday=1, Sunday=7)
    activity_time['wday'] = activity_time['start'].dt.weekday + 1

    # Generate a DataFrame containing minute-by-minute activity data for all activities
    plot_data = pd.concat([compute_day_curve(i, activity_time) for i in range(len(activity_time))], ignore_index=True)
    
    # Filter to keep only the rows where the activity is marked as active (active > 0)
    plot_data = plot_data[plot_data['active'] > 0].copy()
    
    # Set the weekday factor (categorical) so it's ordered from Sunday to Monday (reverse order)
    plot_data['wday'] = pd.Categorical(plot_data['wday'], categories=[7, 6, 5, 4, 3, 2, 1], ordered=True)
    
    # Define a color palette for the ridgeline plot (7 colors, one for each day of the week)
    palette = sns.color_palette("coolwarm", 7)
    
    # Create the ridgeline plot
    plt.figure(figsize=(10, 6))  # Set the figure size
    
    # Plot using seaborn's kdeplot (Kernel Density Estimation) to create ridge-like curves
    sns.kdeplot(
        data=plot_data,    # Data for the plot
        x='time',          # Time is the x-axis
        hue='wday',        # Color the ridges by the weekday
        fill=True,         # Fill under the ridges
        common_norm=False, # Do not normalize the densities together (allow varying scales)
        palette=palette,   # Use the defined color palette
        linewidth=1        # Set the line thickness
    )

    # Format the x-axis to display time in 12-hour format (AM/PM)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    
    # Set major ticks on the x-axis at 2-hour intervals
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Set the y-axis ticks and labels (map numbers to day names)
    plt.yticks([1, 2, 3, 4, 5, 6, 7], ["Sun", "Sat", "Fri", "Thu", "Wed", "Tue", "Mon"])
    
    # Turn off the grid lines for a cleaner look
    plt.grid(False)
    
    # Remove x and y axis labels (since they are self-explanatory)
    plt.xlabel(None)
    plt.ylabel(None)
    
    # Adjust the plot layout to ensure everything fits well within the figure
    plt.tight_layout()
    
    # Display the plot
    plt.show()

# Example usage:
# Assuming 'data' is your dataframe with activity data processed from Strava
# data = pd.DataFrame(...)  # Your dataframe should go here
# plot_ridges(data)
