import wx

class MediaPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.InitUI()
    def InitUI(self):
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        #titleIco1 = wx.StaticBitmap(self, wx.ID_ANY, bmp)
        #titleIco2 = wx.StaticBitmap(self, wx.ID_ANY, bmp)
        vbox = wx.BoxSizer(wx.VERTICAL)
        gridSizer = wx.GridSizer(rows=4, cols=4, hgap=5, vgap=5)
        for i in range(gridSizer.GetRows() * gridSizer.GetCols()):
            gridSizer.Add(wx.StaticBitmap(self, wx.ID_ANY, bmp), 0, wx.EXPAND)

        vbox.Add(gridSizer, proportion=1, flag=wx.EXPAND|wx.ALL)
        self.SetSizer(vbox)
