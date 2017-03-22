import os

# find the path
pathname = os.path.dirname(__file__)

# full path
BASE_DIR = os.path.abspath(pathname)
default_sqlite_url = 'sqlite:///' + os.path.join(BASE_DIR, 'catalog.db')

# add support for Postgresql database
# sqlalchemy_database_uri = "postgresql://" +
# "catalog:catalog_super_secret@localhost/catalog"

default_sql_url = default_sqlite_url

items = [
    'Soccer', 'Basketball', 'Baseball', 'Frisbee',
    'Snowboarding', 'Rock Climbing', 'Foosball',
    'Skating', 'Hockey'
]

latest_items = 10
