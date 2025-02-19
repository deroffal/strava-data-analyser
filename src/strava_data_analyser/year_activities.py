from strava_data_analyser.storage import loader
from strava_data_analyser.analyser import overview
from strava_data_analyser.view import data_format

activities = loader.load_activities('file', 2025)

overview = overview.get_overview(activities)

activities_count = int(overview['count'].sum())
print("Total activities : ", activities_count)

total_seconds = int(overview['sum_moving_time'].sum())
print("Activities total time : ", data_format.seconds_as_hhmmss(total_seconds))

total_distance = int(overview['sum_distance'].sum())
print("Activities total distance : ", data_format.m_as_km(total_distance))

overview['sum_distance_overview'] = overview['sum_distance'].apply(data_format.m_as_km)
overview['mean_distance_overview'] = overview['mean_distance'].apply(data_format.m_as_km)
overview['sum_moving_time_overview'] = overview['sum_moving_time'].apply(data_format.seconds_as_hhmmss)
overview['mean_moving_time_overview'] = overview['mean_moving_time'].apply(data_format.seconds_as_hhmmss)

print(overview.to_string())
