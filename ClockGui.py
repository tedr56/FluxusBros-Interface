import wx
from CustomWidgets import wxClock

class ClockPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.InitUI()
    def InitUI(self):
        #vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, "Clock: ")
        self.Clock = wxClock(self)
        hbox.Add(text, 0, wx.EXPAND)
        hbox.Add(self.Clock, 0, wx.EXPAND)
        #vbox.Add(hbox, wx.EXPAND)
        self.SetSizer(hbox)
        self.InitClock()
    def InitClock(self):
        self.parent.SetControls(self.Clock.Update, self.Clock.GetInputs())
