from . import file_loader, mongo_loader


def load_activities(source: str, year: int = None):
    """
    Abstraction to load the activity data
    :param source: either 'file' for local files, or 'mongo' for mongodb database
    :param year: the year of activities to load (default: None = all activities)
    :return: the dataframe of activities
    """
    if source == 'file':
        return file_loader.load_athlete_activities(year)
    elif source == 'mongo':
        return mongo_loader.find_activities(year)


def load_detailed_activities(source: str, year: int = None, type: str = None):
    """
    Abstraction to load the detailed activity data
    :param source: either 'file' for local files, or 'mongo' for mongodb database
    :param year: the year of activities to load (default: None = all activities)
    :param type: type of the activities to load (ex: Run, ...)
    :return: the dataframe of activities
    """
    if source == 'file':
        return file_loader.load_detailed_activities(year, type)
    elif source == 'mongo':
        return mongo_loader.find_detailed_activities(year, type)
