from typing import Optional, Dict, Any, Union
from flask import session, Response as FlaskResponse, current_app as app
import requests
from requests import Response as RequestsResponse
from .get_session_user import get_session_user
from .get_access_token import get_access_token
from .login_required import login_required

def make_strava_request(
    url: str,
    method: str = 'GET',
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Union[RequestsResponse, FlaskResponse]:
    """
    Make a request to the Strava API using the access token of the authenticated user.

    Parameters:
    - url: The endpoint to call.
    - method: HTTP method (GET, POST, PUT, DELETE).
    - data: The data to send in the request body (for POST/PUT).
    - params: The URL parameters to send in the request.

    Returns:
    - A requests.Response or FlaskResponse depending on success/failure.
    """

    app.logger.debug(f"Making Strava API request: {method} {url}")
    app.logger.debug(f"Data: {data}, Params: {params}, Session: {session}")

   
    user = get_session_user()    
    if not user:
        app.logger.error("Failed to get authenticated user")
        return FlaskResponse("Authentication failed", status=401)
    
    access_token = get_access_token(user)
    
    if not access_token:
        app.logger.error("Failed to get access token for user")
        return FlaskResponse("Authentication failed", status=401)

    headers = {'Authorization': f'Bearer {access_token}'}

    # Map HTTP methods to request functions
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            app.logger.error(f"Unsupported HTTP method: {method}")
            return FlaskResponse(f"Unsupported HTTP method: {method}", status=405)

        # Log the status and response content
        app.logger.debug(f"Response status: {response.status_code}")
        app.logger.debug(f"Response content: {response.text}")
        
        # Raise an error for bad responses (4xx, 5xx)
        response.raise_for_status()

    except requests.RequestException as e:
        app.logger.error(f"Error while making Strava API request: {e}")
        return FlaskResponse(f"Error contacting Strava API: {e}", status=500)

    return response
