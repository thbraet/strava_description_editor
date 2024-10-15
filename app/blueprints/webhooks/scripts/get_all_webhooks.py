import os
import requests


# Replace these with your actual Client ID and Client Secret
client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")



# Make the request to get all registered webhooks
response = requests.get(
    'https://www.strava.com/api/v3/push_subscriptions',
    params={
        'client_id': client_id,
        'client_secret': client_secret
    }
)



# Check the response status and print the list of webhooks
if response.status_code == 200:
    subscriptions = response.json()
    if subscriptions:
        print("Registered Webhooks:")
        for subscription in subscriptions:
            print(subscription)
    else:
        print("No webhooks registered.")
else:
    print(f"Failed to retrieve webhooks: {response.json()}")
