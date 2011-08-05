import wx
from wx.lib.agw.knobctrl import *
from MessageDispatch import *
import rtmidi

MIDI_CLOCK_TICK = 0x48
class Control(wx.PyControl):
    def __init__(self, parent, GetControlValue=None, InitValue=0):
        wx.PyControl.__init__(self, parent)
        self.InputCC    = []
        self.InputNote  = []
        self.InputSysEx = []
        self.InputOSC   = []
        self.InputClock = []
        if GetControlValue == None:
            self.getvalue = self.NoGetValue
        else:
            self.getvalue = GetControlValue
    def NoGetValue(self):
        return 0
    def OnRightDown(self,event):
        self.PopupMenu(ControlContextMenu(self), event.GetPosition())
    def SetControl(self):
        print("Set Control")
    def SetInput(self, input_type='CC', address=[0,0], option = None):
        wx.PostEvent(self, MessageRecord(self, input_type, address, option))
        if input_type=='CC' or input_type=='cc':
            self.SetMidiCCInput(address, option)
        elif input_type=='note' or input_type=='Note':
            self.SetMidiNoteInput(address, option)
        elif input_type=='OSC' or input_type=='osc':
            self.SetOSCInput(address, option)
        elif input_type=='SysEx':
            self.SetMidiSysExInput(address)
        elif input_type=='clock' or input_type=='Clock':
            self.SetMidiClockInput(address)
    def SetMidiCCInput(self, address, option=None):
        self.InputCC.append(address)
    def SetMidiNoteInput(self, address, option=None):
        self.InputNote.append(address)
    def SetOSCInput(self, address, option=None):
        self.InputOSC.append(address)
    def SetMidiClockInput(self, address):
        self.InputClock.append(0x48)
    def SetMidiSysExInput(self,address):
        self.InputSysEx.append(address)
    def GetInputs(self):
        inputs= {'CC': self.GetMidiCCInputs(), 'Note':self.GetMidiNoteInputs(), 'OSC':self.GetMidiOSCInputs(), 'SysEx':self.GetMidiSysExInputs(), 'Clock':self.GetMidiClockInputs()}
        return inputs
    def GetMidiCCInputs(self):
        return self.InputCC
    def GetMidiNoteInputs(self):
        return self.InputNote
    def GetMidiOSCInputs(self):
        return self.InputOSC
    def GetMidiSysExInputs(self):
        return self.InputSysEx
    def GetMidiClockInputs(self):
        return self.InputClock
    def GetControlValue(self):
        return self.getvalue()
    def getMessage(self):
        msg = []
        value = self.GetControlValue()
        
        if self.InputCC:
            print("Input CC")
            print self.InputCC
            for c in self.InputCC:
                messageCC = rtmidi.MidiMessage().controllerEvent(c[0] , c[1], value)
                msg.append(messageCC)
        else:
            print("No input CC")
        #if self.InputNote:
        #    print("Input Note")
        #    print self.InputNote        
        #    for n in self.InputNote:
        #        if value:
        #            messageNote = rtmidi.MidiMessage().noteOn(n[0] , n[1], value)
        #        else:
        #            messageNote = rtmidi.MidiMessage().noteOff(n[0] , n[1])
        #        msg.append(messageNote)
        #else:
        #    print("No input Note")
        #print value
        return msg
class ControlContextMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent
        SetControl = wx.MenuItem(self, wx.NewId(), 'Set Control')
        self.AppendItem(SetControl)
        self.Bind(wx.EVT_MENU, self.OnSetControl, id=SetControl.GetId())

    def OnSetControl(self, event):
        self.parent.SetControl()
 
class wxMidiPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
class wxFader(wx.Slider):
    def __init__(self, *args,  **kwargs):
        self.parent = args[0]
        self.FaderId = args[1]
        wx.Slider.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        self.SetRange(0, 127)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.OnScrolled)
        EVT_WIDGET_MESSAGE(self, self.GetMessage)
        EVT_WIDGET_UPDATE(self, self.WidgetUpdate)
    def OnRightDown(self,event):
        self.PopupMenu(ControlContextMenu(self), event.GetPosition())
    def Update(self, input_type='cc', address=[0,0], value=0):
        self.SetValue(value)
    def OnScrolled(self, event):
        #self.parent.OnMessage(self.getMessage())
        wx.PostEvent(self, InternalMessage(self, self.GetValue()))
    def SetInput(self, input_type='CC', address=[0,0], option = None):
        wx.PostEvent(self, MessageRecord(self, self.FaderId, input_type, address, option))
    def UnSetInput(self, input_type='CC', address=[0,0], option = None):
        wx.PostEvent(self, MessageUnRecord(self, self.FaderId, input_type, address, option))
    def GetMessage(self, event):
        print("Message")
        print event.GetType()
        print event.GetAddress()
    def GetInputs(self):
        wx.PostEvent(self, MessageGet(self))
    def WidgetUpdate(self, event):
        self.SetValue(event.GetValue())
