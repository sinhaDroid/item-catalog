import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from config import default_sql_url

Base = declarative_base()

######## end of beginning configuration #####

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    description = Column(String(250))

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'user' : self.user,
        }

######### insert at end of file #########3

def create_sqlite_database(sqlite_database_name):
    engine = create_engine(sqlite_database_name)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_sqlite_database(default_sql_url)