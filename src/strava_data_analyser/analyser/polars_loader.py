import json
from io import StringIO

import polars as pl

from strava_data_analyser.storage.storage import Storage

_summary_schema = {
    "resource_state": pl.Int64,
    "athlete": pl.Struct(
        {
            "id": pl.Int64,
            "resource_state": pl.Int64,
        }
    ),
    "name": pl.Utf8,
    "distance": pl.Float64,
    "moving_time": pl.Int64,
    "elapsed_time": pl.Int64,
    "total_elevation_gain": pl.Float64,
    "type": pl.Utf8,
    "sport_type": pl.Utf8,
    "workout_type": pl.Int64,
    "id": pl.Int64,
    "start_date": pl.Datetime,
    "start_date_local": pl.Datetime,
    "timezone": pl.Utf8,
    "utc_offset": pl.Float64,
    "location_city": pl.Utf8,
    "location_state": pl.Utf8,
    "location_country": pl.Utf8,
    "achievement_count": pl.Int64,
    "kudos_count": pl.Int64,
    "comment_count": pl.Int64,
    "athlete_count": pl.Int64,
    "photo_count": pl.Int64,
    "map": pl.Struct(
        {
            "id": pl.Utf8,
            "summary_polyline": pl.Utf8,
            "resource_state": pl.Int64,
        }
    ),
    "trainer": pl.Boolean,
    "commute": pl.Boolean,
    "manual": pl.Boolean,
    "private": pl.Boolean,
    "visibility": pl.Utf8,
    "flagged": pl.Boolean,
    "gear_id": pl.Utf8,
    "start_latlng": pl.List(pl.Float64),
    "end_latlng": pl.List(pl.Float64),
    "average_speed": pl.Float64,
    "max_speed": pl.Float64,
    "has_heartrate": pl.Boolean,
    "heartrate_opt_out": pl.Boolean,
    "display_hide_heartrate_option": pl.Boolean,
    "elev_high": pl.Float64,
    "elev_low": pl.Float64,
    "upload_id": pl.Int64,
    "upload_id_str": pl.Utf8,
    "external_id": pl.Utf8,
    "from_accepted_tag": pl.Boolean,
    "pr_count": pl.Int64,
    "total_photo_count": pl.Int64,
    "has_kudoed": pl.Boolean,
}

