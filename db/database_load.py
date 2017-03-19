from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, Base
from database_access import db_create_session, db_add_categories

from config import default_sql_url, initial_category_names

db_session = db_create_session()
db_add_categories(db_session, initial_category_names)

# Add some items
soccer = db_session.query(Category).filter_by(name='Soccer').one()
soccer_ball = Item(name='Soccer ball',
                   description='Fast, light official soccer ball.',
                   category_id=soccer.id)

db_session.add(soccer_ball)
db_session.commit()