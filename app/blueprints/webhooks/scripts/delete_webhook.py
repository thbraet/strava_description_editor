import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

subscription_id = 266149
client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")

# Check if environment variables are set
if not client_secret or not client_id:
    logger.error("Environment variables STRAVA_CLIENT_SECRET and STRAVA_CLIENT_ID must be set.")
else:
    try:
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
            logger.info(f"Webhook {subscription_id} deleted successfully.")
        else:
            response_data = response.json() if response.content else {}
            logger.error(f"Failed to delete webhook: {response.status_code} - {response_data}")

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while trying to delete the webhook: {e}")
