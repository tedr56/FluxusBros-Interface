import wx
import time
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
        self.ClockMode = 'Internal'
        self.internClock = InternalClock(self)
        self.TapList = []
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
    def InitUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, "Clock: ")
        self.Clock = wxClock(self,wx.NewId())
        self.Tap = wx.Button(self, wx.NewId(), "Tap", size=wx.Size(40, 25))
        hbox.Add(text, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.Clock, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.Tap, 0, wx.ALIGN_CENTER_VERTICAL)
        self.SetSizerAndFit(hbox)
        self.Bind(wx.EVT_BUTTON, self.OnTap, id=self.Tap.GetId())
        self.Layout()
    def OnTap(self, event):
        timeT = time.time()
        if self.ClockMode == 'Internal' and len(self.TapList) >= 1:
            if timeT - self.TapList[-1] > 2:
                self.TapList = [timeT]
            else:
                self.TapList += [timeT]
                if len(self.TapList) >= 5:
                    bpms = []
                    for i, t in enumerate(self.TapList):
                        if not i == 0:
                            bpms += [t - self.TapList[i - 1]]
                    bpm = float(sum(bpms)) / len(bpms)
                    bpm = 60 / bpm
                    self.SetBpm(bpm)
                    if len (self.TapList) >= 10:
                        self.TapList = self.TapList[1:]
        else:
            self.TapList = [timeT]
    def SetBpm(self, bpm):
        self.internClock.SetBpm(bpm)
    def SetClockMode(self, Mode):
        if Mode == 'Internal':
            self.internClock = InternalClock(self)
        elif Mode == 'External':
            self.internClock.Stop()
    def OnDestroy(self, event):
        print("ClockControl Destroy")
        self.internClock.OnDestroy(event)
        event.Skip()
        
        


