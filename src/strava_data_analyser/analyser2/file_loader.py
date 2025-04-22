import pandas as pd
from pandas import DataFrame

from strava_data_analyser.storage.storage import Storage

storage = Storage()


def load_summary_activities(year: int = None) -> DataFrame:
    """
    :param year: the year requested
    :return: athlete activities as a Dataframe. Activities are filtered by year, if provided.
    """
    activities = _read_summary_activities_file()  # TODO filter the date here !

    if year is not None:
        activities = activities.loc[
            (activities['start_date'] >= f'{year}-01-01') & (activities['start_date'] < f'{year + 1}-01-01')]
    return activities


def load_detailed_activities(year: int = None, type: str = None):
    activities = _read_detailed_activities_files()

    # activities['start_time'] = activities['start_date_local'].apply(
    #     lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").time()
    # )

    if year is not None:
        activities = activities.loc[
            (activities['start_date'] >= f'{year}-01-01') & (activities['start_date'] < f'{year + 1}-01-01')]
    if type is not None:
        activities = activities.loc[(activities['type'] == type)]

    return activities


def _read_summary_activities_file() -> DataFrame:
    _files = storage.load_summary_activities()
    _summaries = pd.DataFrame.from_dict(_files)
    return _summaries


def _read_detailed_activities_files() -> DataFrame:
    _files = storage.load_detailed_activities()
    _activities = pd.DataFrame.from_dict(_files)
    return _activities



