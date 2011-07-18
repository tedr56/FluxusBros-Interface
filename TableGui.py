import wx
from FaderSlider import wxFader
import rtmidi

class TablePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.fader1 = wxFader(self)
        self.fader2 = wxFader(self)
        self.fader3 = wxFader(self)
        self.fader4 = wxFader(self)
        hbox1.Add(self.fader1, flag=wx.EXPAND)
        hbox1.Add(self.fader2, flag=wx.EXPAND)
        hbox1.Add(self.fader3, flag=wx.EXPAND)
        hbox1.Add(self.fader4, flag=wx.EXPAND)
        vbox.Add(hbox1, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)
        
