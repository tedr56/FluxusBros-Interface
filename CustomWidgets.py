import wx
from wx.lib.agw.knobctrl import *
import rtmidi

class Control(wx.Object):
    def __init__(self, *args, **kwargs):
        #wx.EvtHandler.__init__(self,*args, **kwargs)
        self.InputCC = []
        self.InputNote = []
        self.InputOSC = []
        #self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
    def OnRightDown(self,event):
        self.PopupMenu(ControlContextMenu(self), event.GetPosition())
    def SetControl(self):
        print("Set Control")
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
    
class ControlContextMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent
        SetControl = wx.MenuItem(self, wx.NewId(), 'Set Control')
        self.AppendItem(SetControl)
        self.Bind(wx.EVT_MENU, self.OnSetControl, id=SetControl.GetId())

    def OnSetControl(self, event):
        self.parent.SetControl()
 
            
class wxFader(wx.Slider, Control):
    def __init__(self, *args, **kwargs):
        wx.Slider.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        Control.__init__(self)
        self.SetRange(0, 127)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
    def OnRightDown(self,event):
        self.PopupMenu(ControlContextMenu(self), event.GetPosition())
    def Update(self, input_type='cc', address=[0,0], value=0):
        self.SetValue(value)
    def getMessage(self):
        messages = []
        #Controls Event : Type = 0x18
        for c in self.InputCC:
            messageCC = rtmidi.MidiMessage()
            messageCC.controllerEvent(c[0] , c[1], self.GetValue())
            messages.append(messageCC)
        return messages
        
class wxCrossFader(wxFader):
    def __init__(self, *args, **kwargs):
        wxFader.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        self.SetRange(0, 127)

class wxKnob(KnobCtrl, Control):
    def __init__(self, parent, id=-1, size=(20, 20)):
        #KnobCtrl.__init__(self, *args, **kwargs)
        KnobCtrl.__init__(self, parent, id, size)
        Control.__init__(self)
        self.SetTags(range(0,127,1))
        self.SetAngularRange(-45, 225)
        self.SetValue(45)
        self.Bind(EVT_KC_ANGLE_CHANGED, self.OnAngleChanged, self)
        #self.SetFirstGradientColour(wx.Colour(255,0,0,255))
        #self.SetSecondGradientColour(wx.Colour(255,255,0,255))
        #self.SetBoundingColour(wx.Colour(0,255,0,255))
        #self.SetTagsColour(wx.Colour(0,0,255,192))
    def OnAngleChanged(self, event):
        print("Knob Scroll: %i" % event.GetValue())
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
        self.octave_notes =     ['w','b','w','b','w','w','b','w','b','w','b','w']
        self.octave_notes_pos = [ 0 ,0.5, 1 ,1.5, 2 , 3 ,3.5, 4 ,4.5, 5 ,5.5, 6 ]
        self.octaves = 4
        self.after_notes = 1
        self.start = 0
        self.octaves_on_screen = 4
        self.after_notes_on_screen = 1
        self.first_note_on_screen = 0
        self.before_notes_on_screen = 0
        self.Notes = []
        #self.SetBackgroundColour("BLACK")
        self.pDC = wx.PseudoDC()
        self.InitNotes(self.pDC)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x:None)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

    def InitNotes(self, dc):
        for i in range((self.octaves * 12) + self.after_notes):
            octave = int(math.floor (i/12))
            note = i % 12
            if 'w' == self.octave_notes[i % len(self.octave_notes)]:
                noteid = wx.NewId()
                whitenote = wxWhitePianoNote(self, noteid, octave, note)
                self.Notes.append(whitenote)
            elif 'b' == self.octave_notes[i % len(self.octave_notes)]:
                noteid = wx.NewId()
                blacknote = wxBlackPianoNote(self, noteid, octave, note)
                self.Notes.append(blacknote)
        self.DrawOctaves(dc)

    def GetNotesToDraw(self):
        last_note_on_screen = (self.octaves_on_screen * 12) + self.after_notes_on_screen
        return range(self.first_note_on_screen,last_note_on_screen)

    def DrawOctaves(self, dc):
        print("Draw Octaves")
        dc.RemoveAll()
        dc.BeginDrawing()
        notes_to_draw = self.GetNotesToDraw()
        notes_on_screen = len(notes_to_draw)
        for n in range(len(notes_to_draw)):
            if self.Notes[notes_to_draw[n]].GetColor() == 'w':
                self.DrawNote(dc, notes_to_draw[n], n)
        for n in notes_to_draw:
            if self.Notes[notes_to_draw[n]].GetColor() == 'b':
                self.DrawNote(dc, notes_to_draw[n], n)
        dc.EndDrawing()
        
    def DrawNote(self, dc, note, num_note):
        #print self.Notes[note].GetNote()
        notes = (self.octaves_on_screen * 7) + self.after_notes_on_screen
        w, h = self.GetSize()
        note_h = h
        note_w = int(round(w / notes))
        
        note_id = self.Notes[note].GetId()
        
        note_start =self.first_note_on_screen
        note_offset = self.Notes[note_start]
        note_pos = self.octave_notes_pos[note % 12]
        note_octave = int(math.floor(num_note/12))
        print note_octave
        note_octave_pos = (note_octave * 7 * note_w) + (note_pos * note_w)
                

        note_point = wx.Point(note_octave_pos,0)
        note_size  = wx.Size (note_w, note_h)
        dc.SetId(note_id)

        self.Notes[note].Update(dc, note_point, note_size)
        note_size = self.Notes[note].GetSize()
        note_height = note_size.GetHeight()
        note_width = note_size.GetWidth()
        note_rect  = wx.Rect (note_octave_pos, 0, note_width, note_height)        
        dc.SetIdBounds(note_id, note_rect)

    def OnPaint(self, event):
        w, h = self.GetSize()
        dc = wx.BufferedPaintDC(self)
        self.PrepareDC(dc)
        bg = wx.Brush(self.GetBackgroundColour())
        dc.SetBackground(bg)
        dc.Clear()
        self.pDC.DrawToDC(dc)

    def OnSize(self, event):
        self.DrawOctaves(self.pDC)
        self.Refresh()
    def SearchNoteId(self, Id):
        for i in range(len(self.Notes)):
            if self.Notes[i].GetId() == Id:
                return i
    def FindNote(self, event):
        hitradius = 1
        x , y = event.GetPositionTuple()
        l = self.pDC.FindObjects(x, y, hitradius)
        if l:
            first_note_detected = l[0]
            num_note = self.SearchNoteId(first_note_detected)
            return num_note
    def OnRightDown(self,event):
        note = self.FindNote(event)
        if note:
            self.Notes[note].OnRightDown(event)
    def OnLeftDown(self,event):
        note = self.FindNote(event)
        if note:
            self.NoteOn(note, False)
    def OnLeftUp(self,event):
        note = self.FindNote(event)
        if note:
            self.NoteOff(note, False)
    def NoteOn(self, note, play):
        self.Notes[note].NoteOn(play)
        #wx.CallAfter(self.DrawOctaves,self.pDC)
    def NoteOff(self, note, play):
        self.Notes[note].NoteOff(play)
        #wx.CallAfter(self.DrawOctaves,self.pDC)
        
