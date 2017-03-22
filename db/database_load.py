from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, Base
from database_access import db_create_session, db_add_categories

from config import items

db_add_categories(db_create_session(), items)
