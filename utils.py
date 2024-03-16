import os
import requests
import requests_cache

from typing import Dict, Any

requests_cache.install_cache('api_cache', expire_after=3600)


def get_zoom_token() -> Dict[str, Any]:
    """Gets the Zoom API token"""
    account_id = os.environ['ZOOM_ACCOUNT_ID']
    client_id = os.environ['ZOOM_CLIENT_ID']
    client_secret = os.environ['ZOOM_CLIENT_SECRET']

    params = {
        "grant_type": "account_credentials",
        "account_id": account_id,
    }

    response = requests.post('https://api.zoom.us/oauth/token', params=params, auth=(client_id, client_secret))

    token = response.json().get('access_token')

    return token