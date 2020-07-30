"Make sizers available"

import wx

class VBoxSizer(wx.BoxSizer):
    "Create a vertical boxsizer automatically."
    
    def __init__(self, orient=wx.VERTICAL):
        
        super().__init__(orient=orient)