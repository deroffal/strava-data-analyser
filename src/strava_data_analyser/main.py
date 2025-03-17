from strava_data_analyser.analyser.analyzer import Analyzer
import json

analyzer = Analyzer()

print("Overview for 2025:")
overview = analyzer.get_overview(2025)
print(json.dumps(overview, indent=4))
