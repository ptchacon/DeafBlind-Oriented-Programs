"""
This module aims to take the standard Python library module inspect
and present as much info as possible for 
Braille display users of this GUI program
"""

import inspect, pprint, importlib
import wx

from Components.frames import MaxFrame
from Components.sizers import VBoxSizer


class InspectModules(MaxFrame):
    "Set the frame and its components for Inspect Modules program."
    
    def __init__(self, 
                 parent=None,
                 title='Inspecting Python Modules Processes'):
        
        super().__init__(parent=parent, title=title)
        
        panel = wx.Panel(self)
        
        # Building basic widgets
        self.entxl = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.entxl.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        self.insptree = wx.TreeCtrl(panel, style=wx.TR_DEFAULT_STYLE|wx.TR_HAS_BUTTONS)
        self.insptree.Bind(wx.EVT_TREE_KEY_DOWN, self.OnSpace)
        self.outxl = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        
        # Underlying BoxSizer
        vsizer = VBoxSizer()
        
        vsizer.Add(self.entxl, 0, wx.EXPAND)
        vsizer.Add(self.insptree, 2, wx.EXPAND)
        vsizer.Add(self.outxl, 1, wx.EXPAND)
        
        panel.SetSizer(vsizer)
    
    def OnEnter(self, event):
        "Process specific commands with entered data for output"
        
        self.myinput = self.entxl.GetValue()
        try:
            self.mod = importlib.import_module(self.myinput)
        except ModuleNotFoundError:
            self.outxl.WriteText("No such module!")
            self.outxl.SetInsertionPoint(0)
            self.outxl.SetFocus()
        else:
            self.ActivateInsptree()
        event.Skip()
        
    def ActivateInsptree(self):
        "Create the treectrl that show module info"
        
        self.insptree.DeleteAllItems()
        # Attach mod name to the root and its documentation to its event.
        root = self.insptree.AddRoot(self.myinput, data=self.mod)
        
        # Attach second-level hierarchy
        classesbutton = self.insptree.AppendItem(root, 'Classes')
        funcsbutton = self.insptree.AppendItem(root, "Functions")
        self.varbutton = self.insptree.AppendItem(root, "Variables")
        modulesbutton = self.insptree.AppendItem(root, "Modules")
            
        # Attach classes to Classes
        classlist = inspect.getmembers(self.mod, inspect.isclass)
        clobjlist = {}
        for (name, value) in classlist:
            clobj = self.insptree.AppendItem(classesbutton, 
                                             name, 
                                             data=value)
            clobjlist[name] = clobj
        
        # Attach methods to each class
        for name, clobj in clobjlist.items():
            obj = self.insptree.GetItemData(clobj)
            methodlist = dir(obj)
            for item in methodlist:
                if not item.startswith("_"):
                    try:
                        mobj = getattr(obj, item)
                    except: continue
                    try:
                        if not mobj.__qualname__.startswith("dep"):
                            self.insptree.AppendItem(clobj, mobj.__name__, data=mobj)
                    except:
                        self.insptree.AppendItem(clobj, item, data=mobj)
                
        # Attach functions to Functions
        funclist = inspect.getmembers(self.mod, inspect.isfunction)
        for (name, value) in funclist:
            if not value.__qualname__.startswith("dep"):
                self.insptree.AppendItem(funcsbutton, 
                                         value.__name__, 
                                         data=value)
        
        wholist = self.mod.__dict__
        for name, obj in wholist.items():
            if not inspect.isclass(obj) and not inspect.isfunction(obj) \
            and not inspect.ismodule(obj) and not inspect.isbuiltin(obj) \
            and not name.startswith("_"):
                self.insptree.AppendItem(self.varbutton, name, data=obj)
        
        self.insptree.SetFocus()
        
    def OnSpace(self, event):
        
        if event.GetKeyCode() == wx.WXK_SPACE:
            item = self.insptree.GetFocusedItem()
            object = self.insptree.GetItemData(item)
            data = ""
            if self.insptree.GetItemText(item) == 'Modules':
                data = inspect.getmembers(self.mod, inspect.ismodule)
            elif self.insptree.GetItemParent(item) == self.varbutton:
                data = object
            elif object:
                try:
                    data = inspect.getdoc(object)
                except:
                    data = 'No documentations here.'
            self.outxl.Clear()
            try:
                self.outxl.WriteText(data)
            except: self.outxl.WriteText(pprint.pformat(data))
            self.outxl.SetInsertionPoint(0)
            self.outxl.SetFocus()
        event.Skip()
        
app = wx.App(redirect=True)
InspectModules().Show()
app.MainLoop()