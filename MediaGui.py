import wx
from ClockGui import ClockPanel

class MediaPanel(wx.Panel):
    def __init__(self, parent, players=[]):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.players = players
        self.InitUI()
    def InitUI(self):
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        vbox = wx.BoxSizer(wx.VERTICAL)
        gridSizer = wx.GridSizer(rows=4, cols=4, hgap=5, vgap=5)
        for i in range(gridSizer.GetRows() * gridSizer.GetCols()):
            gridSizer.Add(wx.StaticBitmap(self, wx.ID_ANY, bmp), 1, wx.EXPAND)
        vbox.Add(gridSizer, proportion=0, flag=wx.EXPAND)
        self.SetSizer(vbox)

    def OnCombo(self, e):
        self.parent.SetPlayer(e)

