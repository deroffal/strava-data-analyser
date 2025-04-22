import json
from datetime import datetime

from .local_storage_provider import LocalStorageProvider


class Storage:
    # ex: 2025-06-12T18:00:39Z
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, provider=None):
        self.provider = provider if provider is not None else LocalStorageProvider()

    def get_summaries_location(self):
        return self.provider.summary_activity_file_path

    def get_details_location(self):
        return self.provider.detailed_activity_path

    def get_last_activity_date(self):
        activity = self.provider.get_last_activity()
        _last_activity = json.loads(activity)
        _date = _last_activity['start_date']
        return datetime.strptime(_date, self.DATE_FORMAT)

    def upload_summary(self, _name, _data):
        return self.provider.upload_summary(_name, json.dumps(_data))

    def upload_detail(self, _name, _data):
        return self.provider.upload_detail(_name, json.dumps(_data))

    def load_summary_activities(self, _year: int = None):
        return self.provider.load_summary_activities(_year)

    def load_detailed_activities(self, _year: int = None, _type: str = None):
        return self.provider.load_detailed_activities(_year, _type)
