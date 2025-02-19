from pandas import DataFrame


def get_overview(activities: DataFrame):
    overview_2022 = activities[['type', 'distance', 'moving_time']] \
        .groupby('type') \
        .agg({'distance': ['count', 'sum', 'mean'], 'moving_time': ['sum', 'mean']})

    distance_df = overview_2022["distance"]
    moving_time_df = overview_2022["moving_time"]

    overview = distance_df.merge(moving_time_df, on='type', suffixes=("_distance", "_moving_time"))

    return overview
