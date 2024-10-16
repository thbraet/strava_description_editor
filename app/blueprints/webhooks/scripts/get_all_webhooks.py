import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve Client ID and Client Secret from environment variables
client_secret = os.getenv("STRAVA_CLIENT_SECRET")
client_id = os.getenv("STRAVA_CLIENT_ID")

# Check if environment variables are set
if not client_secret or not client_id:
    logger.error("Environment variables STRAVA_CLIENT_SECRET and STRAVA_CLIENT_ID must be set.")
else:
    try:
        # Make the request to get all registered webhooks
        response = requests.get(
            'https://www.strava.com/api/v3/push_subscriptions',
            params={
                'client_id': client_id,
                'client_secret': client_secret
            }
        )

        # Check the response status and process the list of webhooks
        if response.status_code == 200:
            subscriptions = response.json()
            if subscriptions:
                logger.info("Registered Webhooks:")
                for subscription in subscriptions:
                    logger.info(subscription)
            else:
                logger.info("No webhooks registered.")
        else:
            response_data = response.json() if response.content else {}
            logger.error(f"Failed to retrieve webhooks: {response.status_code} - {response_data}")

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while trying to retrieve webhooks: {e}")
