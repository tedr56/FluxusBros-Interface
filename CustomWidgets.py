import wx
from wx.lib.agw.knobctrl import *
from MessageDispatch import *
import rtmidi
import time
from threading import Thread
import MidiVars
import os
import os.path
from configobj import ConfigObj
from math import pi, sqrt
from math import copysign
import re
import sys
sys.path.append('Knob')
import SpeedMeter as SM

#~ class Control(wx.PyEvtHandler):
    #~ def __init__(self, parent):
        #~ wx.PyEvtHandler.__init__(self)
        #~ self.parent = parent
        #~ self.Id = wx.NewId()
        #~ EVT_WIDGET_MESSAGE(self, self.GetInputEvent)
        #~ EVT_WIDGET_UPDATE(self, self.Update)
        #~ EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.RecordEvent)
        #~ EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.UnRecordEvent)
    #~ def GetId(self):
        #~ return self.Id
    #~ def SetInput(self, Type, Address, Option=None):
        #~ wx.PostEvent(self, MessageRecord(self, self.Id, Type, Address, Option))
    #~ def UnSetInput(self, Type, Address, Option=None):
        #~ wx.PostEvent(self, MessageUnRecord(self, self.Id, Type, Address, Option))
    #~ def SetRecord(self):
        #~ wx.PostEvent(self, MessageSequencerRecord(self, self.parent.GetValue()))
    #~ def UnSetRecord(self):
        #~ wx.PostEvent(self, MessageSequencerUnRecord(self))
    #~ def GetInputEvent(self):
        #~ print("Control Input Message Infos")
        #~ print event.GetType()
        #~ print event.GetAddress()
    #~ def Update(self, event):
        #~ self.parent.SetValue(event.GetValue())
    #~ def WidgetUpdate(self, event):
        #~ wx.PostEvent(self, InternalMessage(self, evnt.GetValue()))
    #~ def RecordEvent(self, event):
        #~ self.parent.SetRecording()
    #~ def UnRecordEvent(self, event):
        #~ self.parent.SetUnRecording()
    #~ def Context(self, event):
        #~ self.PopupMenu(ControlContextMenu(self), event.GetPosition())
    
class ControlContextMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent
        SetControl = wx.MenuItem(self, wx.NewId(), 'Set Control')
        self.AppendItem(SetControl)
        self.Bind(wx.EVT_MENU, self.OnSetControl, id=SetControl.GetId())

    def OnSetControl(self, event):
        #~ self.parent.SetControl()
        ControlMessage = wxControlSettings(self.parent)
        ControlMessage.ShowModal()
        ControlMessage.Destroy()
    def GetParent(self):
        return self.parent

class wxControlSettings(wx.Dialog):
    def __init__(self, control):
        wx.Dialog.__init__(self, None, -1, 'Control Settings')
        self.control = control
        self.controlId = control.GetId()
        #~ control.panel = wx.Panel(self, -1)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        EVT_WIDGET_MESSAGE(self, self.GetMessage)
        self.GetInputs()
    def GetMessage(self, event):
        print("GetInputMessage")
        self.InitLine(event)
    def GetInputs(self):
        wx.PostEvent(self, MessageGet(self.control, Source=self))
    def InitLine(self, Input):
        hbox = BoxSizer(wx.HORIZONTAL)
        TypeCombo = wx.ComboBox(self, -1, choices=["Midi CC", "Midi Note", "OSC"])
        hbox.Add(TypeCombo)
        self.vbox.Add(hbox)
        
class wxFader(wx.Panel):
    def __init__(self):
        pre = wx.PrePanel()
        self.PostCreate(pre)
        #~ self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        
    #~ def OnCreate(self, event):
    def Create(self, parent, Id, pos, size, style):
        wx.Panel.Create(self, parent, Id, pos, size, style)
        self.parent = parent
        self.Unbind(wx.EVT_WINDOW_CREATE)
        #~ event.skip()
        #~ wx.Panel.__init__(self, *args, **kwargs)
        box = wx.BoxSizer()
        self.Fader = wxFaderWidget(self)
        box.Add(self.Fader, proportion=1, flag = wx.EXPAND)
        self.SetSizer(box)
        #~ self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)

    def SetInput(self, *args,  **kwargs):
        self.Fader.SetInput(*args,  **kwargs)
    def UnSetInput(self, *args,  **kwargs):
        self.Fader.UnSetInput(*args,  **kwargs)
    def SetRecord(self):
        self.SetBackgroundColour('YELLOW')
    def UnSetRecord(self):
        #~ self.SetBackgroundColour(self.InitialBackground)
        #~ self.SetBackgroundStyle(self.InitialBackgroundStyle)
        #~ self.SetWindowStyle(self.InitialWindowStyle)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
    def OnDestroy(self, event):
        #~ event.Skip()
        print("wxFader Destroy")
        #~ self.Fader.OnDestroy(event)
        
