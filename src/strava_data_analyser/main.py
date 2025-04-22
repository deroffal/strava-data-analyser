import json

from strava_data_analyser.analyser import polars_loader
from strava_data_analyser.analyser.polars_analyzer import PolarsAnalyzer

analyzer = PolarsAnalyzer.from_loader(_polars_loader=polars_loader)

print("Overview for 2025 :")
overview = analyzer.get_overview(2025)
print(json.dumps(overview, indent=4))

# activity_id = 14085045834 # longest activity
activity_id = 14250862441 # fastest this year
print(f"Analyse for activity {activity_id}")
activity = analyzer.analyse_activity(activity_id)
print(json.dumps(activity, indent=4))
