import argparse
import sys
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select


# @todo: load from ENV vars
db_config = dict(user='markhovs',
                 host='localhost',
                 name='activity_calendar')

parser = argparse.ArgumentParser(description="Imports a list of activities from JSON file to DB")
parser.add_argument('user_id', type=int,
                    help="a user ID to assign activities to")
parser.add_argument('file', type=open,
                    help="a relative path to the input file")

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

    db_record['fields'] = fields if len(fields) else None

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


if __name__ == '__main__':
    engine = create_engine(f"postgresql+pg8000://{db_config['user']}@{db_config['host']}/{db_config['name']}")

    with engine.connect() as connection:
        users = Table('users', MetaData(), autoload=True, autoload_with=engine)
        result = connection.execute(select([users]).where(users.c.id == args.user_id))
        row = result.fetchone()

        if row is None:
            sys.exit(f"user with ID {args.user_id} is not found in DB")

        activities = Table('activities', MetaData(), autoload=True, autoload_with=engine)
        result = connection.execute(activities.insert(), [create_db_record(json_record)
                                                          for json_record in json.load(args.file)])
        print(f"inserted {result.rowcount} records into 'activities' table")

    import doctest
    doctest.testmod()
