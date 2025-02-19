import pandas as pd
from datetime import datetime
from pymongo import MongoClient


def _read_mongo(username, password, host, port, db, collection, query={}):
    mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)

    conn = MongoClient(mongo_uri)
    db = conn[db]

    cursor = db[collection].find(query)

    df = pd.DataFrame(list(cursor))

    return df


def find_activities(year: int = None):
    query = {}
    if year is not None:
        query = {"start_date": {"$gte": datetime(year, 1, 1), "$lt": datetime(year + 1, 1, 1)}}
    return _do_mongo_query(query, "strava_summary_activity")


def find_detailed_activities(year: int = None, type: str = None):
    query = {}
    if year is not None:
        query = {"start_date": {"$gte": datetime(year, 1, 1), "$lt": datetime(year + 1, 1, 1)}}
    if type is not None:
        query = {"type": type}
    return _do_mongo_query(query, "strava_detailed_activity")


def _do_mongo_query(query, collection_name):
    return _read_mongo(
        username="analysis-app",
        password="password",
        host='localhost',
        port=27017,
        db="statistics",
        collection=collection_name,
        query=query
    )
