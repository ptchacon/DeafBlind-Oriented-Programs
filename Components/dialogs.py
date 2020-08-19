"""
A place to hold customized dialogs
"""

# Import from wx
import wx
# Import from SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

# Import from my library
from Components.sizers import VBoxSizer
from Components.dbtablemodels import BookTable

class AddRowtoBookDBDialog(wx.Dialog):
    
    def __init__(self, parent, title="Add a Row to the Table"):
        
        super().__init__(parent, title=title)
        
        vsizer = VBoxSizer()
        
        self.panel = self.GetParent()
        self.tabletitle = self.panel.tablecombo.GetString(self.panel.tablecombo.GetCurrentSelection())
        metadata = MetaData()
        metadata.reflect(self.panel.engine)
        self.columntitles = list(metadata.tables[self.tabletitle].c.keys())
        self.entxtlist = []
        for title in self.columntitles[1:]:
            hsizer = wx.BoxSizer()
            stxt = wx.StaticText(self, label=title)
            entxt = wx.TextCtrl(self)
            self.entxtlist.append(entxt)
            hsizer.Add(stxt)
            hsizer.Add(entxt)
            vsizer.Add(hsizer)
        fhsizer = wx.BoxSizer()
        addbtn = wx.Button(self, label="Add the Data", id=wx.ID_OK)
        addbtn.Bind(wx.EVT_BUTTON, self.OnAdd)
        cancelbtn = wx.Button(self, label="Cancel")
        cancelbtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        fhsizer.Add(addbtn)
        fhsizer.Add(cancelbtn)
        vsizer.Add(fhsizer)
        
        self.SetSizer(vsizer)
        
    def OnAdd(self, event):
    
        listofents = []
        for obj in self.entxtlist:
            value = obj.GetValue()
            listofents.append(value)
        self.AddDatatoDB(listofents)
        self.Destroy()
        
    def OnCancel(self, event):
    
        self.Destroy()
        
    def AddDatatoDB(self, data):
        
        if self.tabletitle == "book":
            newobj = BookTable(title=data[0],
                               author=data[1],
                               copyright_year=int(data[2]),
                               series=data[3])
            Session = sessionmaker(bind=self.panel.engine)
            session = Session()
            session.add(newobj)
            session.commit()
            
class EditBookRowDialog(wx.Dialog):
    
    def __init__(self, parent, rowobj=None, title="Edit a Row in the Table"):
        
        super().__init__(parent, title=title)
        
        self.panel = self.GetParent()
        self.engine = self.panel.engine
        self.rowtoedit = list(self.panel.session.query(BookTable).filter_by(book_id=rowobj.book_id))
        self.tabletitle = self.panel.tablecombo.GetString(self.panel.tablecombo.GetCurrentSelection())
        
        metadata = MetaData()
        metadata.reflect(self.panel.engine)
        self.columntitles = list(metadata.tables[self.tabletitle].c.keys())
        vsizer = VBoxSizer()
        hsizer1 = wx.BoxSizer()
        stxt = wx.StaticText(self, label="Title")
        self.titleentxt = wx.TextCtrl(self, value=str(rowobj.title))
        hsizer1.Add(stxt)
        hsizer1.Add(self.titleentxt)
        vsizer.Add(hsizer1)
        hsizer2 = wx.BoxSizer()
        stxt = wx.StaticText(self, label="Author")
        self.authorentxt = wx.TextCtrl(self, value=str(rowobj.author))
        hsizer2.Add(stxt)
        hsizer2.Add(self.authorentxt)
        vsizer.Add(hsizer2)
        hsizer3 = wx.BoxSizer()
        stxt = wx.StaticText(self, label="Copyright Year")
        self.cryentxt = wx.TextCtrl(self, value=str(rowobj.copyright_year))
        hsizer3.Add(stxt)
        hsizer3.Add(self.cryentxt)
        vsizer.Add(hsizer3)
        hsizer4 = wx.BoxSizer()
        stxt = wx.StaticText(self, label="Series")
        self.seriesentxt = wx.TextCtrl(self, value=str(rowobj.title))
        hsizer4.Add(stxt)
        hsizer4.Add(self.seriesentxt)
        vsizer.Add(hsizer4)
        fhsizer = wx.BoxSizer()
        editbtn = wx.Button(self, label="Edit the Data", id=wx.ID_OK)
        editbtn.Bind(wx.EVT_BUTTON, self.OnEdit)
        cancelbtn = wx.Button(self, label="Cancel")
        cancelbtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        fhsizer.Add(editbtn)
        fhsizer.Add(cancelbtn)
        vsizer.Add(fhsizer)
        
        self.SetSizer(vsizer)
        
    def OnEdit(self, event):
    
        data = []
        data.append(self.titleentxt.GetValue())
        data.append(self.authorentxt.GetValue())
        data.append(self.cryentxt.GetValue())
        data.append(self.seriesentxt.GetValue())
        self.AddDatatoDB(data)
        self.Destroy()
        
    def OnCancel(self, event):
    
        self.Destroy()
        
    def AddDatatoDB(self, data):
        
        if self.tabletitle == "book":
            newobj = BookTable(title=data[0],
                               author=data[1],
                               copyright_year=int(data[2]),
                               series=data[3])
            Session = sessionmaker(bind=self.panel.engine)
            session = Session()
            session.add(newobj)
            session.commit()