import wx
import rtmidi
from FaderSlider import wxFader
#try:
    #from agw import KnobCtrl
#    import agw
#except ImportError: # if it's not there locally, try the wxPython lib.
    #from wx.lib.agw import KnobCtrl
#import wx.lib.agw
from wx.lib.agw.knobctrl import KnobCtrl

class TablePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.InitUI()
        self.InitControls()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        self.knob1 = KnobCtrl(self)
        self.knob2 = KnobCtrl(self)
        self.knob3 = KnobCtrl(self)
        self.knob4 = KnobCtrl(self)
#        hbox0.Add(self.knob1, flag=wx.EXPAND)
#        hbox0.Add(self.knob2, flag=wx.EXPAND)
#        hbox0.Add(self.knob3, flag=wx.EXPAND)
#        hbox0.Add(self.knob4, flag=wx.EXPAND)
        hbox0.Add(self.knob1)
        hbox0.Add(self.knob2)
        hbox0.Add(self.knob3)
        hbox0.Add(self.knob4)                
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
        vbox.Add(hbox0, flag=wx.EXPAND|wx.ALL)
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
        
