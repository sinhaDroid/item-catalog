import os

# find the path
pathname = os.path.dirname(__file__)

# full path
BASE_DIR = os.path.abspath(pathname)

# sqlite url
default_sql_url = 'sqlite:///' + os.path.join(BASE_DIR, 'catalog.db')

initial_category_names = [
	'Soccer', 'Basketball', 'Baseball', 'Frisbee',
	'Snowboarding', 'Rock Climbing', 'Foosball'
]

items = 8