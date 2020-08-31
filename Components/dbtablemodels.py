# Placeholder for db table classes

# SQLAlchemy module library
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
class BookTable(Base):
    
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copyright_year = Column(Integer, nullable=False)
    series = Column(Integer, ForeignKey("series.series_id"))
    
    seriesid = relationship("SeriesTable", backref=backref("series"))
    
    def __repr__(self):
        return f"<title={self.title}, author={self.author}, copyright_year={self.copyright_year}, series={self.series}>"

class SeriesTable(Base):
    
    __tablename__ = "series"
    series_id = Column(Integer, primary_key=True)
    seriesname = Column(String, nullable=False)
    bookstotal = Column(Integer, nullable=False)
            
    def __repr__(self):
        
        return f"<series_id={self.series_id}, seriesname={self.seriesname}, bookstotal={self.bookstotal}>"

class OlvBookTable():
        
    def __init__(self, book_id, title, author, copyright_year, seriesname):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.copyright_year = copyright_year
        self.seriesname = seriesname
        
        
class OlvSeriesTable():
    
    def __init__(self, series_id, seriesname, bookstotal):
        
        self.series_id = series_id
        self.seriesname = seriesname
        self.bookstotal = bookstotal
        