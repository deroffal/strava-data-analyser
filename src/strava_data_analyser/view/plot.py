import matplotlib.pyplot as plt
import pandas

from . import data_conversion


def plot_distance_distribution(distance_distribution: pandas.DataFrame, show_empty: bool = False):
    if show_empty:
        distance_distribution.reindex().plot(x='distance', y='count', kind="bar")
    else:
        distance_distribution[distance_distribution['count'] != 0].plot(x='distance', y='count', kind="bar")


def plot_top_segments_bar(segments):
    width = 0.5
    ax = segments.plot(x='name', y='count', kind="bar", legend=False, width=width)

    for i, (name, height) in enumerate(zip(segments['name'], segments['count'])):
        ax.text(i, height, ' ' + name, ha='center', va='top', rotation=-90, fontsize=10)

    ax.set_title('Top 10 Segment')
    ax.set_xlabel('')
    ax.set_ylabel('Count')
    ax.set_xticks([])


def plot_split_metric_heartrate(metrics, means):
    fig, ax = plt.subplots()

    ax.scatter(metrics['split'], metrics['average_heartrate'])
    ax.scatter(means['split'], means['average_heartrate'])

    ax.set_xlabel("km split")
    ax.set_ylabel("heart rate (bpm)")
    plt.show()


def plot_split_metric_speed(metrics, means):
    fig, ax = plt.subplots()

    metrics['average_speed_kmh'] = metrics['average_speed'].apply(data_conversion.mps_to_kmh)
    ax.scatter(metrics['split'], metrics['average_speed_kmh'])

    means['mean_speed_kmh'] = means['average_speed'].apply(data_conversion.mps_to_kmh)
    ax.scatter(means['split'], means['mean_speed_kmh'])

    ax.set_xlabel("km split")
    ax.set_ylabel("speed (km/h)")

    plt.show()
