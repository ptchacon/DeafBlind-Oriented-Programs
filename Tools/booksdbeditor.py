"""
This program creates and then edit Books database.
"""

# Import from Python library
import os, pprint

# Import from wx
import wx
# Import from ObjectListView
from ObjectListView import ObjectListView, ColumnDefn
# Import from SQLAlchemy
from sqlalchemy import (create_engine, MetaData, Table, 
                        Column, Integer, String, 
                        select)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import from my library
from Components.sizers import VBoxSizer
from Components.dialogs import (AddRowtoBookDBDialog, EditBookRowDialog,
                                AddRowtoSeriesDBDialog, EditSeriesRowDialog)
from Components.dbtablemodels import (BookTable, OlvBookTable,
                                      SeriesTable, OlvSeriesTable,
                                      Base)
from Components import sqlafuns

class BooksDBPanel(wx.Panel):
    """
    A panel for Books database construction.
    """
    
    def __init__(self, parent):
        
        self.engine = None
        if not os.path.exists("books.db"):
            self.CreateDB("books.db")
        else:
            self.engine = create_engine("sqlite:///books.db")
        self.session = sqlafuns.getsqlsess(self.engine)
        
        super().__init__(parent)
        vsizer = VBoxSizer()
        
        hsizer1 = wx.BoxSizer()
        combolab = wx.StaticText(self, label="Pick a table:")
        self.tablenames = [BookTable.__tablename__, SeriesTable.__tablename__]
        self.tablecombo = wx.Choice(self, choices=self.tablenames)
        self.tablecombo.SetSelection(0)
        self.tablecombo.Bind(wx.EVT_CHOICE, self.OnChoice)
        self.current_table = self.tablecombo.GetStringSelection()
        hsizer1.Add(combolab)
        hsizer1.Add(self.tablecombo)
        vsizer.Add(hsizer1, 0, wx.CENTER)
        
        self.olvtable = ObjectListView(self, style=wx.LC_REPORT)
        vsizer.Add(self.olvtable, 1, wx.EXPAND)
        
        hsizer2 = wx.BoxSizer()
        addbtn = wx.Button(self, label="Add a row")
        addbtn.Bind(wx.EVT_BUTTON, self.OnAdd)
        hsizer2.Add(addbtn)
        editbtn = wx.Button(self, label="Edit a row")
        editbtn.Bind(wx.EVT_BUTTON, self.OnEdit)
        hsizer2.Add(editbtn)
        delbtn = wx.Button(self, label="Delete a row")
        delbtn.Bind(wx.EVT_BUTTON, self.OnDelete)
        hsizer2.Add(delbtn)
        vsizer.Add(hsizer2, 0, wx.CENTER)
        
        self.SetSizer(vsizer)
        
        self.AddCols("book")
        
    def CreateDB(self, dbfilename):
        
        self.engine = create_engine(f"sqlite:///{dbfilename}")
        Base.metadata.create_all(self.engine)
        
    def AddCols(self, current_table):
        
        self.olvtable.ClearAll()
        if current_table == "book":
            self.olvtable.SetColumns([ColumnDefn("Book Id", "left", 50, "book_id"),
                                      ColumnDefn("Title", "left", 200, "title"),
                                      ColumnDefn("Author", "left", 200, "author"),
                                      ColumnDefn("Copyright Year", 'left', 200, "copyright_year"),
                                      ColumnDefn("Series", "left", 200, "seriesname")])
        elif current_table == "series":
            self.olvtable.SetColumns([ColumnDefn("Series Id", "left", 50, "series_id"),
                                      ColumnDefn("Series Name", "left", 200, "seriesname"),
                                      ColumnDefn("Books Total", "left", 200, "bookstotal")])
        self.ShowAll(current_table)
    
    def ShowAll(self, current_table):
    
        self.olvtable.DeleteAllItems()
        if current_table == "book":
            result = self.session.query(BookTable.book_id, BookTable.title, BookTable.author, BookTable.copyright_year, SeriesTable.seriesname).join(SeriesTable)
            for row in result:
                rowinstance = OlvBookTable(row.book_id, row.title, row.author, row.copyright_year, row.seriesname)
                self.olvtable.AddObject(rowinstance)
        elif current_table == "series":
            result = self.session.query(SeriesTable)
            for row in result:
                rowinstance = OlvSeriesTable(row.series_id, row.seriesname, row.bookstotal)
                self.olvtable.AddObject(rowinstance)
        
    def OnChoice(self, event):
        
        self.current_table = self.tablecombo.GetStringSelection()
        self.AddCols(self.current_table)
        event.Skip()
    
    def OnAdd(self, event):
        
        if self.current_table == "book":
            AddRowtoBookDBDialog(self).ShowModal()
        elif self.current_table == "series":
            AddRowtoSeriesDBDialog(self).ShowModal()
        self.ShowAll(self.current_table)
        event.Skip()
        
    def OnEdit(self, event):
    
        rowobj = self.olvtable.GetSelectedObject()
        if self.current_table == "book":
            EditBookRowDialog(self, rowobj=rowobj).ShowModal()
        elif self.current_table == "series":
            EditSeriesRowDialog(self, rowobj=rowobj).ShowModal()
        self.ShowAll(self.current_table)
        event.Skip()
        
    def OnDelete(self, event):
    
        rowobj = self.olvtable.GetSelectedObject()
        if self.current_table == "book":
            target = self.session.query(BookTable).filter_by(book_id=rowobj.book_id).one()
            self.session.delete(target)
            self.session.commit()
            self.session.close()
        if self.current_table == "series":
            target = self.session.query(SeriesTable).filter_by(book_id=rowobj.book_id).one()
            self.session.delete(target)
            self.session.commit()
            self.session.close()
        self.ShowAll(self.current_table)
        event.Skip()

if __name__ == "__main__":
    # Import from my libraries
    from Components.frames import MaxFrame
    
    app = wx.App(redirect=True)
    frm = MaxFrame(None, "Books Database Editor")
    BooksDBPanel(frm)
    frm.Show()
    app.MainLoop()