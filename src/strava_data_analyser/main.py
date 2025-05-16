import json

from strava_data_analyser.analyser import polars_loader
from strava_data_analyser.analyser.polars_analyzer import PolarsAnalyzer

analyzer = PolarsAnalyzer.from_loader(_polars_loader=polars_loader)

print("Overview for 2025 :")
overview = analyzer.get_overview(2025)
print(json.dumps(overview, indent=4))

# activity_id = 14085045834 # longest activity
# activity_id = 14250862441 # fastest this year
activity_id = 14497321322 # latest
print(f"Analyse for activity {activity_id}")
activity = analyzer.analyse_activity(activity_id)
print(json.dumps(activity, indent=4))

activity_id = 14193115973
segment_id = 13680755 # (many)
# activity_id = 14432892146
# segment_id = 28811814 # (just one)
segment = analyzer.analyse_segment_for_activity(activity_id, segment_id)
print(json.dumps(segment, indent=4))
