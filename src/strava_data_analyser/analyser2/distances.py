import math

import pandas as pd


def round_down_to_nearest_step(num: int, step: int) -> int:
    """
    Round a distance to the nearest lower step (in meters)
    :param num: distance (meters)
    :param step: step to round (meters)
    :return: rounded distance
    """
    return math.floor(num / step) * step


def get_distance_distribution(activities: pd.DataFrame, step: int):
    distances = pd.DataFrame(activities['distance'].apply(lambda distance: round_down_to_nearest_step(distance, step)))
    distances_count = distances.groupby(['distance']).size().reset_index(name="count")

    empty_distances = []
    for dist in range(distances_count['distance'].min(), distances_count['distance'].max(), step):
        if distances_count[distances_count['distance'] == dist].size == 0:
            empty_distances.append({'distance': dist, 'count': 0})

    distances_count = pd.concat([distances_count, pd.DataFrame(empty_distances)])
    distances_count.sort_values('distance', inplace=True)

    return distances_count
