import datetime

import polars as pl
from dateutil.relativedelta import relativedelta

from strava_data_analyser.analyser.efforts import get_efforts_statistics
from strava_data_analyser.analyser.statistics import _get_percentile_for, BetterWhen
from strava_data_analyser.view import data_format

class PolarsAnalyzer:

    @classmethod
    def from_loader(cls, _polars_loader):
        _summaries, _details = _polars_loader.load_data()
        return cls(_summaries, _details)

    def __init__(self, summaries: pl.DataFrame, details: pl.DataFrame):
        self.summaries = summaries
        self.details = details

    def get_overview(self, year: int = None):
        df = (
            self.summaries
            .filter(
                pl.col("start_date").is_between(pl.datetime(year, 1, 1), pl.datetime(year + 1, 1, 1), 'left'))
        ) if year is not None else self.summaries

        df = (
            df
            .group_by("type")
            .agg(
                pl.col("distance").count().name.prefix("count_"),
                pl.col("distance").sum().name.prefix("sum_"),
                pl.col("distance").mean().name.prefix("mean_"),
                pl.col("moving_time").sum().name.prefix("sum_"),
                pl.col("moving_time").mean().name.prefix("mean_")
            )
        )

        _overviews = df.to_dicts()
        for _overview in _overviews:
            _overview['sum_moving_time'] = data_format.seconds_as_hhmmss(_overview['sum_moving_time'])
            _overview['mean_moving_time'] = data_format.seconds_as_hhmmss(_overview['mean_moving_time'])
            _overview['sum_distance'] = data_format.m_as_km(_overview['sum_distance'])
            _overview['mean_distance'] = data_format.m_as_km(_overview['mean_distance'])
        return _overviews

    def analyse_activity(self, _id, _start_date=datetime.date.today()):
        _activity = self._find_activity(_id)

        # just on the same type (by default)
        df_type = self.details.filter(pl.col("type") == _activity['type'])
        overall = get_details_statistics(df_type, _activity)
        overall['description'] = "Overall"

        # for 1 year
        _to = _start_date
        _from = _to - relativedelta(years=1)
        df_yoy = (df_type
                  .filter(pl.col("start_date").is_between(_from, _to, 'right'))
                  )
        yoy = get_details_statistics(df_yoy, _activity)
        yoy['description'] = f"From {_from} to {_to}"

        # same distance range ex [10k, 15k[
        lower = (_activity['distance'] // 5000) * 5000
        distance_df = (df_type
                       .filter(pl.col("distance").is_between(lower, lower + 5000, 'left'))
                       )
        distance_range = get_details_statistics(distance_df, _activity)
        distance_range['description'] = f"Distance range [{lower}, {lower + 5000}["
        return {
            "overall": overall,
            "yoy": yoy,
            "distance_range": distance_range
        }

    def analyse_segment_for_activity(self, _activity_id, _segment_id):
        effort_ = self._find_best_segment_effort(_activity_id, _segment_id)

        explode = (self.details
        # first filtering on activity with the correct segment
        .filter(
            pl.col("segment_efforts").list.eval(
                pl.element().struct.field("segment").struct.field("id") == _segment_id
            ).list.any()
        )
        # then exploding and filter on the segment efforts
        .explode("segment_efforts")
        .filter(pl.col("segment_efforts").struct.field("segment").struct.field("id") == _segment_id)
        .with_columns(
            pl.col("segment_efforts").struct.field("moving_time").alias("segment_effort_moving_time"),
        )
        )

        moving_time_percentile = _get_percentile_for(explode,
                                                     pl.col('segment_effort_moving_time'),
                                                     effort_['moving_time'],
                                                     BetterWhen.LOW
                                                     )
        return {
            "count": {
                "overall": explode.height,
                "activity": explode.filter(pl.col("id") == _activity_id).height,
            },
            "moving_time_percentile": moving_time_percentile,
        }

    def _find_best_segment_effort(self, _activity_id, _segment_id):
        """
        Find the segment effort in the activity. If there are several efforts for the same segment, take the best one (the one with the lowest moving time).
        :param _activity_id:
        :param _segment_id:
        :return:
        """
        _activity = self._find_activity(_activity_id)

        _efforts = [
            _effort
            for _effort in _activity['segment_efforts']
            if _effort['segment']['id'] == _segment_id
        ]

        if not _efforts:
            raise ValueError(f"Segment {_segment_id} not found in activity {_activity_id}")

        if _efforts.__len__() > 1:
            print("Warning: more than one effort for the same segment. Taking the best one.")

        effort_ = sorted(_efforts, key=lambda x: x['moving_time'])[0]
        print(f"Segment {effort_['segment']['name']} (id: {effort_['segment']['id']}))")
        return effort_

    def _find_activity(self, _activity_id):
        return self.details.filter(pl.col("id") == _activity_id).to_dicts()[0]

def get_details_statistics(_details_df, _activity) -> dict:
    """
    Returns various statistics for a given activity
    :param _details_df:
    :param _activity:
    :return:
    """
    distance_percentile = _get_percentile_for(_details_df, pl.col("distance"), _activity['distance'])
    moving_time_percentile = _get_percentile_for(_details_df, pl.col("moving_time"), _activity['moving_time'])
    speed_percentile = _get_percentile_for(_details_df, pl.col("average_speed"), _activity['average_speed'])
    elevation_percentile = _get_percentile_for(_details_df, pl.col("total_elevation_gain"), _activity['total_elevation_gain'])
    efforts_percentile = get_efforts_statistics(_details_df, _activity['best_efforts'])

    return {
        "distance": distance_percentile,
        "duration": moving_time_percentile,
        "speed": speed_percentile,
        "elevation": elevation_percentile,
        "best_efforts": efforts_percentile
    }