class wxKnobF(wxFader):
    def __init__(self):
        wxFader.__init__(self)
    def Create(self, parent, id, pos, size, style):
        wxFader.Create(self, parent, id, pos, size, style)

class wxCrossFader(wxFader):
    def __init__(self, *args, **kwargs):
        wxFader.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)

        
class wxFaderWidget(wx.Slider):
    def __init__(self, *args,  **kwargs):
        wx.Slider.__init__(self, *args, id=wx.NewId(), style = wx.SL_AUTOTICKS |  wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        self.parent = args[0]
        self.SetRange(0, 127)
        self.SeqRecord = False
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.OnScrolled)
        EVT_WIDGET_MESSAGE(self, self.GetMessage)
        EVT_WIDGET_UPDATE(self, self.WidgetUpdate)
        EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.RecordEvent)
        EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.UnRecordEvent)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
    def UnRecordEvent(self, event):
        if self.SeqRecord:
            self.UnRecord()
    def RecordEvent(self, event):
        if not self.SeqRecord:
            self.Record()
    def GetRecording(self):
        return self.SeqRecord
    def Record(self):
        self.GetParent().SetRecord()
        self.SeqRecord = True
    def UnRecord(self):
        self.GetParent().UnSetRecord()
        self.SeqRecord = False
    def OnRightDown(self,event):
        self.PopupMenu(ControlContextMenu(self), event.GetPosition())
    #~ def GetOptions(self):
        
    def OnMiddleDown(self, event):
        #~ print self.GetParent()
        if self.SeqRecord:
            wx.PostEvent(self.parent, MessageSequencerUnRecord(self))
            self.UnRecord()
        else:
            wx.PostEvent(self.parent, MessageSequencerRecord(self, self.GetValue()))
            self.Record()
    def OnScrolled(self, event):
        wx.PostEvent(self, InternalMessage(self, self.GetValue()))
    def SetInput(self, input_type='CC', address=[0,0], option = None):
        wx.PostEvent(self, MessageRecord(self, self.GetId(), input_type, address, option))
    def UnSetInput(self, input_type=None, address=None, option = None):
        #~ wx.PostEvent(self, MessageUnRecord(self, self.GetId(), input_type, address, option))
        self.GetParent().GetEventHandler().ProcessEvent(MessageUnRecord(self, self.GetId(), input_type, address, option))
    def GetMessage(self, event):
        print("Message")
        print event.GetType()
        print event.GetAddress()
    def GetInputs(self):
        wx.PostEvent(self, MessageGet(self))
    def WidgetUpdate(self, event):
        self.SetValue(event.GetValue())
    def OnDestroy(self,event):
        print("wxFaderWidget Destroy")
        self.UnSetInput()
        event.Skip()
        
#~ class wxFaderWidget2(wx.Slider):
    #~ def __init__(self, *args,  **kwargs):
        #~ wx.Slider.__init__(self, *args, style = wx.SL_AUTOTICKS |  wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_INVERSE, **kwargs)
        #~ self.SetRange(0, 127)
        #~ self.SeqRecord = False
        #~ self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        #~ self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        #~ self.Bind(wx.EVT_COMMAND_SCROLL, self.OnScrolled)
        #~ self.control = Control(self)
    #~ def OnRightDown(self, event):
        #~ self.control.WidgetUpdate(event)
    #~ def OnMiddleDown(self, event):
        #~ if self.SeqRecord:
            #~ self.control.UnRecord()
        #~ else:
            #~ self.control.Record()
    #~ def SetRecording(self):
        #~ self.SeqRecord = True
        #~ self.GetParent().SetRecord()
    #~ def UnSetRecording(self):
        #~ self.SeqRecord = False
        #~ self.GetParent().UnSetRecord()

