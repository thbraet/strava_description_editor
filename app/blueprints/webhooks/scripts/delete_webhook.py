import os
import requests


subscription_id = 259375
client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")

# Make the DELETE request to delete the webhook
response = requests.delete(
    f'https://www.strava.com/api/v3/push_subscriptions/{subscription_id}',
    params={
        'client_id': client_id,
        'client_secret': client_secret
    }
)

# Check if the deletion was successful
if response.status_code == 204:
    print(f"Webhook {subscription_id} deleted successfully.")
else:
    print(f"Failed to delete webhook: {response.json()}")