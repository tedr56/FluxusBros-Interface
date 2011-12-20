import wx
from CustomWidgets import wxClock
from CustomWidgets import InternalClock

class ClockPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.InitUI()
    def InitUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, "Clock: ")
        self.Clock = wxClock(self,wx.NewId())
        hbox.Add(text, 0, wx.EXPAND)
        hbox.Add(self.Clock, 0, wx.EXPAND)
        self.SetSizer(hbox)

class ClockControl(wx.PyControl):
    def __init__(self, *args, **kwargs):
        wx.PyControl.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.InitUI()
        #~ print("Clock")
        self.internClock = InternalClock(self)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
    def InitUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, "Clock: ")
        self.Clock = wxClock(self,wx.NewId())
        hbox.Add(text, 0, wx.EXPAND)
        hbox.Add(self.Clock, 1, wx.EXPAND)
        self.SetSizerAndFit(hbox)
        #self.Fit()
        self.Layout()
    def SetBpm(self, bpm):
        self.internClock.SetBpm(bpm)
    def SetClockMode(self, Mode):
        if Mode == 'Internal':
            self.internClock.Start()
        elif Mode == 'External':
            self.internClock.Stop()
    def OnDestroy(self, event):
        print("ClockControl Destroy")
        self.internClock.OnDestroy(event)
        event.Skip()
        
        