class wxKnob(wx.Panel):
    def __init__(self):
        pre = wx.PrePanel()
        self.PostCreate(pre)
        #~ self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        #~ def OnCreate(self, event):

    def Create(self, parent, Id, pos, size, style):
        wx.Panel.Create(self, parent, Id, pos) #, wx.Size(50,50), style)
        self.knobTxt = wx.StaticText(self)
        self.knob = wxKnobWidget(self,
                            extrastyle=
                            SM.SM_DRAW_HAND |
                            SM.SM_DRAW_PARTIAL_FILLER
                            ,
                            mousestyle=1
                            )
        self.parent = parent
        self.knob.SetAngleRange(-pi/6, 7*pi/6)
        intervals = range(0, 128)
        self.knob.SetIntervals(intervals)
        colours = [wx.BLACK]*127
        self.knob.SetIntervalColours(colours)
        ticks = ["" for interval in intervals]

        self.knob.SetTicks(ticks)
        self.knob.SetHandColour(wx.BLACK)
        self.knob.DrawExternalArc(False)
        self.knob.SetMinSize(wx.Size(50,50))
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.knobTxt, 0, wx.CENTER)
        box.Add(self.knob, 1, wx.EXPAND)
        self.SetSizer(box)
        self.SeqRecord = False
        self.knob.Bind(wx.EVT_MOUSEWHEEL, self.OnAngleChanged)
        self.knob.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        EVT_WIDGET_UPDATE(self, self.WidgetUpdate)
        EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.RecordEvent)
        EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.UnRecordEvent)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
    def SetValue(self, v):
        self.knob.SetSpeedValue(v)
    def GetValue(self):
        return int(self.knob.GetSpeedValue())
    def UnRecordEvent(self, event):
        if self.SeqRecord:
            self.UnRecord()
    def RecordEvent(self, event):
        if not self.SeqRecord:
            self.Record()
    def GetRecording(self):
        return self.SeqRecord
    def Record(self):
        self.SeqRecord = True
        self.knob.SetSpeedBackground("YELLOW")
        self.Layout()
    def UnRecord(self):
        self.SeqRecord = False
        self.knob.SetSpeedBackground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
        self.Layout()
    def OnMiddleDown(self, event):
        if self.SeqRecord:
            wx.PostEvent(self.parent, MessageSequencerUnRecord(self))
            self.UnRecord()
        else:
            wx.PostEvent(self.parent, MessageSequencerRecord(self, self.GetValue()))
            self.Record()
    def OnAngleChanged(self, event):
        wheel = copysign(1, event.GetWheelRotation())
        new_value = self.GetValue() + wheel
        self.SetValue(new_value)
    def OnValueChange(self, value):
        self.SetLabel(value)
        wx.PostEvent(self, InternalMessage(self, value))
    def SetLabel(self, msg):
        self.knobTxt.SetLabel(str(msg))
    def SetInput(self, input_type="CC", address=[0,0], option = None):
        wx.PostEvent(self, MessageRecord(self, self.GetId(), input_type, address, option))
    def UnSetInput(self, input_type=None, address=None, option = None):
        #~ wx.PostEvent(self, MessageUnRecord(self, self.GetId(), input_type, address, option))
        self.GetParent().GetEventHandler().ProcessEvent(MessageUnRecord(self, self.GetId(), input_type, address, option))
    def WidgetUpdate(self, event):
        self.knob.SetSpeedValueNoEvent(event.GetValue())
    def DrawTags(self, dc, size):
        None
    def OnDestroy(self,event):
        print("wxKnob Destroy")
        self.UnSetInput()
        event.Skip()