class wxCrossFader(wxFader):
    def __init__(self, *args, **kwargs):
        wxFader.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)

class wxKnob(KnobCtrl):
    def __init__(self, parent, id=-1, size=(20, 20)):
        #KnobCtrl.__init__(self, *args, **kwargs)
        KnobCtrl.__init__(self, parent, id, size)
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
        self.pianoroll=wxPianoRoll(parent=self, id=ID_PIANO_ROLL)
        hbox1.Add(self.pianoroll, proportion=1, flag=wx.EXPAND|wx.ALL)
        vbox.Add(hbox1, proportion=3, flag=wx.EXPAND)
        self.SetSizer(vbox)
    def GetInputs(self):
        return self.pianoroll.GetInputs()
    def Update(self, input_type='Note', address=[0,0], value=0):
        self.pianoroll.Update(input_type, address, value)
    def getMessage(self):
        print("piano getmessage")
        
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
        self.DefaultMidiChannel=1
        self.FirstMidiNote=12
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
        midichannel = self.DefaultMidiChannel
        for i in range((self.octaves * 12) + self.after_notes):
            octave = int(math.floor (i/12))
            note = i % 12
            midinote = i + self.FirstMidiNote
            if 'w' == self.octave_notes[i % len(self.octave_notes)]:
                noteid = wx.NewId()
                whitenote = wxWhitePianoNote(self, noteid, octave, note)
                whitenote.SetInput(input_type = 'Note', address = [midichannel,midinote,i])
                self.Notes.append(whitenote)
            elif 'b' == self.octave_notes[i % len(self.octave_notes)]:
                noteid = wx.NewId()
                blacknote = wxBlackPianoNote(self, noteid, octave, note)
                blacknote.SetInput(input_type = 'Note', address = [midichannel,midinote,i])
                self.Notes.append(blacknote)
        self.DrawOctaves(dc)

    def GetNotesToDraw(self):
        last_note_on_screen = (self.octaves_on_screen * 12) + self.after_notes_on_screen
        return range(self.first_note_on_screen,last_note_on_screen)

    def DrawOctaves(self, dc):
        notes_to_draw = self.GetNotesToDraw()
        notes_on_screen = len(notes_to_draw)
        dc.RemoveAll()
        dc.BeginDrawing()
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
        #print note_octave
        note_octave_pos = int(math.floor((note_octave * 7 * note_w) + (note_pos * note_w)))
                

        note_point = wx.Point(note_octave_pos,0)
        note_size  = wx.Size (note_w, note_h)
        dc.SetId(note_id)

        self.Notes[note].UpdateDC(dc, note_point, note_size)
        note_coord = self.Notes[note].GetPos()
        note_x = note_coord[0]
        note_y = note_coord[1]
        #print("Coord: %i %i" % (note_x,note_y))
        note_size = self.Notes[note].GetSize()
        note_height = note_size.GetHeight()
        note_width = note_size.GetWidth()
        #print("Size : %i %i" % (note_width, note_height))
        note_rect  = wx.Rect (note_x, note_y, note_width, note_height)        
        dc.SetIdBounds(note_id, note_rect)
        #print dc.GetLen()
        #print dc.GetIdBounds(note_id)

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
        #l = self.pDC.FindObjects(x, y, hitradius)
        l = self.pDC.FindObjectsByBBox(x, y)
        if l:
            first_note_detected = l[0]
            num_note = self.SearchNoteId(first_note_detected)
            return num_note
        else:
            return None
    def OnRightDown(self,event):
        note = self.FindNote(event)
        if not note == None:
            self.Notes[note].OnRightDown(event)
    def OnLeftDown(self,event):
        note = self.FindNote(event)
        if not note == None:
            self.NoteOn(note, True)
    def OnLeftUp(self,event):
        note = self.FindNote(event)
        if not note == None:
            self.NoteOff(note, True)
    def NoteOn(self, note, play):
        self.Notes[note].NoteOn(play)
        self.DrawOctaves(self.pDC)
        self.Refresh()
    def NoteOff(self, note, play):
        self.Notes[note].NoteOff(play)
        self.DrawOctaves(self.pDC)
        self.Refresh()

    def GetInputs(self):
        inputs=dict()
        for n in self.Notes:
            #print n.GetInputs()
            for k,v in n.GetInputs().iteritems():
                #print i
                if inputs.has_key(k):
                    inputs[k] = v+inputs[k]
                else:
                    inputs[k] = v
        #print inputs
        return inputs
            
    def Update(self, input_type='Note', address=[0,0], value=0):
        if len(address) > 2:
            num_note = address[2]
            note = self.Notes[num_note]
            note.Update(input_type, address, value)
            self.DrawOctaves(self.pDC)
            self.Refresh()

