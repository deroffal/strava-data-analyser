import logging
import os

import requests
from strava_data_analyser.utils.oauth2 import OAuth2

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StravaClient:

    def __init__(self):
        _oauth2 = OAuth2(
            "https://www.strava.com/oauth/authorize",
            "https://www.strava.com/oauth/token",
            os.getenv("STRAVA_CLIENT_ID"),
            os.getenv("STRAVA_CLIENT_SECRET"),
            response_type="code",
            scope="read_all,activity:read_all,profile:read_all", approval_prompt="auto",
            grant_type="authorization_code"
        )
        self.strava_token = _oauth2.get_access_token()
        self.url = "https://www.strava.com"

    def get_summaries_since(self, date):
        date = int(date.timestamp())

        headers = {"Authorization": f"Bearer {self.strava_token}"}
        response = requests.request(
            "GET",
            f"{self.url}/api/v3/athlete/activities?per_page=100&after={date}",
            headers=headers
        )
        if response.status_code == 200:
            logger.info("returning summaries...")
            return response.json()
        else:
            logger.error(f"Error: {response.status_code}")
            return []

    def get_detail(self, activity_id):
        url = f"{self.url}/api/v3/activities/{activity_id}"

        headers = {"Authorization": f"Bearer {self.strava_token}"}

        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            logger.info(f"returning activity {activity_id}")
            return response.json()
        else:
            logger.error(f"Error: {response.status_code}")
        return None

class StravaStub:

    def get_summaries_since(self, date):
        return [
            {
                "id": "1",
                "start_date": "2024-10-07T10:22:23Z"
            },
            {
                "id": "2",
                "start_date": "2025-06-12T18:00:39Z"
            }
        ]

    def get_detail(self, activity_id):
        if activity_id == "1":
            return {"id": "1"}
        elif activity_id == "2":
            return {"id": "2"}
        else:
            return None
