import wx
from FaderSlider import wxFader
import rtmidi

class TablePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.InitUI()
        self.InitControls()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.fader1 = wxFader(self)
        self.fader2 = wxFader(self)
        self.fader3 = wxFader(self)
        self.fader4 = wxFader(self)
        self.Bind(wx.EVT_SCROLL, self.OnScrollChanged, self.fader1)
        #self.fader1.Connect(wx.EVT_SCROLL, self.faderscrolled())
        #EVT_SCROLL_THUMBTRACK
        hbox1.Add(self.fader1, flag=wx.EXPAND)
        hbox1.Add(self.fader2, flag=wx.EXPAND)
        hbox1.Add(self.fader3, flag=wx.EXPAND)
        hbox1.Add(self.fader4, flag=wx.EXPAND)
        vbox.Add(hbox1, proportion=1, flag=wx.EXPAND|wx.ALL)
        self.SetSizer(vbox)
    def OnScrollChanged(self, event):
        print("Scroll!")
        event_object = event.GetEventObject()
        message = event_object.getMessage()
        #print message
        self.parent.MidiOutputRefresh(message)
    def InitControls(self):
        self.fader1.SetInput(input_type = 'CC', address = [2,24])
        self.fader2.SetInput(input_type = 'CC', address = [2,25])
        self.fader3.SetInput(input_type = 'Note', address = [1,48])
        self.parent.SetControls(self.fader1.Update, self.fader1.GetInputs())
        self.parent.SetControls(self.fader2.Update, self.fader2.GetInputs())
        self.parent.SetControls(self.fader3.Update, self.fader3.GetInputs())
        
