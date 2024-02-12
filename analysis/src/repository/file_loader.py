import json
from datetime import datetime
from os import walk
from pathlib import Path

import pandas as pd

activity_file_path = "../../../.tmp/athlete_activities.json"
detailed_activity_path = "../../../.tmp/activities"


def load_athlete_activities(year: int = None):
    """
    :param year: the year requested
    :return: athlete activities as a Dataframe. Activities are filtered by year, if provided.
    """
    activities = _read_activities_file()

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


def _read_activities_file():
    return pd.read_json(activity_file_path, convert_dates=['start_date'])


def _read_detailed_activities_files():
    files = _read_json_files(detailed_activity_path)
    activities = pd.DataFrame.from_dict(files)
    return activities


def _read_json_files(path: str):
    """
    Read json files in a directory
    :param path:
    :return: the content of each file.
    """
    content = []
    for file_name in _list_files(path):
        txt = Path(f"{path}/{file_name}").read_text(encoding='utf-8')
        data = json.loads(txt)
        content.append(data)

    return content


def _list_files(directory: str):
    """
    List directory's files name
    :param directory:
    :return: Returns all files name in the directory
    """
    return next(walk(directory), (None, None, []))[2]
