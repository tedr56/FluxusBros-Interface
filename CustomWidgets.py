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

class wxPiano(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        ID_OCTAVE_DOWN = wx.NewId()
        ID_OCTAVE_UP = wx.NewId()
        OctaveDown = wx.Button(self, ID_OCTAVE_DOWN, '<')
        OctaveUp = wx.Button(self, ID_OCTAVE_UP, '>')
        hbox0.Add(OctaveDown, proportion=1, flag=wx.EXPAND)
        hbox0.Add(OctaveUp, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox0, proportion=0, flag=wx.EXPAND)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        ID_PIANO_ROLL = wx.NewId()
        pianoroll=wxPianoRoll(parent=self, id=ID_PIANO_ROLL)
        hbox1.Add(pianoroll, proportion=1, flag=wx.EXPAND|wx.ALL)
        vbox.Add(hbox1, proportion=3, flag=wx.EXPAND)
        self.SetSizer(vbox)
        
class wxPianoRoll(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.parent = kwargs['parent']
        self.octaves = 3
        self.octaves_on_screen = 2
        self.after_notes_on_screen = 1
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        self.Refresh()

    def OnPaint(self, event):
        self.dc = wx.PaintDC(self)
        for o in range(int(math.floor(self.octaves_on_screen))):
            self.DrawOctave(start=o)
        self.DrawOctave(start=self.octaves_on_screen, l=self.after_notes_on_screen)
    def DrawOctave(self, start=0, l=12):
        w, h = self.GetSize()
        Note_H = h
        notes_on_screen = (self.octaves_on_screen * 7) + self.after_notes_on_screen
        Note_W = int(round(w / notes_on_screen))
        octave_start = start * Note_W * 7
        octave_long = int(round (l))
        octave_notes =       ['w','b','w','b','w','w','b','w','b','w','b','w']
        octave_notes_order = [ 0 , 0 , 1 , 1 , 2 , 3 , 2 , 4 , 3 , 5 , 4 , 6 ]
        black_notes_pos = [0.5 , 1.5 , 3.5 , 4.5 , 5.5]
        white_notes_pos = [0, 1 , 2 , 3 , 4 , 5 , 6 , 7]
        for n in range(l):
            octave_note = octave_notes[n]
            if octave_note == 'w':
                white_note = octave_notes_order[n]
                white_note_pos = white_notes_pos[white_note]
                self.dc.SetPen(wx.Pen('BLACK'))
                self.dc.SetBrush(wx.Brush('WHITE'))
                self.dc.DrawRectanglePointSize(wx.Point(octave_start + (1 + (white_note_pos * Note_W)), 0) , wx.Size(Note_W, Note_H))
                #print("N:%i Clr:%s Pos:%f" % (n , octave_note , white_note_pos))
        for n in range(l):
            octave_note = octave_notes[n]
            if octave_note == 'b':
                black_note = octave_notes_order[n]
                black_note_pos = black_notes_pos[black_note]
                self.dc.SetPen(wx.Pen('WHITE'))
                self.dc.SetBrush(wx.Brush('BLACK'))
                self.dc.DrawRectanglePointSize(wx.Point(octave_start + (1 + (black_note_pos * Note_W)), 0) , wx.Size(Note_W, Note_H * 0.6))
            
