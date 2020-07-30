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
        
        self.ActivateInsptree()
        event.Skip()
        
    def ActivateInsptree(self):
        "Create the treectrl that show module info"
        
        myinput = self.entxl.GetValue()
        self.insptree.DeleteAllItems()
        # Create the inspected module object
        self.mod = importlib.import_module(myinput)
        
        # Attach mod name to the root and its documentation to its event.
        root = self.insptree.AddRoot(myinput, data=self.mod)
        
        # Attach second-level hierarchy
        classesbutton = self.insptree.AppendItem(root, 'Classes')
        funcsbutton = self.insptree.AppendItem(root, "Functions")
        modulesbutton = self.insptree.AppendItem(root, "Modules")
            
        # Attach classes to Classes
        classlist = inspect.getmembers(self.mod, inspect.isclass)
        clobjlist = []
        for (name, value) in classlist:
            clobj = self.insptree.AppendItem(classesbutton, 
                                             name, 
                                             data=value)
            clobjlist.append(clobj)
        
        # Attach methods to each class
        for clobj in clobjlist:
            obj = self.insptree.GetItemData(clobj)
            methodlist = inspect.getmembers(obj, inspect.isfunction)
            for method in methodlist:
                name = method[1].__qualname__
                self.insptree.AppendItem(clobj, name, data=method[1])
        
        # Attach functions to Functions
        funclist = inspect.getmembers(self.mod, inspect.isfunction)
        for (name, value) in funclist:
            self.insptree.AppendItem(funcsbutton, 
                                     value.__qualname__, 
                                     data=value)
        
        self.insptree.SetFocus()
        
    def OnSpace(self, event):
        
        if event.GetKeyCode() == wx.WXK_SPACE:
            item = self.insptree.GetFocusedItem()
            object = self.insptree.GetItemData(item)
            if object:
                data = inspect.getdoc(object)
                if data is None:
                    data = 'No documentations here.'
            elif self.insptree.GetItemText(item) == 'Modules':
                data = inspect.getmembers(self.mod, inspect.ismodule)
                data = pprint.pformat(data)
            self.outxl.Clear()
            self.outxl.write(data)
            self.outxl.SetInsertionPoint(0)
            self.outxl.SetFocus()
        event.Skip()
        
app = wx.App()
InspectModules().Show()
app.MainLoop()