class wxKnobWidget(SM.SpeedMeter):
    def __init__(self, *args, **kwargs):
        self.parent = args[0]
        SM.SpeedMeter.__init__(self, *args, **kwargs)
    def SetSpeedValue(self, value = 0):
        SM.SpeedMeter.SetSpeedValue(self, value)
        self.parent.OnValueChange(int(value))
    def SetSpeedValueNoEvent(self, value = 0):
        SM.SpeedMeter.SetSpeedValue(self, value)
        self.parent.SetLabel(int(value))
        
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
        self.octaves_on_screen = 3
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
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)

    def InitNotes(self, dc):
        midichannel = self.DefaultMidiChannel
        for i in range((self.octaves * 12) + self.after_notes):
            octave = int(math.floor (i/12))
            note = i % 12
            midinote = i + self.FirstMidiNote
            if 'w' == self.octave_notes[i % len(self.octave_notes)]:
                noteid = wx.NewId()
                whitenote = wxWhitePianoNote(self, noteid, octave, note)
                whitenote.SetInput(input_type = 'Note', address = [midichannel,midinote])
                self.Notes.append(whitenote)
            elif 'b' == self.octave_notes[i % len(self.octave_notes)]:
                noteid = wx.NewId()
                blacknote = wxBlackPianoNote(self, noteid, octave, note)
                blacknote.SetInput(input_type = 'Note', address = [midichannel,midinote])
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
        notes = (self.octaves_on_screen * 7) + self.after_notes_on_screen
        w, h = self.GetSize()
        note_h = h
        note_w = int(round(w / notes))
        
        note_id = self.Notes[note].GetId()
        
        note_start =self.first_note_on_screen
        note_offset = self.Notes[note_start]
        note_pos = self.octave_notes_pos[note % 12]
        note_octave = int(math.floor(num_note/12))
        note_octave_pos = int(math.floor((note_octave * 7 * note_w) + (note_pos * note_w)))
                

        note_point = wx.Point(note_octave_pos,0)
        note_size  = wx.Size (note_w, note_h)
        dc.SetId(note_id)

        self.Notes[note].UpdateDC(dc, note_point, note_size)
        note_coord = self.Notes[note].GetPos()
        note_x = note_coord[0]
        note_y = note_coord[1]
        note_size = self.Notes[note].GetSize()
        note_height = note_size.GetHeight()
        note_width = note_size.GetWidth()
        note_rect  = wx.Rect (note_x, note_y, note_width, note_height)        
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
        self.Update()
        
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
        else:
            return None
    def OnMiddleDown(self, event):
        note = self.FindNote(event)
        if not note == None:
            self.Notes[note].OnMiddleDown(event)
    def OnRightDown(self,event):
        note = self.FindNote(event)
        if not note == None:
            self.Notes[note].OnRightDown(event)
    def OnLeftDown(self,event):
        note = self.FindNote(event)
        if not note == None:
            self.NoteOn(note)
    def OnLeftUp(self,event):
        note = self.FindNote(event)
        if not note == None:
            self.NoteOff(note)
    def NoteOn(self, note):
        self.Notes[note].NoteOn()
        self.Update()
    def NoteOff(self, note):
        self.Notes[note].NoteOff()
        self.Update()

    def Update(self):
        self.DrawOctaves(self.pDC)
        self.Refresh()
    def OnDestroy(self, event):
        event.Skip()
        print("PianoRoll destroy")
        for i in self.Notes:
            self.GetParent().GetEventHandler().ProcessEvent(MessageUnRecord(i, i.GetId(), None, None, None))
            i.Destroy()
        del self.Notes
        

