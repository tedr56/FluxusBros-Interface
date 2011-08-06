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
import ConfigParser

APP_SIZE_X = 900
APP_SIZE_Y = 400

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        self.InitConfig(parent, ID, title)
        self.Dispatch = MessageDispatchRules(self)
        EVT_WIDGET_MESSAGE_RECORD(self, self.Dispatch.AddInMessage)
        EVT_WIDGET_MESSAGE_UNRECORD(self, self.Dispatch.DelInMessage)
        EVT_WIDGET_MESSAGE_GET(self, self.Dispatch.GetInMessage)
        EVT_WIDGET_MESSAGE_UPDATE(self, self.Dispatch.InternalMessage)
        EVT_EXTERNAL_MIDI_IN_MESSAGE(self, self.Dispatch.ExternalMidiInMessage)
        EVT_EXTERNAL_MIDI_OUT_MESSAGE(self, self.MidiOutputRefresh)
        self.InitMidi()
        self.InitPanels()
    def InitConfig(self, parent, ID, title):
        self.cfg = ConfigParser.ConfigParser()
        f = "./config.cfg"
        self.cfg.read(f)
        if self.cfg.has_section('App'):
            print("Config File")
            w, h = self.cfg.getint('App', 'width'), self.cfg.getint('App', 'height')
        else:
            print("Default Config")
            w, h = (APP_SIZE_X, APP_SIZE_Y)
            self.cfg.add_section('App')
            self.cfg.set('App' , 'width', w)
            self.cfg.set('App' , 'height', h)
            self.cfg.write(open(f,"w"))
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(w, h))

        
    def InitPanels(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.Media = MediaPanel(self)
        self.Table = TablePanel(self)
        self.Sequencer = SequencerPanel(self)
        hbox.Add(self.Media, proportion = 0, flag=wx.EXPAND)
        hbox.Add(self.Table, proportion = 2, flag=wx.EXPAND)
        hbox.Add(self.Sequencer, proportion = 1, flag=wx.EXPAND)
        vbox.Add(hbox, proportion=-1, flag=wx.EXPAND)
        self.SetSizer(vbox)
    def InitMidi(self):
        self.MidiConnect = Connections(self.MidiInputRefresh)
    def MidiInputRefresh(self, midi_data):
        wx.PostEvent(self, ExternalMidiInMessage(midi_data))
    def MidiOutputRefresh(self, event):
        self.MidiConnect.sendMessage(event.GetMidiMessage())
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
