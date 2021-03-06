"""
This launches other Python programs in one button-push.
"""

import os, sys, subprocess
import wx

from Components.frames import MaxFrame
from Components.sizers import VBoxSizer

class LaunchFrame(MaxFrame):
    
    def __init__(self,
                 parent=None, 
                 title='Programs Launcher'):
        
        super().__init__(parent, title=title)
        
        panel = wx.Panel(self)
        
        self.buttons = {'Inspecting Python Modules': 'inspectmodules.py',
                        "Books DB Editor": "booksdbeditor.py",
                        "Program Output": "programoutput.py",
                        "IoInteraction": "iointeraction.py"}
        
        buttonslist = []
        for name in self.buttons:
            button = wx.Button(panel, label=name)
            button.Bind(wx.EVT_BUTTON, self.OnButton)
            buttonslist.append(button)
        
        vsizer = VBoxSizer()
        
        for button in buttonslist:
            vsizer.Add(button, wx.EXPAND)
        
        panel.SetSizer(vsizer)
    
    def OnButton(self, event):
        
        button = event.GetEventObject()
        filepath = self.buttons[button.GetLabel()]
        subprocess.Popen([sys.executable, filepath], creationflags=subprocess.DETACHED_PROCESS)
        
        event.Skip()
        
app = wx.App()
LaunchFrame().Show()
app.MainLoop()