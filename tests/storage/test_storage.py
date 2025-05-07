import unittest
from datetime import datetime
from unittest.mock import Mock

from strava_data_analyser.storage.storage import Storage

class StorageTest(unittest.TestCase):
    mockProvider = Mock()
    cut = Storage(provider=mockProvider)

    def test_get_last_activity_date(self):
        self.mockProvider.get_last_activity.return_value = """{"start_date": "2000-01-01T00:00:00Z"}"""
        _last_activity_date = self.cut.get_last_activity_date()

        self.assertEqual(datetime.strftime(_last_activity_date, "%Y-%m-%dT%H:%M:%SZ"), "2000-01-01T00:00:00Z")
