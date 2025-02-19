import unittest
from datetime import datetime
from unittest.mock import Mock

from strava_data_analyser.storage.storage import Storage

class StorageTest(unittest.TestCase):
    mockProvider = Mock()
    cut = Storage(provider=mockProvider)

    def test_get_last_activity_date(self):
        self.mockProvider.get_last_activity.return_value = """{"lastRecordedActivityDate": "2000-01-01T00:00:00Z"}"""
        _last_activity_date = self.cut.get_last_activity_date()

        self.assertEqual(datetime.strftime(_last_activity_date, "%Y-%m-%dT%H:%M:%SZ"), "2000-01-01T00:00:00Z")

    def test_update_last_activity_date(self):
        self.mockProvider.update_last_activity.return_value = True

        # given a new last activity date
        _date = "2025-02-26T14:23:35Z"

        # when I update the date :
        result = self.cut.update_last_activity_date(_date)

        # then the new value is updated
        self.mockProvider.update_last_activity.assert_called_once_with("""{"lastRecordedActivityDate": "2025-02-26T14:23:35Z"}""")
        self.assertTrue(result)
