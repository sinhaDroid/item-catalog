import sys
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from config import default_sql_url

Base = declarative_base()

######## end of beginning configuration #####

class User(Base):
    __tablename__ = 'user'

    id = Column(String(80), primary_key = True)
    name = Column(String(80))

    @property
    def serialize(self):
        return {
            'id':   self.id,
            'name': self.name
        }

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)

    @property
    def serialize(self):
        return {
            'id':   self.id,
            'name': self.name
        }

class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    description = Column(String(250))

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.datetime.now)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    user_id = Column(String(80), ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'category_id':  self.category_id,
            'user_id':  self.user_id
        }

######### insert at end of file #########3

def create_database(sqlite_database_name):
    Base.metadata.create_all(create_engine(sqlite_database_name))

if __name__ == '__main__':
    create_database(default_sql_url)