# issue with scan_ndjson :
# FIXME some comment due to missing data ->
# FIXME pl.Datetime when start_date is inside a struct is not working
# TODO check if ok with read_json
_detail_schema = {
    "resource_state": pl.Int64,
    "athlete": pl.Struct(
        {
            "id": pl.Int64,
            "resource_state": pl.Int64,
        }
    ),
    "name": pl.Utf8,
    "distance": pl.Float64,
    "moving_time": pl.Int64,
    "elapsed_time": pl.Int64,
    "total_elevation_gain": pl.Float64,
    "type": pl.Utf8,
    "sport_type": pl.Utf8,
    "workout_type": pl.Int64,
    "id": pl.Int64,
    "start_date": pl.Datetime,
    "start_date_local": pl.Datetime,
    "timezone": pl.Utf8,
    "utc_offset": pl.Float64,
    "location_city": pl.Utf8,
    "location_state": pl.Utf8,
    "location_country": pl.Utf8,
    "achievement_count": pl.Int64,
    "kudos_count": pl.Int64,
    "comment_count": pl.Int64,
    "athlete_count": pl.Int64,
    "photo_count": pl.Int64,
    "map": pl.Struct(
        {
            "id": pl.Utf8,
            "polyline": pl.Utf8,
            "resource_state": pl.Int64,
            "summary_polyline": pl.Utf8,
        }
    ),
    "trainer": pl.Boolean,
    "commute": pl.Boolean,
    "manual": pl.Boolean,
    "private": pl.Boolean,
    "visibility": pl.Utf8,
    "flagged": pl.Boolean,
    "gear_id": pl.Utf8,
    "start_latlng": pl.List(pl.Float64),
    "end_latlng": pl.List(pl.Float64),
    "average_speed": pl.Float64,
    "max_speed": pl.Float64,
    "has_heartrate": pl.Boolean,
    "heartrate_opt_out": pl.Boolean,
    "display_hide_heartrate_option": pl.Boolean,
    "elev_high": pl.Float64,
    "elev_low": pl.Float64,
    "upload_id": pl.Int64,
    "upload_id_str": pl.Utf8,
    "external_id": pl.Utf8,
    "from_accepted_tag": pl.Boolean,
    "pr_count": pl.Int64,
    "total_photo_count": pl.Int64,
    "has_kudoed": pl.Boolean,
    "description": pl.Utf8,
    "calories": pl.Float64,
    "perceived_exertion": pl.Float64,
    "prefer_perceived_exertion": pl.Boolean,
    "segment_efforts": pl.List(
        pl.Struct(
            {
                "id": pl.Int64,
                "resource_state": pl.Int64,
                "name": pl.Utf8,
                "activity": pl.Struct(
                    {
                        "id": pl.Int64,
                        "visibility": pl.Utf8,
                        "resource_state": pl.Int64,
                    }
                ),
                "athlete": pl.Struct(
                    {
                        "id": pl.Int64,
                        "resource_state": pl.Int64,
                    }
                ),
                "elapsed_time": pl.Int64,
                "moving_time": pl.Int64,
                "start_date": pl.Utf8,
                "start_date_local": pl.Utf8,
                "distance": pl.Float64,
                "start_index": pl.Int64,
                "end_index": pl.Int64,
                "device_watts": pl.Boolean,
                "segment": pl.Struct(
                    {
                        "id": pl.Int64,
                        "resource_state": pl.Int64,
                        "name": pl.Utf8,
                        "activity_type": pl.Utf8,
                        "distance": pl.Float64,
                        "average_grade": pl.Float64,
                        "maximum_grade": pl.Float64,
                        "elevation_high": pl.Float64,
                        "elevation_low": pl.Float64,
                        "start_latlng": pl.List(pl.Float64),
                        "end_latlng": pl.List(pl.Float64),
                        "climb_category": pl.Int64,
                        "city": pl.Utf8,
                        "state": pl.Utf8,
                        "country": pl.Utf8,
                        "private": pl.Boolean,
                        "hazardous": pl.Boolean,
                        "starred": pl.Boolean,
                    }
                ),
                "pr_rank": pl.Int64,
                "achievements": pl.List(
                    pl.Struct(
                        {
                            "type_id": pl.Int64,
                            "type": pl.Utf8,
                            "rank": pl.Int64,
                        }
                    )
                ),
                "visibility": pl.Utf8,
                "hidden": pl.Boolean,
            }
        )
    ),
    "splits_metric": pl.List(
        pl.Struct(
            {
                "distance": pl.Float64,
                "elapsed_time": pl.Int64,
                "elevation_difference": pl.Float64,
                "moving_time": pl.Int64,
                "split": pl.Int64,
                "average_speed": pl.Float64,
                "average_grade_adjusted_speed": pl.Float64,
                "pace_zone": pl.Int64,
            }
        )
    ),
    "splits_standard": pl.List(
        pl.Struct(
            {
                "distance": pl.Float64,
                "elapsed_time": pl.Int64,
                "elevation_difference": pl.Float64,
                "moving_time": pl.Int64,
                "split": pl.Int64,
                "average_speed": pl.Float64,
                "average_grade_adjusted_speed": pl.Float64,
                "pace_zone": pl.Int64,
            }
        )
    ),
    "laps": pl.List(
        pl.Struct(
            # [
            #     pl.Field("id", pl.Int64),
            #     pl.Field("resource_state", pl.Int64),
            #     pl.Field("name", pl.Utf8),
            #     pl.Field("activity", pl.Struct(
            #         {
            #             "id": pl.Int64,
            #             "visibility": pl.Utf8,
            #             "resource_state": pl.Int64,
            #         }
            #     )),
            #     pl.Field("athlete", pl.Struct(
            #         {
            #             "id": pl.Int64,
            #             "resource_state": pl.Int64,
            #         }
            #     )),
            #     pl.Field("elapsed_time", pl.Int64),
            #     pl.Field("moving_time", pl.Int64),
            #     pl.Field("start_date", pl.Datetime),
            # ]
            {
                "id": pl.Int64,
                "resource_state": pl.Int64,
                "name": pl.Utf8,
                "activity": pl.Struct(
                    {
                        "id": pl.Int64,
                        "visibility": pl.Utf8,
                        "resource_state": pl.Int64,
                    }
                ),
                "athlete": pl.Struct(
                    {
                        "id": pl.Int64,
                        "resource_state": pl.Int64,
                    }
                ),
                "elapsed_time": pl.Int64,
                "moving_time": pl.Int64,
                "start_date": pl.Utf8,
                "start_date_local": pl.Utf8,
                "distance": pl.Float64,
                "average_speed": pl.Float64,
                "max_speed": pl.Float64,
                "lap_index": pl.Int64,
                "split": pl.Int64,
                "start_index": pl.Int64,
                "end_index": pl.Int64,
                # "total_elevation_gain": pl.Float64,
                "device_watts": pl.Boolean,
                "pace_zone": pl.Int64,
            }
        )
    ),
    "best_efforts": pl.List(
        pl.Struct(
            {
                "id": pl.Int64,
                "resource_state": pl.Int64,
                "name": pl.Utf8,
                "activity": pl.Struct(
                    {
                        "id": pl.Int64,
                        "visibility": pl.Utf8,
                        "resource_state": pl.Int64,
                    }
                ),
                "athlete": pl.Struct(
                    {
                        "id": pl.Int64,
                        "resource_state": pl.Int64,
                    }
                ),
                "elapsed_time": pl.Int64,
                "moving_time": pl.Int64,
                "start_date": pl.Utf8,
                "start_date_local": pl.Utf8,
                "distance": pl.Int64,
                "pr_rank": pl.Int64,
                "start_index": pl.Int64,
                "end_index": pl.Int64,
                "achievements": pl.List(
                    pl.Struct(
                        {
                            "type_id": pl.Int64,
                            "type": pl.Utf8,
                            "rank": pl.Int64,
                        }
                    )
                ),
            }
        )
    ),
    # for now, we don't care about photos
    #
    # "photos": pl.Struct(
    #     {
    #         "primary": pl.Utf8,
    #         "count": pl.Int64,
    #     }
    # ),
    "stats_visibility": pl.List(
        pl.Struct(
            {
                "type": pl.Utf8,
                "visibility": pl.Utf8,
            }
        )
    ),
    "hide_from_home": pl.Boolean,
    "embed_token": pl.Utf8,
    "similar_activities": pl.Struct(
        {
            "effort_count": pl.Int64,
            # "average_speed": pl.Float64,
            # "min_average_speed": pl.Float64,
            # "mid_average_speed": pl.Float64,
            # "max_average_speed": pl.Float64,
            "pr_rank": pl.Int64,
            "frequency_milestone": pl.Utf8,
            "trend": pl.Struct(
                {
                    "speeds": pl.List(pl.Float64),
                    "current_activity_index": pl.Int64,
                    # "min_speed": pl.Float64,
                    # "mid_speed": pl.Float64,
                    # "max_speed": pl.Float64,
                    "direction": pl.Int64,
                }
            ),
            "resource_state": pl.Int64,
        }
    ),
    "available_zones": pl.List(pl.Utf8)
}


# To read json files with Polar, read/scan_ndjson seems to be better than read_json at first (can load multiple files, lazy loading)
# Yet, I experience some issues : datetime format inside struc for example
# For now, i'm going to use read_json.
def load_data():
    _storage = Storage()
    _details = source_to_df(_storage.load_detailed_activities(), _detail_schema)
    _summary = source_to_df(_storage.load_summary_activities(), _summary_schema)
    return _summary, _details


def source_to_df(_source, _schema):
    _json = [
        json.loads(it)
        for it in _source
    ]
    return pl.read_json(StringIO(json.dumps(_json)), schema=_schema, infer_schema_length=10000)
