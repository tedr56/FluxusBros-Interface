import wx
import rtmidi
from CustomWidgets import wxFader
from CustomWidgets import wxKnob
from CustomWidgets import wxPiano
from wx.lib.agw.knobctrl import *

class TablePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.InitUI()
        self.InitControls()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        self.knob1 = wxKnob(self)
        self.knob2 = wxKnob(self)
        self.knob3 = wxKnob(self)
        self.knob4 = wxKnob(self)
        print self.knob1.GetMaxValue()
        self.Bind(EVT_KC_ANGLE_CHANGING, self.OnKnobChanged, self.knob1)
        hbox0.Add(self.knob1)
        hbox0.Add(self.knob2)
        hbox0.Add(self.knob3)
        hbox0.Add(self.knob4)
        vbox.Add(hbox0, proportion=1, flag=wx.EXPAND|wx.ALL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.fader1 = wxFader(self)
        self.fader2 = wxFader(self)
        self.fader3 = wxFader(self)
        self.fader4 = wxFader(self)
        self.Bind(wx.EVT_SCROLL, self.OnScrollChanged, self.fader1)
        hbox1.Add(self.fader1, proportion=1, flag=wx.EXPAND|wx.ALL)
        hbox1.Add(self.fader2, proportion=1, flag=wx.EXPAND|wx.ALL)
        hbox1.Add(self.fader3, proportion=1, flag=wx.EXPAND|wx.ALL)
        hbox1.Add(self.fader4, proportion=1, flag=wx.EXPAND|wx.ALL)
        vbox.Add(hbox1, proportion=2, flag=wx.EXPAND|wx.ALL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.piano = wxPiano(self)
        hbox2.Add(self.piano,proportion = 1,flag=wx.EXPAND)
        vbox.Add(hbox2,proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)
    def OnKnobChanged(self, event):
        print("Knob!")
        #event_object = event.GetEventObject()
        #message = event_object.getValue()
        #print message
        #print event.GetValue()
    def OnScrollChanged(self, event):
        print("Scroll!")
        event_object = event.GetEventObject()
        message = event_object.getMessage()
        self.parent.MidiOutputRefresh(message)
    def InitControls(self):
        self.fader1.SetInput(input_type = 'CC', address = [2,24])
        self.fader2.SetInput(input_type = 'CC', address = [2,25])
        self.fader3.SetInput(input_type = 'Note', address = [1,48])
        self.parent.SetControls(self.fader1.Update, self.fader1.GetInputs())
        self.parent.SetControls(self.fader2.Update, self.fader2.GetInputs())
        self.parent.SetControls(self.fader3.Update, self.fader3.GetInputs())
