import wx

class Control:
    def __init__(self):
        self.InputCC = []
        self.InputNote = []
        self.InputOSC = []
    def SetInput(self, inputtype, address, option = None):
        if inputtype=='CC' or inputtype=='cc':
            self.SetMidiCCInput(address, option)
        elif inputtype=='note' or inputtype=='Note':
            self.SetMidiNoteInput(address, option)
        elif inputtype=='OSC' or inputtype=='osc':
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
    def Update(self, Value):
        self.SetValue(Value)
        
class wxCrossFader(wxFader):
    def __init__(self, *args, **kwargs):
        wx.Slider.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        self.SetRange(0, 127)


        
    
