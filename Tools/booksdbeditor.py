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
from Components.dialogs import AddRowtoBookDBDialog, EditBookRowDialog
from Components.dbtablemodels import BookTable, OlvBookTable

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
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        metadata = MetaData(bind=self.engine)
        metadata.reflect(bind=self.engine)
        tables = metadata.tables
        
        super().__init__(parent)
        vsizer = VBoxSizer()
        
        hsizer1 = wx.BoxSizer()
        combolab = wx.StaticText(self, label="Pick a table:")
        self.tablenames = list(tables.keys())
        self.tablecombo = wx.Choice(self, choices=self.tablenames)
        self.tablecombo.SetSelection(0)
        self.tablecombo.Bind(wx.EVT_CHOICE, self.OnChoice)
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
        
        self.AddCols()
        
    def CreateDB(self, dbfilename):
        
        self.engine = create_engine(f"sqlite:///{dbfilename}")
        metadata = BookTable.metadata
        metadata.create_all(bind=self.engine)
        
    def AddCols(self):
        
        current_table = self.tablecombo.GetStringSelection()
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        tableobject = metadata.tables[current_table]
        for col in tableobject.columns:
            if col.name == "book_id": continue
            if col.name == "copyright_year":
                self.olvtable.AddColumnDefn(ColumnDefn("Copyright Year", width=100, valueGetter="copyright_year"))
                continue
            self.olvtable.AddColumnDefn(ColumnDefn(col.name.title(), width=100, valueGetter=col.name))
        self.olvtable.RepopulateList()
        self.ShowAll()
    
    def ShowAll(self):
    
        self.olvtable.DeleteAllItems()
        current_table = self.tablecombo.GetStringSelection()
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        tableobject = metadata.tables[current_table]
        tablecontents = self.session.query(tableobject).all()
        for row in tablecontents:
            rowinstance = OlvBookTable(book_id=row[0],
                                       title=row[1],
                                       author=row[2],
                                       copyright_year=row[3],
                                       series=row[4])
            self.olvtable.AddObject(rowinstance)
    
    def OnChoice(self, event):
        
        self.ShowAll()
        event.Skip()
    
    def OnAdd(self, event):
        
        AddRowtoBookDBDialog(self).ShowModal()
        self.ShowAll()
        event.Skip()
        
    def OnEdit(self, event):
    
        rowobj = self.olvtable.GetSelectedObject()
        EditBookRowDialog(self, rowobj=rowobj).ShowModal()
        self.ShowAll()
        event.Skip()
        
    def OnDelete(self, event):
    
        rowobj = self.olvtable.GetSelectedObject()
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        if self.tablecomboselection == "book":
            Session = sessionmaker(bind=self.engine)
            session = Session()
            target = session.query(BookTable).filter_by(book_id=rowobj.book_id).one()
            session.delete(target)
        self.ShowAll()
        event.Skip()

if __name__ == "__main__":
    # Import from my libraries
    from Components.frames import MaxFrame
    
    app = wx.App(redirect=True)
    frm = MaxFrame(None, "Books Database Editor")
    BooksDBPanel(frm)
    frm.Show()
    app.MainLoop()