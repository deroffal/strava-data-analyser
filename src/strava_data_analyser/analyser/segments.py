import itertools

import pandas as pd


def get_top_10_segments(activities):
    activities_segments = activities['segment_efforts'].apply(extract_segments)
    segments_2022 = pd.DataFrame(itertools.chain.from_iterable(activities_segments.values))

    top_10_segments = segments_2022.groupby(['id']) \
        .agg(count=('id', 'count'), name=('name', 'min'))[['count', 'name']] \
        .reset_index().sort_values(by=('count'), ascending=False) \
        .head(10)
    return top_10_segments


def extract_segments(segments: dict):
    """
    Extract segment's data
    :param segments: segments
    :return: a list of segments :
    {
        "id": $segment['segment']['id'],
        "elapsedTime": $segment['elapsed_time'],
        "name": $segment['name']
    }
    """
    datas = []
    for segment in segments:
        segment_id = segment['segment']['id']
        elapsed_time = segment['elapsed_time']
        segment_name = segment['name']
        datas.append({'id': segment_id, 'name': segment_name, 'elapsed_time': elapsed_time})
    return datas
