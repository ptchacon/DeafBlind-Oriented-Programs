import os, subprocess

import wx

from Components.frames import MaxFrame
from Components.sizers import VBoxSizer


class PyOutputFrame(MaxFrame):
    
    def __init__(self, title="Program Output"):
        
        super().__init__(None, title=title)
        
        menubar = wx.MenuBar()
        actionmenu = wx.Menu()
        chdirmenuitem = actionmenu.Append(wx.ID_ANY, 'Change Current Dir')
        menubar.Append(actionmenu, '&Action')
        self.Bind(wx.EVT_MENU, self.OnChange, chdirmenuitem)
        self.SetMenuBar(menubar)
        
        panel = wx.Panel(self)
        self.entxt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.entxt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        self.outxt = wx.TextCtrl(panel, style=wx.TE_MULTILINE|
                                              wx.TE_READONLY|
                                              wx.TE_BESTWRAP)
        
        sizer = VBoxSizer()
        sizer.Add(self.entxt, 0, wx.EXPAND)
        sizer.Add(self.outxt, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        
    def OnEnter(self, event):
        
        self.outxt.Clear()
        cmd = self.entxt.GetValue()
        proc = subprocess.run(cmd, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.STDOUT,
                              shell=True,
                              text=True)
        self.outxt.write(proc.stdout)
        self.outxt.SetInsertionPoint(0)
        self.outxt.SetFocus()
        
    def OnChange(self, event):
        
        dlg = wx.DirDialog(self, style=wx.DD_CHANGE_DIR)
        dlg.ShowModal()

if __name__ == '__main__':
    app = wx.App()
    frm = PyOutputFrame()
    frm.Show()
    app.MainLoop()