class wxPianoNote(Control):
    def __init__(self, parent, Id, octave, note):
        Control.__init__(self)
        self.id = Id
        self.parent = parent
        self.octave = octave
        self.note = note
        self.notelist = ["C", "C#" , "D" , "D#" , "E" , "F" , "F#" , "G" , "G#" , "A" , "A#" , "B"]
        self.size = wx.Size(0,0)
        self.pos = wx.Point(0,0)
        self.played = False
    def OnRightDown(self,event):
        self.PopupMenu(ControlContextMenu(self), event.GetPosition())
    def GetId(self):
        return self.id
    def SetControl(self):
        print("Set Control Event Note")
    def Update(self, paint, pos, size):
        self.DrawNote(paint)
    def DrawNote(self, paint):
        paint.DrawRectanglePointSize(self.pos,self.size)
    def GetNote(self):
        return self.notelist[self.note % len(self.notelist)]
    def GetOctave(self):
        return self.octave
    def GetPos(self):
        return self.pos
    def GetSize(self):
        return self.size

    def OnRightDown(self,event):
        event.GetEventObject().PopupMenu(ControlContextMenu(self), event.GetPosition())        
    def OnLeftDown(self,event):
        self.NoteOn()
    def OnLeftUp(self,event):
        self.NoteOff()
    def NoteOn(self, play):  #Parametre play a True => Send Midi Message Note On
        print("Note On : %i %i" % (self.note, self.octave))
        self.played = True
    def NoteOff(self, play):  #Parametre play a True => Send Midi Message Note Off
        print("Note Off : %i %i" % (self.note, self.octave))
        self.played = False
    
class wxWhitePianoNote(wxPianoNote):
    def __init__(self, parent, ID, octave, note):
        wxPianoNote.__init__(self, parent, ID, octave, note)
    def Update(self, paint, pos, size):
        self.size = size
        self.pos = pos
        paint.SetPen(wx.Pen('BLACK'))
        if self.played:
            paint.SetBrush(wx.Brush('RED'))
        else:
            paint.SetBrush(wx.Brush('WHITE'))
        self.DrawNote(paint)
    def GetColor(self):
        return 'w'

class wxBlackPianoNote(wxPianoNote):
    def __init__(self, parent, ID, octave, note):
        wxPianoNote.__init__(self, parent, ID, octave, note)
    def Update(self, paint, pos, size):
        self.size = wx.Size(size[0], size[1] * 0.6)
        self.pos = pos
        new_size = [size[0], size[1] * 0.6]
        paint.SetPen(wx.Pen('WHITE'))
        if self.played:
            paint.SetBrush(wx.Brush('RED'))
        else:
            paint.SetBrush(wx.Brush('BLACK'))
        self.DrawNote(paint)

    def GetColor(self):
        return 'b'

