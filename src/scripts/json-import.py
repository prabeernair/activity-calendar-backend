import argparse
import sys
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, exc, Table, MetaData
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

# as "args.file" is "TextIOWrapper", this already checks if given file exists
args = parser.parse_args()


def create_db_record(user_id: int, json_record: dict[str, str | float | list]) -> dict[str, str | int | dict]:
    """
    Converts a JSON record to a DB-insertable dict:
    `{user_id: int, type: str, duration: str, fields: dict}`.

    >>> create_db_record(1, dict(type='run',
    ...                          date='2022-02-09 12:06',
    ...                          distance=5.3,
    ...                          duration='0:25:29'))
    {'user_id': 1, 'type': 'run', 'duration': '[2022-02-09 12:06:00, 2022-02-09 12:31:29]', 'fields': {'distance': 5.3}}
    """

    db_record = dict(user_id=user_id,
                     type=json_record['type'],
                     duration=get_ts_range(json_record['date'],
                                           json_record['duration'] if 'duration' in json_record else '0:00:00'))

    field_name_to_exclude_list = ['type', 'date', 'duration']
    fields = {field_name: json_record[field_name]
              for field_name in json_record
              if field_name not in field_name_to_exclude_list}

    db_record['fields'] = fields if len(fields) else None

    return db_record


def get_ts_range(date_str: str, duration_str: str) -> str:
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
    try:
        json_record_list: list[dict[str, str | float | list]] = json.load(args.file)
    except json.JSONDecodeError as error:
        sys.exit(f"File content can not be deserialized to JSON:\n{error}")

    engine = create_engine(f"postgresql+pg8000://{db_config['user']}@{db_config['host']}/{db_config['name']}")

    try:
        with engine.connect() as connection:
            user_id = int(args.user_id)
            users = Table('users', MetaData(), autoload=True, autoload_with=engine)
            result = connection.execute(select([users]).where(users.c.id == user_id))
            row = result.fetchone()

            if row is None:
                sys.exit(f"user with ID {user_id} is not found in DB")

            activities = Table('activities', MetaData(), autoload=True, autoload_with=engine)
            result = connection.execute(activities.insert(), [create_db_record(user_id, json_record)
                                                              for json_record in json_record_list])
            print(f"inserted {result.rowcount} records into 'activities' table")
    except exc.InterfaceError as error:
        sys.exit(f"SQLAlchemy InterfaceError:\n{error}")

    import doctest
    doctest.testmod()
