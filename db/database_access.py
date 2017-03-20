from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User
from config import default_sql_url, items, latest_items

def db_create_session():
	engine = create_engine(default_sql_url)
	Base.metadata.bind = engine

	DBSession = sessionmaker(bind=engine)
	return DBSession()

def db_add_categories(session, category_names):
	for category_name in category_names:
		session.add(Category(name=category_name))
		session.commit()

def db_add_item_using_category_name(session, category_name, item_name, item_desc, user_id):
	category = session.query(Category).filter_by(name=category_name).one()
	session.add(Item(name=item_name, description=item_desc, category_id=category.id))
	session.commit()

def db_categories(db_session):
	return db_session.query(Category).order_by(Category.name).all()

def db_category(db_session, category_id):
	return db_session.query(Category).filter_by(id=category_id).one()

def db_items_in_category(db_session, category_id):
	return db_session.query(Item).filter_by(category_id=category_id).order_by(Item.name).all()

def db_item(db_session, item_id):
	return db_session.query(Item).filter_by(id=item_id).one()

def db_latest_items(db_session, number_of_items=latest_items):
	return db_session.query(Item).order_by(Item.updated.desc()).limit(number_of_items)

def db_save_item(session, item):
	session.add(item)
	session.commit()

def db_delete_item(session, item):
    session.delete(item)
    session.commit()

def db_update_user(db_session, login_session):
    user_id = login_session['id']
    user = db_session.query(User).filter_by(id=user_id).all()
    if not user:
        user = User()
        user.id = user_id
        db_session.add(user)
        db_session.commit()