class wxPianoNote(wx.PyEvtHandler):
    def __init__(self, parent, Id, octave, note):
        wx.PyEvtHandler.__init__(self)
        self.Id = Id
        self.parent = parent
        self.notelist = ["C", "C#" , "D" , "D#" , "E" , "F" , "F#" , "G" , "G#" , "A" , "A#" , "B"]
        self.size = wx.Size(0,0)
        self.pos = wx.Point(0,0)
        self.Value = 0
        self.SeqRecord = False
        EVT_WIDGET_MESSAGE(self, self.GetMessage)
        EVT_WIDGET_UPDATE(self, self.Update)
        EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.RecordEvent)
        EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.UnRecordEvent)
    def UnRecordEvent(self, event):
        if self.SeqRecord:
            self.UnRecord()
    def RecordEvent(self, event):
        if not self.SeqRecord:
            self.Record()
    def GetRecording(self):
        return self.SeqRecord
    def Record(self):
        self.SeqRecord = True
    def UnRecord(self):
        self.SeqRecord = False
    def OnMiddleDown(self, event):
        if self.SeqRecord:
            wx.PostEvent(self.parent, MessageSequencerUnRecord(self))
            self.UnRecord()
        else:
            wx.PostEvent(self.parent, MessageSequencerRecord(self, self.GetValue()))
            self.Record()
    def GetId(self):
        return self.Id
    def GetParent(self):
        return self.parent
    def GetPos(self):
        return self.pos
    def GetSize(self):
        return self.size
    def GetValue(self):
        return self.Value
    def UpdateDC(self, paint, pos, size):
        self.DrawNote(paint)
    def DrawNote(self, paint):
        paint.DrawRectanglePointSize(self.pos,self.size)
    def OnRightDown(self,event):
        event.GetEventObject().PopupMenu(ControlContextMenu(self), event.GetPosition())
    def SetControl(self):
        print("Set Control Event Note")
    def NoteOn(self, value=64, play=True):  #Parametre play a True => Send Midi Message Note On
        self.Value = value
        if play:
            wx.PostEvent(self.parent, InternalMessage(self, value))
    def NoteOff(self, play=True):  #Parametre play a True => Send Midi Message Note Off
        self.Value = 0
        if play:
            wx.PostEvent(self.parent, InternalMessage(self, 0))
    def Update(self, event):
        value = event.GetValue()
        if value:
            self.NoteOn(value, False)
        else:
            self.NoteOff(False)
        self.parent.Update()
    def SetInput(self, input_type='CC', address=[0,0], option = None):
        wx.PostEvent(self.parent, MessageRecord(self, self.Id, input_type, address, option))
    def UnSetInput(self, input_type=None, address=None, option = None):
        self.GetParent().ProcessEvent(MessageUnRecord(self, self.Id, input_type, address, option))
    def GetInputs(self):
        wx.PostEvent(self, MessageGet(self))
    def GetMessage(self, event):
        print("Input")
        print event.GetType()
        print event.GetAddress()
        
class wxWhitePianoNote(wxPianoNote):
    def __init__(self, parent, ID, octave, note):
        wxPianoNote.__init__(self, parent, ID, octave, note)
    def UpdateDC(self, paint, pos, size):
        self.size = size
        self.pos = pos
        paint.SetPen(wx.Pen('BLACK'))
        if self.Value:
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
        if self.Value:
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
        EVT_WIDGET_UPDATE(self, self.Update)
        self.BeatsLights = []
        self.BeatsPerBar = beats_per_bar
        self.Beat = 0
        self.TickPerBeat = ticks_per_beat
        self.Tick = 0
        self.stopped = 0
        self.InitUI()
        self.InitClock()
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
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
        self.SetInput('Clock', 248)
        self.SetInput('Clock', 252)
        self.SetInput('Clock', 250)
    def Update(self, event):
        address = event.GetAddress()
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
        wx.PostEvent(self.parent, MessageRecord(self, self.Id, input_type, address, option))
    def UnSetInput(self, input_type=None, address=None, option = None):
        wx.PostEvent(self.parent, MessageUnRecord(self, self.Id, input_type, address, option))
    def GetInputs(self):
        wx.PostEvent(self, MessageGet(self))
    def OnDestroy(self, event):
        event.Skip()
        print("Clock Destroy")
        self.UnSetInput()
    def GetRecording(self):
        return False

class InternalClock(wx.PyEvtHandler, Thread):
    def __init__(self, parent, Id=wx.NewId()):
        wx.PyEvtHandler.__init__(self)
        Thread.__init__(self)
        self.parent = parent
        self.Id = Id
        print("InternalClock")
        self.SetBpm(120)
        print("Bpm:%i" % self.bpm)
        self.KeepGoing = True
        
        EVT_WIDGET_UPDATE(self, self.WidgetUpdate)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        wx.PostEvent(self.parent, MessageRecord(self, self.Id, Type = 'Clock', Address = 248))
        self.start()
    def SetBpm(self, bpm):
        self.bpm = bpm
        self.dTime = bpm * 24.0
        self.dTick = 60 / self.dTime
    def run(self):
        print("Internal Clock Threading")
        while self.KeepGoing:
            wx.PostEvent(self.parent, InternalMessage(self, 1))
            time.sleep(self.dTick)
        self.ProcessEvent(MessageUnRecord(self, self.Id, Type = 'Clock', Address = 248))
        return None
    def WidgetUpdate(self, event):
        self.Stop()
    def Start(self):
        self.KeepGoing = True
        self.start()
    def Stop(self):
        self.KeepGoing = False
    def GetId(self):
        return self.Id
    def OnDestroy(self, event):
        event.Skip()
        print("InternalClock Destroy")
        self.Stop()
        
class SchemeFileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    def OnDropFiles(self, x, y, filenames):
        File = filenames[0]
        FileSplit = File.split('.')
        FileExtension = FileSplit[(len(FileSplit) - 1)]
        if FileExtension == "scm" or FileExtension == "SCM":
            VisuPath = os.path.dirname(File)
            cfg = ConfigObj("./config.cfg")
            FLUXUSBROS_DIRECTORY = cfg['App']['FluxusBros_Directory']
            FBVisuPath = os.path.join(FLUXUSBROS_DIRECTORY, "visus")
            VisuFileName = os.path.basename(File)
            FBVisuFilePath = os.path.join(FBVisuPath, VisuFileName)
            if not VisuPath == FBVisuPath:
                #~ Checking if the file is in the Visual files folder
                if not os.path.exists(FBVisuFilePath):
                    #~ Create the appropriate file in the Visual files folder
                    ExpFile = open(File, 'r')
                    ExpFileR = ExpFile.read()
                    RegFile = self.Brosserizer(ExpFileR)
                    FBVisuFile = open(FBVisuFilePath, 'w')
                    FBVisuFile.write(RegFile)
                    FBVisuFile.close()
                    ExpFile.close()
                #~ Checking if the control config file exists
                player = self.window.GetPlayerName()
                ControlConfigPath = os.path.join(FLUXUSBROS_DIRECTORY, "controls")
                VisuName = VisuFileName.split('.')[0]
                ControlFileName = VisuName + "." + player
                ControlConfigFilePath = os.path.join(ControlConfigPath, ControlFileName)
                if not os.path.exists(ControlConfigFilePath):
                    #~ Create an automatic control config file for the current player
                    ExpFile = open(File, 'r')
                    ConfigFile = open(ControlConfigFilePath, 'w')
                    lines = ExpFile.readlines()
                    pattern = '\((?P<ctype>(m|mn|f)+)(\s+)(?P<channel>\w+)(\s+)(?P<control>\w+)(\s+)(?P<coeff>[-+]?[0-9]*\.?[0-9]*?)(\s*)\'(?P<nom>[\w\_\-]+)(\)+)'
                    reg = re.compile(pattern)
                    print lines
                    WriteLine = lambda l : ConfigFile.write(l + "\n")
                    for l in lines:
                        res = reg.search(l)
                        if res:
                            WriteLine(VisuName)
                            WriteLine(player)
                            WriteLine(res.group("nom"))
                            ControlType = res.group("ctype")
                            if ControlType == "mn":
                                ControlType = "midi-ccn"
                            elif ControlType == "m":
                                ControlType = "midi-cc"
                            else:
                                ControlType = "fake"
                            WriteLine(ControlType)
                            Address = "(vector " + res.group("channel") + " " + res.group("control") + ")"
                            WriteLine(Address)
                            WriteLine("0")
                            WriteLine("-1")
                            WriteLine("0.8")
                            WriteLine("0.7")
                            WriteLine("0.3")
                            WriteLine("0.2")
                    ExpFile.close()
                    ConfigFile.close()
            self.window.SetVisual(File)
            self.window.Layout()
    def Brosserizer(self, txt):
        pattern = '\((m|mn)(\s+)(?P<channel>\w+)(\s+)(?P<control>\w+)(\s+)(?P<coeff>[-+]?[0-9]*\.?[0-9]*?)(\s*)\'(?P<nom>[\w\_\-]+)(\){1})'
        return re.sub(pattern, self.BrosserizerMatch, txt)
    def BrosserizerMatch(self, matching):
        coeff = matching.group("coeff")
        if coeff:
            return "(c \"" +  matching.group("nom") + "\" id " + "#:coeff " + coeff + ")"
        else:
            return "(c \"" +  matching.group("nom") + "\" id)"
        
        
