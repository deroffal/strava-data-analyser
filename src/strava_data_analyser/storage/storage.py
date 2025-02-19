import json
from datetime import datetime

from .pcloud import PCloud


class Storage:
    # ex: 2025-06-12T18:00:39Z
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, provider=None):
        self.provider = provider if provider is not None else PCloud()

    def get_last_activity_date(self):
        _last_activity = json.loads(self.provider.get_last_activity())
        _date = _last_activity['lastRecordedActivityDate']
        return datetime.strptime(_date, self.DATE_FORMAT)

    def update_last_activity_date(self, _date):
        return self.provider.update_last_activity(json.dumps({"lastRecordedActivityDate": _date}))

    def upload_summary(self, _name, _data):
        return self.provider.upload_summary( _name, json.dumps(_data))

    def upload_detail(self, _name, _data):
        return self.provider.upload_detail( _name, json.dumps(_data))