class wxPianoNote(wx.PyEvtHandler):
    def __init__(self, parent, Id, octave, note):
        wx.PyEvtHandler.__init__(self)
        self.Id = Id
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
        return self.Id
    def SetControl(self):
        print("Set Control Event Note")
    def UpdateDC(self, paint, pos, size):
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
    def Update(self, input_type='Note', address=[0,0], value=0):
        if value == 0:
            self.NoteOff(False)
        else:
            self.NoteOn(False)
    def SetInput(self, input_type='CC', address=[0,0], option = None):
        wx.PostEvent(self, MessageRecord(self, self.Id, input_type, address, option))
    def GetInputs(self):
        wx.PostEvent(self, MessageGet(self))
class wxWhitePianoNote(wxPianoNote):
    def __init__(self, parent, ID, octave, note):
        wxPianoNote.__init__(self, parent, ID, octave, note)
    def UpdateDC(self, paint, pos, size):
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
    def UpdateDC(self, paint, pos, size):
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

class wxClock(wx.Panel):
    def __init__(self, parent, Id, signature=[4,4], beats_per_bar=4, ticks_per_beat = 24):
        self.parent = parent
        wx.Panel.__init__(self, parent)
        self.BeatsLights = []
        self.BeatsPerBar = beats_per_bar
        self.Beat = 0
        self.TickPerBeat = ticks_per_beat
        self.Tick = 0
        self.stopped = 0
        self.InitUI()
        self.InitClock()
                #Clock Raw Data
        #clock tick     = 248(10) F8(16)
        #clock stop     = 252(10) FC(16)
        #clock start    = 250(10) FA(16)
        #clock continue = 251(10) FB(16)

    def InitUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        for b in range(self.BeatsPerBar):
            ID_N = wx.NewId()
            light = wx.Panel(self, ID_N, size=wx.Size(10,10))
            light.SetBackgroundColour(wx.Colour(10, b * 50, 120))
            self.BeatsLights.append(light)
            hbox.Add(light, 0, wx.ALL, 2)
        self.SetSizer(hbox)
    def InitClock(self):
        self.SetInput('Clock',['0xf8'])
    def Update(self, input_type='Clock', address=248, value=1):
        if address == 248 and not self.stopped:
            self.AddTick()
        elif address == 252:
            self.stopped = 1
        elif address == 250:
            self.stopped = 0
            self.Beat = 0
            self.Tick = 0
            for b in self.BeatsLights:
                b.SetBackgroundColour('BLACK')
            self.BeatsLights[0].SetBackgroundColour('GREEN')
        elif address == 251:
            self.stopped = 0
    def AddTick(self):
        self.Tick += 1
        if self.Tick >= self.TickPerBeat:
            self.Tick = 0
            self.AddBeat()
    def AddBeat(self):
        self.BeatsLights[self.Beat].SetBackgroundColour('BLACK')
        self.Beat += 1
        if self.Beat >= len(self.BeatsLights):
            self.Beat = 0
        self.BeatsLights[self.Beat].SetBackgroundColour('GREEN')
    def SetInput(self, input_type='CC', address=[0,0], option = None):
        wx.PostEvent(self, MessageRecord(self, self.Id, input_type, address, option))
    def GetInputs(self):
        wx.PostEvent(self, MessageGet(self))
