# Either a year, or None for all time activities
from strava_data_analyser.analyser2.highlights import Highlight
from strava_data_analyser.analyser2 import file_loader
from strava_data_analyser.view import data_format

selectedYear = None
# selectedYear = 2023

# Either a year, or None for all kind of activities
# selectedType = None
selectedType = 'Run'

activities = file_loader.load_detailed_activities( year=selectedYear, type=selectedType)

# runs = activities[['id', 'start_date_local', 'name', 'distance', 'elapsed_time', 'average_speed', 'total_elevation_gain']] \
#     .sort_values('distance', ascending=False)
# runs['distance_overview'] = runs['distance'].apply(data_format.m_as_km)
# runs['elapsed_time_overview'] = runs['elapsed_time'].apply(data_format.seconds_as_hhmmss)
# runs['average_speed_overview'] = runs['average_speed'].apply(data_format.mps_as_minpkm)
# runs['total_elevation_gain_overview'] = runs['total_elevation_gain'].apply(data_format.m)
# print(runs[['id', 'name', 'distance_overview', 'elapsed_time_overview', 'average_speed_overview',
#               'total_elevation_gain_overview', 'start_date_local']].to_string())

highlights_requests = [
    Highlight('max_distance', 'distance', display_function=data_format.m_as_km),
    Highlight('max_duration', 'elapsed_time', display_function=lambda x: data_format.seconds_as_hhmmss(int(x))),
    Highlight('max_elevation_gain', 'total_elevation_gain', display_function=data_format.m),
    Highlight('earlier', 'start_date_local', ascending_sort_order=True),
    Highlight('max_average_speed', 'average_speed', data_format.mps_as_minpkm),
    Highlight('max_top_heartrate', 'max_heartrate', data_format.bpm),
]


highlights = []
for highlight_request in highlights_requests:
    highlight = highlight_request.transform(activities)
    highlights.append(highlight)

for highlight in highlights:
    print(highlight)

# distance_distribution = get_distance_distribution(runs, 1000)
#
# plot_distance_distribution(distance_distribution, True)
#
#
# top_10_segments = segments.get_top_10_segments(activities)
#
# print(top_10_segments)
#
# plot.plot_top_segments_bar(top_10_segments)
#
# runs_activities = activities[activities['workout_type'] != 3].reset_index()
# metrics = split_metrics.extract_split_metrics(runs_activities)
#
# plot.plot_split_metric_heartrate(metrics['value'], metrics['means'])
# plot.plot_split_metric_speed(metrics['value'], metrics['means'])
