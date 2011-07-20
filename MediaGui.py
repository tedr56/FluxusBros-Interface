import wx

class MediaPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.InitUI()
    def InitUI(self):
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        vbox = wx.BoxSizer(wx.VERTICAL)
        toolbar = wx.ToolBar(self, -1)
        TOOL_ID = wx.NewId()
        TOOL_ID_COMBO = wx.NewId()
        combo = wx.ComboBox(toolbar, TOOL_ID_COMBO, choices = ["MicroKontrol", "VMXVJ", "BitStream3X"])
        combo.SetSelection(0)
        toolbar.AddControl(combo)
        wx.EVT_COMBOBOX(self, TOOL_ID_COMBO, self.OnCombo)
        toolbar.Realize()
        vbox.Add(toolbar, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 4 )
        gridSizer = wx.GridSizer(rows=4, cols=4, hgap=5, vgap=5)
        for i in range(gridSizer.GetRows() * gridSizer.GetCols()):
            gridSizer.Add(wx.StaticBitmap(self, wx.ID_ANY, bmp), 0, wx.EXPAND)
        vbox.Add(gridSizer, proportion=1, flag=wx.EXPAND|wx.ALL)
        self.SetSizer(vbox)
    def OnCombo(self, e):
        self.parent.SetPlayer(e)