class wxMediaVisual(wx.Panel):
    def __init__(self):
        pre = wx.PrePanel()
        self.PostCreate(pre)
    def Create(self, parent, Id, visual=None):
        wx.Panel.Create(self, parent, Id)
        self.parent = parent
        self.Visual = visual
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.addr = None
        if visual:
            self.InitVisual()
        else:
            self.BMP = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
            self.BTN = wx.BitmapButton(self, wx.ID_ANY, self.BMP)
            self.Sizer.Add(self.BTN, 1, wx.EXPAND)
        self.SetSizer(self.Sizer)
        SDT = SchemeFileDrop(self)
        self.SetDropTarget(SDT)
        self.SeqRecord = False
        self.BTN.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.BTN.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.BTN.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.BTN.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.BTN.Bind(wx.EVT_COMMAND_SCROLL, self.OnScrolled)
        EVT_WIDGET_MESSAGE(self, self.GetMessage)
        EVT_WIDGET_UPDATE(self, self.WidgetUpdate)
        EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.RecordEvent)
        EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.UnRecordEvent)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
    def InitVisual(self):
        self.wx.StaticText(self.Visual)
    def SetVisual(self, Visu):
        FilePath = os.path.split(Visu)
        Path = FilePath[0]
        File = FilePath[1]
        VisuName = os.path.splitext(File)[0]
        
        cfg = ConfigObj("./config.cfg")
        FLUXUSBROS_INTERFACE_DIRECTORY = cfg['App']['FluxusBros_Interface_Directory']
        ImageVisuName = VisuName + ".jpg"
        ImageFilePath = os.path.join(FLUXUSBROS_INTERFACE_DIRECTORY, "Preview", ImageVisuName)
        if os.path.exists(ImageFilePath):
            
            ImageVisu = wx.Image(ImageFilePath,wx.BITMAP_TYPE_JPEG)
            ImageVisu.Rescale(72,57)
            self.BTN.SetBitmapLabel(wx.BitmapFromImage(ImageVisu))
            self.BTN.SetToolTipString(VisuName)
            #~ self.parent.UpdateSizer()
            
            #~ self.Fit()
            self.parent.FitInside()
            self.parent.Layout()
        else:
            
            self.BMP = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16))
            self.BTN = wx.BitmapButton(self, wx.ID_ANY, self.BMP)
            self.BTN.SetToolTipString(VisuName)
            #~ self.Sizer.Add(self.BTN, 1, wx.EXPAND)
            self.FitInside()
            self.Layout()
            
    def UnRecordEvent(self, event):
        if self.SeqRecord:
            self.UnRecord()
    def RecordEvent(self, event):
        if not self.SeqRecord:
            self.Record()
    def GetRecording(self):
        return self.SeqRecord
    def Record(self):
        self.GetParent().SetRecord()
        self.SeqRecord = True
        self.SetBackgroundColour('YELLOW')
    def UnRecord(self):
        self.GetParent().UnSetRecord()
        self.SeqRecord = False
        self.SetBackgroundColour(self.InitialBackground)
        self.SetBackgroundStyle(self.InitialBackgroundStyle)
        self.SetWindowStyle(self.InitialWindowStyle)
    def OnRightDown(self,event):
        self.PopupMenu(ControlContextMenu(self), event.GetPosition())
    #~ def GetOptions(self):
        
    def OnMiddleDown(self, event):
        #~ print self.GetParent()
        if self.SeqRecord:
            wx.PostEvent(self.parent, MessageSequencerUnRecord(self))
            self.UnRecord()
        else:
            wx.PostEvent(self.parent, MessageSequencerRecord(self, self.GetValue()))
            self.Record()
    def OnLeftDown(self, event):
        wx.PostEvent(self.parent, InternalMessage(self, 127))
    def OnLeftUp(self, event):
        wx.PostEvent(self.parent, InternalMessage(self, 0))
    def OnScrolled(self, event):
        0
    def SetInput(self, input_type='CC', address=[0,0], option = None):
        self.addr = address
        wx.PostEvent(self.parent, MessageRecord(self, self.GetId(), input_type, address, option))
    def UnSetInput(self, input_type='CC', address=[0,0], option = None):
        #~ wx.PostEvent(self.parent, MessageUnRecord(self, self.GetId()))
        self.GetEventHandler().ProcessEvent(MessageUnRecord(self, self.GetId()))
    def GetMessage(self, event):
        print("Message")
        print event.GetType()
        print event.GetAddress()
    def GetInputs(self):
        wx.PostEvent(self, MessageGet(self))
    def WidgetUpdate(self, event):
        self.SetValue(event.GetValue())
    def OnDestroy(self, event):
        event.Skip()
        print("Media Destroy")
        self.UnSetInput()
    def GetPlayerName(self):
        return self.parent.GetParent().GetPlayerName()
