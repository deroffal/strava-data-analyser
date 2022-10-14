const {readFile, writeToFile} = require("./file-adatpter");

async function getLastRecordedActivityDate() {
    let currentAthleteActivities = await readFile('/athlete_activities.json')
    return new Date(currentAthleteActivities[currentAthleteActivities.length - 1]['start_date'])
}

async function addNewActivitiesToAthleteActivities(newActivities) {
    let activities = await readFile('/athlete_activities.json')
    activities.push(...newActivities);
    await writeToFile(activities, '/athlete_activities.json')
}

async function addNewActivity(newActivity) {
    await writeToFile(newActivity, `/activities/${newActivity.id}`)
}

module.exports = {getLastRecordedActivityDate, addNewActivitiesToAthleteActivities, addNewActivity}
