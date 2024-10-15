import os
import requests

client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")
callback_url = 'https://1e96-80-201-144-130.ngrok-free.app/subscription'
verify_token = 'YOUR_VERIFY_TOKEN'

response = requests.post(
    'https://www.strava.com/api/v3/push_subscriptions',
    data={
        'client_id': client_id,
        'client_secret': client_secret,
        'callback_url': callback_url,
        'verify_token': verify_token
    }
)

if response.status_code == 201:
    print('Webhook registered successfully')
else:
    print('Failed to register webhook:', response.json())