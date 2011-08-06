import wx
from ClockGui import ClockPanel

class MediaPanel(wx.Panel):
    def __init__(self, parent, players=[]):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.players = players
        print("MediaPanel debug")
        print players
        self.InitUI(self.players)
    def InitUI(self, players):
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        vbox = wx.BoxSizer(wx.VERTICAL)
        toolbar = wx.ToolBar(self, -1)
        TOOL_ID = wx.NewId()
        TOOL_ID_COMBO = wx.NewId()
        combo = wx.ComboBox(toolbar, TOOL_ID_COMBO, choices = players)
        combo.SetSelection(0)
        toolbar.AddControl(combo)
        wx.EVT_COMBOBOX(self, TOOL_ID_COMBO, self.OnCombo)
        toolbar.Realize()
        vbox.Add(toolbar, 0, wx.EXPAND)
        Clock = ClockPanel(self)
        vbox.Add(Clock, 0, wx.EXPAND)
        gridSizer = wx.GridSizer(rows=4, cols=4, hgap=5, vgap=5)
        for i in range(gridSizer.GetRows() * gridSizer.GetCols()):
            gridSizer.Add(wx.StaticBitmap(self, wx.ID_ANY, bmp), 1, wx.EXPAND)
        vbox.Add(gridSizer, proportion=0, flag=wx.EXPAND)
        self.SetSizer(vbox)

    def OnCombo(self, e):
        self.parent.SetPlayer(e.GetEventObject().GetValue())

