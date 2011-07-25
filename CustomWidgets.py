import wx
from wx.lib.agw.knobctrl import *
import rtmidi

class Control:
    def __init__(self):
        self.InputCC = []
        self.InputNote = []
        self.InputOSC = []
    def SetInput(self, input_type='CC', address=[0,0], option = None):
        if input_type=='CC' or input_type=='cc':
            self.SetMidiCCInput(address, option)
        elif input_type=='note' or input_type=='Note':
            self.SetMidiNoteInput(address, option)
        elif input_type=='OSC' or input_type=='osc':
            self.SetOSCInput(address, option)
    def SetMidiCCInput(self, address, option=None):
        self.InputCC.append(address)
    def SetMidiNoteInput(self, address, option=None):
        self.InputNote.append(address)
    def SetMidiOSCInput(self, address, option=None):
        self.InputOSC.append(address)
    def GetInputs(self):
        inputs= {'CC': self.GetMidiCCInputs(), 'Note':self.GetMidiNoteInputs(), 'OSC':self.GetMidiOSCInputs()}
        return inputs
    def GetMidiCCInputs(self):
        return self.InputCC
    def GetMidiNoteInputs(self):
        return self.InputNote
    def GetMidiOSCInputs(self):
        return self.InputOSC
    
    
            
class wxFader(wx.Slider, Control):
    def __init__(self, *args, **kwargs):
        wx.Slider.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        Control.__init__(self)
        self.SetRange(0, 127)
    def Update(self, input_type='cc', address=[0,0], value=0):
        self.SetValue(value)
    def getMessage(self):
        messages = []
        #Controls Event : Type = 0x18
        for c in self.InputCC:
            messageCC = rtmidi.MidiMessage()
            #print c
            messageCC.controllerEvent(c[0] , c[1], self.GetValue())
            messages.append(messageCC)
        return messages
        
class wxCrossFader(wxFader):
    def __init__(self, *args, **kwargs):
        wx.Slider.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        self.SetRange(0, 127)

class wxKnob(KnobCtrl, Control):
    def __init__(self, *args, **kwargs):
        KnobCtrl.__init__(self, *args, **kwargs)
        Control.__init__(self)
        self.SetTags([0,127])
        #self.SetFirstGradientColour(wx.Colour(255,0,0,255))
        #self.SetSecondGradientColour(wx.Colour(255,255,0,255))
        #self.SetBoundingColour(wx.Colour(0,255,0,255))
        #self.SetTagsColour(wx.Colour(0,0,255,192))

    
