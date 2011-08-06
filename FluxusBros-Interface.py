#!/usr/bin/python

from os import popen
import wx
import re
import rtmidi
from MidiConnectionsRtMidi import Connections
from MessageDispatch import *
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

INMIDIPORT = [MicroKontrol_Out_Port , VirtualKeyboard_Port]
OUTMIDIPORT = [FluxusInPort , Kmidimon_Port]

DEFAULT_PLAYERS = ["Korg" , "VMXVJ" , "BitStream"]

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        self.cfg = ConfigObj("./config.cfg")
        self.InitConfig(parent, ID, title)
        self.Dispatch = MessageDispatchRules(self)
        EVT_WIDGET_MESSAGE_RECORD(self, self.Dispatch.AddInMessage)
        EVT_WIDGET_MESSAGE_UNRECORD(self, self.Dispatch.DelInMessage)
        EVT_WIDGET_MESSAGE_GET(self, self.Dispatch.GetInMessage)
        EVT_WIDGET_MESSAGE_UPDATE(self, self.Dispatch.InternalMessage)
        EVT_EXTERNAL_MIDI_IN_MESSAGE(self, self.Dispatch.ExternalMidiInMessage)
        EVT_EXTERNAL_MIDI_OUT_MESSAGE(self, self.MidiOutputRefresh)
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
        self.InitPanels(self.Players)
    def InitPanels(self, players=[]):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.Media = MediaPanel(self, players)
        self.Table = TablePanel(self)
        self.Sequencer = SequencerPanel(self)
        hbox.Add(self.Media, proportion = 0, flag=wx.EXPAND)
        hbox.Add(self.Table, proportion = 2, flag=wx.EXPAND)
        hbox.Add(self.Sequencer, proportion = 1, flag=wx.EXPAND)
        vbox.Add(hbox, proportion=-1, flag=wx.EXPAND)
        self.SetSizer(vbox)
    def InitMidi(self, inmidi=[], outmidi=[]):
        self.MidiConnect = Connections(self.MidiInputRefresh, inmidi, outmidi)
    def MidiInputRefresh(self, midi_data):
        wx.PostEvent(self, ExternalMidiInMessage(midi_data))
    def MidiOutputRefresh(self, event):
        self.MidiConnect.sendMessage(event.GetMidiMessage())
    def SetPlayer(self, player):
        print("New Player : %s" % player)
         
class MyApp(wx.App):
    def OnInit(self, *args, **kwargs):
        self.MainFrame = MyFrame(None, -1, "FluxusBros Interface")
        self.MainFrame.Show(True)
        self.SetTopWindow(self.MainFrame)
        return True

app = MyApp(0)
app.MainLoop()
