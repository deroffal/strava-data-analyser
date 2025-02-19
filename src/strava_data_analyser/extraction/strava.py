import logging
import os

from .strava_providers import StravaClient, StravaStub

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Strava:

    def __init__(self):
        self.client = StravaStub() if os.getenv("ENV") != "production" else StravaClient()

    def get_summaries_since(self, date):
        return self.client.get_summaries_since(date)

    def get_detail(self, activity_id):
        return self.client.get_detail(activity_id)
