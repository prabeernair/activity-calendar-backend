import argparse


parser = argparse.ArgumentParser(description='Imports a list of activities from JSON file to DB')
parser.add_argument('userid', type=int,
                    help='a user ID')
parser.add_argument('filepath', type=open,
                    help='a relative path to the input file')

args = parser.parse_args()

print(args)

# @todo: connect to Postgres and import a given JSON file into the "activities" table
