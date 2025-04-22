import unittest
from datetime import datetime

import polars as pl

from strava_data_analyser.analyser.polars_analyzer import PolarsAnalyzer


class PolarsAnalyzerOverviewTest(unittest.TestCase):

    def test_get_overview_without_result(self):
        # Given summaries on year 2023
        summaries = pl.DataFrame({
            "start_date": [datetime(2023, 1, 1), datetime(2023, 2, 1)],
            "type": ["Run", "Bike"],
            "distance": [1000, 2000],
            "moving_time": [3600, 7200]
        })
        details = pl.DataFrame({})
        analyser = PolarsAnalyzer(summaries, details)

        # When I request overview for year 2022
        overview = analyser.get_overview(year=2022)

        # Then I expect the overview to be empty
        self.assertEqual(overview, [])

    def test_get_overview_without_year(self):
        # Given summaries on year 2023
        summaries = pl.DataFrame({
            "start_date": [datetime(2023, 1, 1), datetime(2023, 2, 1), datetime(2023, 3, 1)],
            "type": ["Run", "Bike", "Run"],
            "distance": [1000, 2000, 3000],
            "moving_time": [3600, 7200, 5400]
        })
        # and empty details (no need of it)
        details = pl.DataFrame({})
        analyser = PolarsAnalyzer(summaries, details)

        # When I request overview without year
        overview = analyser.get_overview()

        # Then I have overview for running :
        running_overview = [runs for runs in overview if runs["type"] == "Run"][0]
        self.assertEqual(running_overview,
                         {'type': 'Run',
                          'count_distance': 2,
                          'sum_distance': '4.0km',
                          'mean_distance': '2.0km',
                          'sum_moving_time': '02:30:00',
                          'mean_moving_time': '01:15:00'
                          })
        # And I have overview for biking :
        biking_overview = [bikes for bikes in overview if bikes["type"] == "Bike"][0]
        self.assertEqual(biking_overview, {
            'type': 'Bike',
            'count_distance': 1,
            'sum_distance': '2.0km',
            'mean_distance': '2.0km',
            'sum_moving_time': '02:00:00',
            'mean_moving_time': '02:00:00'
        })


class PolarsAnalyzerActivityTest(unittest.TestCase):

    def test_analyse_activity(self):
        # Given details on year 2023
        details = pl.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "start_date": [
                datetime(2024, 1, 1),
                datetime(2024, 2, 1),
                datetime(2024, 3, 1),
                datetime(2025, 1, 1),
                datetime(2025, 2, 1)
            ],
            "type": ["Run", "Run", "Run", "Run", "Run"],
            "distance": [10000, 8000, 12000, 20000, 10000],
            "moving_time": [3600, 3000, 4000, 7200, 3000],
            "average_speed": [float(2.77), float(2.66), float(3), float(2.77), float(3.33)],
            "total_elevation_gain": [100, 50, 30, 20, 0]
        })
        # and empty summaries (no need of it)
        summaries = pl.DataFrame({})
        analyser = PolarsAnalyzer(summaries, details)

        # When I request analysis for activity with id 1
        activity = analyser.analyse_activity(1, _start_date=datetime(2024, 6, 1))

        # Then I expect the activity to be analysed correctly
        self.assertEqual(activity['overall'], {
            'description': 'Overall',
            'count': 5,
            'distance': {'percentile': 60, 'rank': 3},
            'duration': {'percentile': 60, 'rank': 3},
            'speed': {'percentile': 60, 'rank': 3},
            'elevation': {'percentile': 100, 'rank': 1}
        })
        self.assertEqual(activity['yoy'], {
            'description': 'From 2023-06-01 00:00:00 to 2024-06-01 00:00:00',
            'count': 3,
            'distance': {'percentile': 67, 'rank': 2},
            'duration': {'percentile': 67, 'rank': 2},
            'speed': {'percentile': 67, 'rank': 2},
            'elevation': {'percentile': 100, 'rank': 1}
        })

        self.assertEqual(activity['distance_range'], {
            'description': 'Distance range [10000, 15000[',
            'count': 3,
            'distance': {'percentile': 67, 'rank': 2},
            'duration': {'percentile': 67, 'rank': 2},
            'speed': {'percentile': 33, 'rank': 3},
            'elevation': {'percentile': 100, 'rank': 1}
        })
