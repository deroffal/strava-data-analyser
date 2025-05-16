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
            "total_elevation_gain": [100, 50, 30, 20, 0],
            "best_efforts": [
                [
                    {'name': '400m', 'moving_time': 60},
                    {'name': '800m', 'moving_time': 120},
                    {'name': '1K', 'moving_time': 240}
                ],
                [
                    {'name': '400m', 'moving_time': 50},
                    {'name': '800m', 'moving_time': 100},
                    {'name': '1K', 'moving_time': 200}
                ],
                [
                    {'name': '400m', 'moving_time': 40},
                    {'name': '800m', 'moving_time': 80},
                    {'name': '1K', 'moving_time': 160}
                ],
                [
                    {'name': '400m', 'moving_time': 30},
                    {'name': '800m', 'moving_time': 60},
                    {'name': '1K', 'moving_time': 120}
                ],
                [
                    {'name': '400m', 'moving_time': 20},
                    {'name': '800m', 'moving_time': 40},
                    {'name': '1K', 'moving_time': 80}
                ]
            ]
        })
        # and empty summaries (no need of it)
        summaries = pl.DataFrame({})
        analyser = PolarsAnalyzer(summaries, details)

        # When I request analysis for activity with id 1
        activity = analyser.analyse_activity(1, _start_date=datetime(2024, 6, 1))

        # Then I expect the activity to be analysed correctly
        self.assertEqual(activity['overall'], {
            'description': 'Overall',
            'distance': {'percentile': 60, 'rank': 3, 'total': 5},
            'duration': {'percentile': 60, 'rank': 3, 'total': 5},
            'speed': {'percentile': 60, 'rank': 3, 'total': 5},
            'elevation': {'percentile': 100, 'rank': 1, 'total': 5},
            'best_efforts': [
                {'effort': {'percentile': 20, 'rank': 5, 'total': 5},
                 'name': '400m',
                 'value': '00:01:00'},
                {'effort': {'percentile': 20, 'rank': 5, 'total': 5},
                 'name': '800m',
                 'value': '00:02:00'},
                {'effort': {'percentile': 20, 'rank': 5, 'total': 5},
                 'name': '1K',
                 'value': '00:04:00'}
            ]
        })
        self.assertEqual(activity['yoy'], {
            'description': 'From 2023-06-01 00:00:00 to 2024-06-01 00:00:00',
            'distance': {'percentile': 67, 'rank': 2, 'total': 3},
            'duration': {'percentile': 67, 'rank': 2, 'total': 3},
            'speed': {'percentile': 67, 'rank': 2, 'total': 3},
            'elevation': {'percentile': 100, 'rank': 1, 'total': 3},
            'best_efforts': [
                {'effort': {'percentile': 33, 'rank': 3, 'total': 3},
                 'name': '400m',
                 'value': '00:01:00'},
                {'effort': {'percentile': 33, 'rank': 3, 'total': 3},
                 'name': '800m',
                 'value': '00:02:00'},
                {'effort': {'percentile': 33, 'rank': 3, 'total': 3},
                 'name': '1K',
                 'value': '00:04:00'}
            ]
        })

        self.assertEqual(activity['distance_range'], {
            'description': 'Distance range [10000, 15000[',
            'distance': {'percentile': 67, 'rank': 2, 'total': 3},
            'duration': {'percentile': 67, 'rank': 2, 'total': 3},
            'speed': {'percentile': 33, 'rank': 3, 'total': 3},
            'elevation': {'percentile': 100, 'rank': 1, 'total': 3},
            'best_efforts': [
                {'effort': {'percentile': 33, 'rank': 3, 'total': 3},
                 'name': '400m',
                 'value': '00:01:00'},
                {'effort': {'percentile': 33, 'rank': 3, 'total': 3},
                 'name': '800m',
                 'value': '00:02:00'},
                {'effort': {'percentile': 33, 'rank': 3, 'total': 3},
                 'name': '1K',
                 'value': '00:04:00'}
            ]
        })


class PolarsAnalyzerSegmentTest(unittest.TestCase):

    def test_analyse_segment_for_activity(self):
        details = pl.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "type": ["Run", "Run", "Run", "Run", "Run"],
            "segment_efforts": [
                [
                    {'id': 11, 'segment': {'id': 1, 'name': 'segment 1'}, 'moving_time': 10},
                    {'id': 12, 'segment': {'id': 2, 'name': 'segment 2'}, 'moving_time': 100},
                    {'id': 13, 'segment': {'id': 3, 'name': 'segment 3'}, 'moving_time': 100}
                ],
                [
                    {'id': 21, 'segment': {'id': 1, 'name': 'segment 1'}, 'moving_time': 12},
                    {'id': 22, 'segment': {'id': 4, 'name': 'segment 4'}, 'moving_time': 100},
                ],
                [
                    {'id': 31, 'segment': {'id': 1, 'name': 'segment 1'}, 'moving_time': 9},
                    {'id': 32, 'segment': {'id': 1, 'name': 'segment 1'}, 'moving_time': 8},
                    {'id': 33, 'segment': {'id': 1, 'name': 'segment 1'}, 'moving_time': 9},
                    {'id': 34, 'segment': {'id': 1, 'name': 'segment 1'}, 'moving_time': 11}
                ],
                [
                    {'id': 41, 'segment': {'id': 2, 'name': 'segment 2'}, 'moving_time': 100},
                ],
                [
                ],
            ],
        })

        summaries = pl.DataFrame({})
        analyser = PolarsAnalyzer(summaries, details)

        result = analyser.analyse_segment_for_activity(3, 1)

        print(result)

        self.assertEqual(result['count'], {
            'overall': 6,
            'activity': 4
        })

        self.assertEqual(result['moving_time_percentile'], {
            'percentile': 100,
            'rank': 1,
            'total': 6
        })
