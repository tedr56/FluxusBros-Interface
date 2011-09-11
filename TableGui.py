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
        self.knob1 = wxKnob(self,wx.NewId())
        self.knob2 = wxKnob(self,wx.NewId())
        self.knob3 = wxKnob(self,wx.NewId())
        self.knob4 = wxKnob(self,wx.NewId())
        self.knob5 = wxKnob(self,wx.NewId())
        self.knob6 = wxKnob(self,wx.NewId())
        self.knob7 = wxKnob(self,wx.NewId())
        self.knob8 = wxKnob(self,wx.NewId())
        #~ self.Bind(EVT_KC_ANGLE_CHANGING, self.OnKnobChanged, self.knob1)
#        hbox0.Add(self.knob1, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
#        hbox0.Add(self.knob2, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
#        hbox0.Add(self.knob3, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
#        hbox0.Add(self.knob4, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
#        vbox.Add(hbox0, proportion=1, flag=wx.EXPAND|wx.ALL)
        knob_proportion = 1
        knob_flag = wx.SHAPED|wx.ALL|wx.FIXED_MINSIZE
        knob_border = 3

        hbox0.Add(self.knob1, proportion=knob_proportion, flag=knob_flag, border=knob_border)
        hbox0.Add(self.knob2, proportion=knob_proportion, flag=knob_flag, border=knob_border)
        hbox0.Add(self.knob3, proportion=knob_proportion, flag=knob_flag, border=knob_border)
        hbox0.Add(self.knob4, proportion=knob_proportion, flag=knob_flag, border=knob_border)
        hbox0.Add(self.knob5, proportion=knob_proportion, flag=knob_flag, border=knob_border)
        hbox0.Add(self.knob6, proportion=knob_proportion, flag=knob_flag, border=knob_border)
        hbox0.Add(self.knob7, proportion=knob_proportion, flag=knob_flag, border=knob_border)
        hbox0.Add(self.knob8, proportion=knob_proportion, flag=knob_flag, border=knob_border)
        #vbox.Add(hbox0, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox0, proportion=1, flag=wx.SHAPED)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.fader1 = wxFader(self,wx.NewId())
        self.fader2 = wxFader(self,wx.NewId())
        self.fader3 = wxFader(self,wx.NewId())
        self.fader4 = wxFader(self,wx.NewId())
        self.fader5 = wxFader(self,wx.NewId())
        self.fader6 = wxFader(self,wx.NewId())
        self.fader7 = wxFader(self,wx.NewId())
        self.fader8 = wxFader(self,wx.NewId())
        hbox1.Add(self.fader1, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
        hbox1.Add(self.fader2, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
        hbox1.Add(self.fader3, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
        hbox1.Add(self.fader4, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
        hbox1.Add(self.fader5, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
        hbox1.Add(self.fader6, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
        hbox1.Add(self.fader7, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
        hbox1.Add(self.fader8, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)
        vbox.Add(hbox1, proportion=2, flag=wx.EXPAND|wx.ALL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.piano = wxPiano(self)
        #~ self.Bind(wx.EVT_MOUSE_EVENTS, self.OnPianoChanged, self.piano)
        hbox2.Add(self.piano,proportion = 1,flag=wx.EXPAND)
        vbox.Add(hbox2,proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)

        
    def OnKnobChanged(self, event):
        print("Knob!")
        #event_object = event.GetEventObject()
        #message = event_object.getValue()
        #print message
        #print event.GetValue()

    #~ def OnPianoChanged(self, event):
        #~ print ("Note!!")
        #~ event_object = event.GetEventObject()
        #~ message = event_object.getMessage()
        #~ self.parent.MidiOutputRefresh(message)
        
    def InitControls(self):
        self.knob1.SetInput(input_type = 'CC', address = [2,16])
        self.knob2.SetInput(input_type = 'CC', address = [2,17])
        self.knob3.SetInput(input_type = 'CC', address = [2,18])
        self.knob4.SetInput(input_type = 'CC', address = [2,19])
        self.knob5.SetInput(input_type = 'CC', address = [2,20])
        self.knob6.SetInput(input_type = 'CC', address = [2,21])
        self.knob7.SetInput(input_type = 'CC', address = [2,22])
        self.knob8.SetInput(input_type = 'CC', address = [2,23])
        self.fader1.SetInput(input_type = 'CC', address = [2,24])
        self.fader2.SetInput(input_type = 'CC', address = [2,25])
        #~ self.fader3.SetInput(input_type = 'Note', address = [1,48])
        self.fader3.SetInput(input_type = 'CC', address = [2, 26])
        self.fader4.SetInput(input_type = 'CC', address = [2,27])
        self.fader5.SetInput(input_type = 'CC', address = [2,28])
        self.fader6.SetInput(input_type = 'CC', address = [2,29])
        self.fader7.SetInput(input_type = 'CC', address = [2,30])
        self.fader8.SetInput(input_type = 'CC', address = [2,31])
