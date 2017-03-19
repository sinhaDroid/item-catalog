from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item
from config import default_sql_uri, initial_category_names, items

def db_create_session(sqlite_db_uri=default_sql_uri):
	print 'entering db_create_session()...'
	engine = create_engine(sqlite_db_uri)
	Base.metadata.bind = engine

	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	return session

def db_add_categories(session, category_names):
	"""Add specified category_names to database."""
	for category_name in category_names:
		category = Category(name=category_name)
		session.add(category)
		session.commit()

def db_add_item_using_category_name(session, category_name, item_name, item_desc):
	category = session.query(Category).filter_by(name=category_name).one()

	# TODO:// category_id category.id
	new_item = Item(name=item_name, description=item_desc, category_id=category_id)
	session.add(new_item)
	session.commit()

def db_categories(db_session, category_id):
	categories = db_session.query(Category).order_by(Category.name).all()
	print 'db_categories...'
	print 'len(categories) = ' + str(len(categories))
	return categories

def db_category(db_session, category_id):
	category = db_session.query(Category).filter_by(id=category_id).one()
	return category

def db_items_in_category(db_session, category_id):
	items = db_session.query(Item).filter_by(category_id=category_id).order_by(Item.name).all()
	return items

def db_item(db_session, item_id):
	item = db_session.query(Item).filter_by(id=item_id).one()
	return item

def db_latest_items(db_session, number_of_items=items):
	pass

def db_save_item(session, item):
	session.add(item)
	session.commit()

def db_delete_item(session, item):
    session.delete(item)
    session.commit()