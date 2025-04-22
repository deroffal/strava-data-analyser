import itertools

import pandas as pd


def extract_split_metrics(activities):
    """
    Extract split metrics from activities dataframe
    :param activities: all activities
    :return: a dataframe with each activity's split for speed and heart rate
    """
    metrics_list = []

    for index, row in activities.iterrows():
        run_metrics = row['splits_metric']
        activity_id = row['id']
        for metric in run_metrics:
            metric['activity_id'] = activity_id
        metrics_list.append(run_metrics)

    metrics = itertools.chain.from_iterable(metrics_list)

    df = pd.DataFrame(metrics)[['split', 'average_speed', 'average_heartrate', 'activity_id']]

    means = df[['split', 'average_speed', 'average_heartrate']] \
        .groupby('split').mean() \
        .reset_index()

    return {
        'value': df,
        'means': means
    }
