import logging

from dotenv import load_dotenv

from extraction.strava import Strava
from storage.storage import Storage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

storage = Storage()

last_activity_date = storage.get_last_activity_date()
logger.info(f"Last activity date is {last_activity_date}")

strava = Strava()

_list = [
    {
        'summary': summary,
        'detail': detail
    }
    for summary in strava.get_summaries_since(last_activity_date) # todo exclude this date
    if (detail := strava.get_detail(summary['id'])) is not None
]

logger.info("Found %d new activities", len(_list))

for item in _list:
    summary_ = item['summary']
    logger.info("saving activity %s", summary_['id'])
    storage.upload_summary(f"{summary_['id']}.json", summary_)
    detail_ = item['detail']
    storage.upload_detail(f"{detail_['id']}.json", detail_)

last_activity_date = _list[-1]['summary']['start_date']
logger.info(f"Last activity date is now {last_activity_date}")

