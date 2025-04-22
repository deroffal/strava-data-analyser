from pandas import DataFrame

from strava_data_analyser.analyser2.highlights import Highlight
from strava_data_analyser.analyser2 import file_loader
from strava_data_analyser.view import data_format


class Analyzer:

    def __init__(self):
        self.summaries: DataFrame = file_loader.load_summary_activities()
        self.details: DataFrame = file_loader.load_detailed_activities()

    def get_overview(self, year: int = None) -> dict:
        _summaries = self._get_summaries(year)

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

        return {
            'activities_count': int(overview['count'].sum()),
            'total_seconds': int(overview['sum_moving_time'].sum()),
            'total_distance': int(overview['sum_distance'].sum()),
            'overview': overview[['sum_distance_overview', 'mean_distance_overview', 'sum_moving_time_overview', 'mean_moving_time_overview']].to_dict(orient='index')
        }

    def get_running_analysis(self, year: int = None) -> list[dict]:
        details = self._get_details(year, 'Run')
        specs = [
            Highlight('max_distance', 'distance', display_function=data_format.m_as_km),
            Highlight('max_duration', 'moving_time', display_function=lambda x: data_format.seconds_as_hhmmss(int(x))),
            Highlight('max_elevation_gain', 'total_elevation_gain', display_function=data_format.m),
            Highlight('earlier', 'start_date_local', ascending_sort_order=True),
            Highlight('max_average_speed', 'average_speed', data_format.mps_as_minpkm),
            Highlight('max_top_heartrate', 'max_heartrate', data_format.bpm),
        ]
        return [spec.transform(details) for spec in specs]



    def _get_summaries(self, year = None) -> DataFrame:
        if year is not None:
            return self.summaries.loc[
                (self.summaries['start_date'] >= f'{year}-01-01') & (self.summaries['start_date'] < f'{year + 1}-01-01')
                ]
        return self.summaries

    def _get_details(self, _year = None, _type = None) -> DataFrame:
        _details = self.details
        if _year is not None:
            _details =  self.details.loc[
                (self.details['start_date'] >= f'{_year}-01-01') & (self.details['start_date'] < f'{_year + 1}-01-01')
                ]
        if _type is not None:
            _details = _details.loc[(self.details['type'] == _type)]

        return _details
