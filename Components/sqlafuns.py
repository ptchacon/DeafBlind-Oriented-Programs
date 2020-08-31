# Base functions for interacting with SQLAlchemy

# imports from SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def getsqlsess(engine):
    
    Session = sessionmaker(bind=engine)
    return Session()