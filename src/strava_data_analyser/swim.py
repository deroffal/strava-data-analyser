from strava_data_analyser.storage import loader

# Either a year, or None for all time activities
selectedYear = None
# selectedYear = 2023

# Either a year, or None for all kind of activities
# selectedType = None
selectedType = 'Swim'



activities = loader.load_detailed_activities(source='file', year=selectedYear, type=selectedType)

activities = activities[['id', 'laps', 'splits_metric', 'splits_standard']]

print(activities.to_string())
