import argparse
import json
from datetime import datetime, timedelta


parser = argparse.ArgumentParser(description='Imports a list of activities from JSON file to DB')
parser.add_argument('user_id', type=int,
                    help='a user ID to assign activities to')
parser.add_argument('file', type=open,
                    help='a relative path to the input file')

args = parser.parse_args()


def create_db_record(json_record):
    db_record = dict(user_id=args.user_id,
                     type=json_record['type'],
                     duration=get_ts_range(json_record['date'], json_record['duration']))

    field_name_list = [
        'distance',
        'surface',
        'averagePace',
        'fastestSplitPace',
        'slowestSplitPace',
    ]
    fields = dict({field_name: json_record[field_name]
                   for field_name in field_name_list
                   if field_name in json_record})

    if len(fields):
        db_record['fields'] = fields

    return db_record


def get_ts_range(date_str, duration_str):
    """
    Returns a Postgres TSRANGE string.

    >>> get_ts_range('2020-03-18 09:20', '0:23:21')
    '[2020-03-18 09:20:00, 2020-03-18 09:43:21]'
    """

    [hours, minutes, seconds] = duration_str.split(':')
    duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    from_dt = datetime.fromisoformat(date_str)
    to_dt = from_dt + duration

    return f'[{from_dt}, {to_dt}]'


if __name__ == "__main__":
    db_record_map = map(create_db_record, json.load(args.file))

    for db_record in db_record_map:
        print(db_record)

    # @todo: connect to Postgres and import a given JSON file into the "activities" table

    import doctest
    doctest.testmod()
