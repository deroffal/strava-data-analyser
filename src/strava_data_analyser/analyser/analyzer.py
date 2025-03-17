from pandas import DataFrame

from strava_data_analyser.storage import loader
from strava_data_analyser.view import data_format


class Analyzer:

    def __init__(self, source: str = 'file'):
        self.summaries: DataFrame = loader.load_activities(source)
        self.details: DataFrame = loader.load_detailed_activities(source)

    def get_overview(self, year: int = None):
        _summaries = self._get_summaries_by_year(year)

        overview = _summaries[['type', 'distance', 'moving_time']] \
            .groupby('type') \
            .agg({'distance': ['count', 'sum', 'mean'], 'moving_time': ['sum', 'mean']})

        distance_df = overview["distance"]
        moving_time_df = overview["moving_time"]

        overview = distance_df.merge(moving_time_df, on='type', suffixes=("_distance", "_moving_time"))

        overview['sum_distance_overview'] = overview['sum_distance'].apply(data_format.m_as_km)
        overview['mean_distance_overview'] = overview['mean_distance'].apply(data_format.m_as_km)
        overview['sum_moving_time_overview'] = overview['sum_moving_time'].apply(data_format.seconds_as_hhmmss)
        overview['mean_moving_time_overview'] = overview['mean_moving_time'].apply(data_format.seconds_as_hhmmss)

        result = {
            'activities_count': int(overview['count'].sum()),
            'total_seconds': int(overview['sum_moving_time'].sum()),
            'total_distance': int(overview['sum_distance'].sum()),
            'overview': overview.to_dict(orient='index')
        }
        return result

    def _get_summaries_by_year(self, year) -> DataFrame:
        if year is not None:
            return self.summaries.loc[
                (self.summaries['start_date'] >= f'{year}-01-01') & (self.summaries['start_date'] < f'{year + 1}-01-01')
                ]
        return self.summaries
