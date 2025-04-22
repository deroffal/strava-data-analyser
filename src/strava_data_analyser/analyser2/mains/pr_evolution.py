from strava_data_analyser.storage import file_loader

activities = file_loader.load_detailed_activities(type='Run')
runs = activities[activities['type'] == 'Run']

# FIXME create only if needed
achievements = {
    '400m': [],
    '1/2 mile': [],
    '1K': [],
    '1 mile': [],
    '2 mile': [],
    '5K': [],
    '10K': [],
    '15K': [],
    '10 mile': [],
    '20K': [],
    'Half-Marathon': []
}

for index, run in runs[['id', 'start_date', 'name', 'best_efforts']].reset_index().iterrows():
    run_name = run['name']
    run_id = run['id']
    run_start_date = run['start_date']
    best_efforts = run['best_efforts']
    for efforts in best_efforts:
        if (efforts['achievements']) and (efforts['pr_rank'] == 1):
            efforts_name = efforts['name']
            pr_value = efforts['elapsed_time']
            achievements.get(efforts_name) \
                .append({
                'id': run_id,
                'name': run_name,
                'start_date': run_start_date,
                'pr_key': efforts_name,
                'pr_value': pr_value
            })

print(achievements)
