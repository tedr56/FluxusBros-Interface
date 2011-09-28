import wx
from ClockGui import ClockPanel
from CustomWidgets import wxMediaVisual

class MediaPanel(wx.Panel):
    def __init__(self, parent, players=[], config_file=None):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.players = players
        self.config_file = config_file
        self.InitUI()
    def InitUI(self):
        gridSizer = wx.GridSizer(rows=4, cols=4, hgap=0, vgap=0)
        for i in range(gridSizer.GetRows() * gridSizer.GetCols()):
            gridSizer.Add(wxMediaVisual(self, wx.NewId()), 1, wx.EXPAND)
        self.SetSizer(gridSizer)
    #~ def InitConfig(self, profile):
        
    def OnCombo(self, e):
        self.parent.SetPlayer(e)

    def UpdateSizer(self):
        self.parent.Layout()
