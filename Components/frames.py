"""
This module sets up Frames to specific preferences.
"""

import wx

class MaxFrame(wx.Frame):
    "Frame with maxed window set."
    
    def __init__(self, 
                 parent, 
                 title=''):
        "Initialize construction of Frame from wx.Frame"
        
        super().__init__(parent, 
                         title=title, 
                         style=wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE)
        
if __name__ == '__main__':
    app = wx.App()
    MyFrame(None, 'Testing Frame').Show()
    app.MainLoop()