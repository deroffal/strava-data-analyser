from strava_data_analyser.analyser.analyzer import Analyzer
import json

analyzer = Analyzer()

print("Overview for 2025 :")
overview = analyzer.get_overview(2025)
print(json.dumps(overview, indent=4))

# print("Running analysis for 2025 :")
# running_analysis = analyzer.get_running_analysis(2025)
# print(json.dumps(running_analysis, indent=4))
