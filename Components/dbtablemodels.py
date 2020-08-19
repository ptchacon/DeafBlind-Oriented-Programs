# Placeholder for db table classes

# SQLAlchemy module library
from sqlalchemy import (Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class BookTable(Base):
    
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copyright_year = Column(Integer, nullable=False)
    series = Column(String)
    
    def __repr__(self):
        return f"<title={self.title}, author={self.author}, copyright_year={self.copyright_year}, series={self.series}>"

class OlvBookTable():
        
    def __init__(self, book_id, title, author, copyright_year, series):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.copyright_year = copyright_year
        self.series = series
        
