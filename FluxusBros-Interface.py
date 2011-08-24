#!/usr/bin/python

from os import popen
import wx
import re
import rtmidi
from MidiConnectionsRtMidi import Connections
from MessageDispatch import *
from ClockGui import ClockControl
from MediaGui import MediaPanel
from TableGui import TablePanel
from SequencerGui import SequencerPanel
from configobj import ConfigObj

APP_SIZE_X = 900
APP_SIZE_Y = 400

FluxusInClient = "FluxusMidi Input Client"
FluxusInPort = "FluxusMidi Input Client:0"
MicroKontrol_Out_Client = "microKontrol"
MicroKontrol_Out_Port = "microKONTROL:1"
VirtualKeyboard_Port = "Virtual Keyboard:0"
Kmidimon_Port = "KMidimon:0"
NanoKontrolPort = "nanoKONTROL:0"
LMMSPort = "LMMS:1"

INMIDIPORT = [MicroKontrol_Out_Port , VirtualKeyboard_Port , NanoKontrolPort]
OUTMIDIPORT = [FluxusInPort , Kmidimon_Port, LMMSPort]

DEFAULT_PLAYERS = ["Korg" , "VMXVJ" , "BitStream"]

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        self.cfg = ConfigObj("./config.cfg")
        
        self.InitConfig(parent, ID, title)
        
        self.Dispatch = MessageDispatchRules(self)
        #~ self.Dispatch = MessageDispatch(self)
        
        EVT_WIDGET_MESSAGE_RECORD(self, self.Dispatch.AddInMessage)
        EVT_WIDGET_MESSAGE_UNRECORD(self, self.Dispatch.DelInMessage)
        EVT_WIDGET_MESSAGE_GET(self, self.Dispatch.GetInMessage)
        EVT_WIDGET_MESSAGE_UPDATE(self, self.Dispatch.InternalMessage)
        EVT_EXTERNAL_MIDI_IN_MESSAGE(self, self.Dispatch.ExternalMidiInMessage)
        EVT_EXTERNAL_MIDI_OUT_MESSAGE(self, self.MidiOutputRefresh)
        
        EVT_WIDGET_SEQUENCER_RECORD(self, self.Dispatch.AddSequencer)
        EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.Dispatch.AddSequence)
        EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.Dispatch.DelSequence)
        
        
    def InitConfig(self, parent, ID, title):
        if 'App' in self.cfg:
            print("Config File")
            w , h = self.cfg['App'].as_int('width'), self.cfg['App'].as_int('height')
        else:
            print("Defaults")
            w, h = (APP_SIZE_X, APP_SIZE_Y)
            self.cfg['App'] = {}
            self.cfg['App']['width'] = w
            self.cfg['App']['height'] = h
            self.cfg.write()
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(w, h))
        if 'MidiPort' in self.cfg:
            inmidiport = self.cfg['MidiPort'].as_list('InPort')
            outmidiport = self.cfg['MidiPort'].as_list('OutPort')
        else:
            inmidiport = INMIDIPORT
            outmidiport = OUTMIDIPORT
            self.cfg['MidiPort']={}
            self.cfg['MidiPort']['InPort'] = inmidiport
            self.cfg['MidiPort']['OutPort'] = outmidiport
            self.cfg.write()
        self.InitMidi(inmidiport, outmidiport)
        if 'Players' in self.cfg:
            self.Players = self.cfg.as_list('Players')
        else:
            self.Players = DEFAULT_PLAYERS
            self.cfg['Players'] = self.Players
            self.cfg.write()
        if 'DefaultPlayer' in self.cfg:
            self.DefaultPlayer = self.cfg['DefaultPlayer']
        else:
            self.DefaultPlayer = self.cfg.as_list('Players')[1]
            self.cfg['DefaultPlayer'] = self.DefaultPlayer
            self.cfg.write()
        self.InitPanels()
    def InitMidi(self, inmidi=[], outmidi=[]):
        self.MidiConnect = Connections(self.MidiInputRefresh, inmidi, outmidi)
    def MidiInputRefresh(self, midi_data):
        wx.PostEvent(self, ExternalMidiInMessage(midi_data))
    def MidiOutputRefresh(self, event):
        self.MidiConnect.sendMessage(event.GetMidiMessage())
    def InitPanels(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        toolbar = self.InitToolBar()
        vbox.Add(toolbar, 0, wx.EXPAND)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.Media = MediaPanel(self)
        self.Table = TablePanel(self)
        self.Sequencer = SequencerPanel(self)
        hbox.Add(self.Media, proportion = 0, flag=wx.EXPAND)
        hbox.Add(self.Table, proportion = 2, flag=wx.EXPAND)
        hbox.Add(self.Sequencer, proportion = 1, flag=wx.EXPAND)
        vbox.Add(hbox, proportion=-1, flag=wx.EXPAND)
        self.SetSizer(vbox)
        #~ EVT_WIDGET_SEQUENCER_MESSAGE_RECORD(self, self.Sequencer.InitSequence)
        #~ EVT_WIDGET_SEQUENCER_MESSAGE_UNRECORD(self, self.Sequencer.DelSequence)
        
    def InitToolBar(self):
        toolbar = wx.ToolBar(self, -1)
        TOOL_ID = wx.NewId()
        TOOL_ID_COMBO = wx.NewId()
        combo = wx.ComboBox(toolbar, TOOL_ID_COMBO, choices = self.Players)
        combo.SetStringSelection(self.DefaultPlayer)
        toolbar.AddControl(combo)
        wx.EVT_COMBOBOX(self, TOOL_ID_COMBO, self.SetPlayer)
        Clock = ClockControl(toolbar, wx.NewId())
        toolbar.AddControl(Clock)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_OTHER, (16, 16))
        toolbar.AddSeparator()
        ToolbarPreferences = toolbar.AddLabelTool(-1, 'Preferences', bmp, shortHelp='Preferences')
        #~ self.Bind(wx.EVT_MENU, self.onPrint, printTool)
        toolbar.Realize()
        return toolbar
    def SetPlayer(self, event):
        print("New Player : %s" % event.GetEventObject().GetValue())
         
class MyApp(wx.App):
    def OnInit(self, *args, **kwargs):
        self.MainFrame = MyFrame(None, -1, "FluxusBros Interface")
        self.MainFrame.Show(True)
        self.SetTopWindow(self.MainFrame)
        return True

app = MyApp(0)
app.MainLoop()
