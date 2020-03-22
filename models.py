from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)  
from sqlalchemy.ext.declarative import declarative_base 

engine = create_engine('sqlite:///covid.sqlite3', convert_unicode = True) 
db_session = scoped_session(sessionmaker(autocommit = False,
                                         autoflush=False,
                                         bind=engine)) 

Base = declarative_base() 
Base.query = db_session.query_property() 

class Country(Base):
    __tablename__ = 'country' 
    id = Column(Integer, primary_key = True) 
    name = Column(String)
    total_cases = Column(Integer) 
    total_deaths = Column(Integer)
    history = relationship("DayData", primaryjoin="DayData.country_id == Country.id")


class DayData(Base):
    __tablename__ = 'country_history' 
    id = Column(Integer, primary_key = True)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country", back_populates = 'history')
    date = Column(Date) 
    new_cases = Column(Integer) 
    new_deaths = Column(Integer)

