import polars as pl

from strava_data_analyser.analyser.statistics import _get_percentile_for, BetterWhen
from strava_data_analyser.view import data_format

efforts_tracked = ['400m', '800m', '1K', '5K', '10K', '15K', '20K', 'Half-Marathon', '30' 'Marathon', '50k']


def get_efforts_statistics(_details_df, _activity_efforts: dict) -> list[dict]:
    """
    Compare the best efforts of the activity with the best efforts of all activities
    :param _details_df: the dataframe containing the details of all activities
    :param _activity_efforts: all the activity efforts
    :return:
    """
    _activity_efforts = _filter_tracked_efforts(_activity_efforts)
    return [
        _compute_statistics_for_effort(_details_df, _effort)
        for _effort in _activity_efforts
    ]


def _filter_tracked_efforts(efforts_: dict) -> list[dict]:
    """
    Filtering only the relevant efforts
    :param efforts_:
    :return:
    """
    return [
        _effort
        for _effort in efforts_
        if _effort['name'] in efforts_tracked
    ]


def _compute_statistics_for_effort(_details_df, _effort: dict) -> dict:
    """
    Rank a given effort among all same efforts
    :param _details_df:
    :param _effort:
    :return:
    """
    _best_effort_df = (
        _details_df.explode("best_efforts")
        .filter(pl.col("best_efforts").struct.field("name") == _effort['name'])
    )
    effort_percentile = _get_percentile_for(_best_effort_df,
                                            pl.col("best_efforts").struct.field("moving_time"),
                                            _effort['moving_time'],
                                            BetterWhen.LOW
                                            )

    return {
        'name': _effort['name'],
        'value': data_format.seconds_as_hhmmss(_effort['moving_time']),
        'effort': effort_percentile
    }
