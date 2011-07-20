#!/usr/bin/python

from os import popen
import wx
import re
import rtmidi
from MidiConnectionsRtMidi import Connections
from MediaGui import MediaPanel
from TableGui import TablePanel
from SequencerGui import SequencerPanel

APP_SIZE_X = 500
APP_SIZE_Y = 200

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(APP_SIZE_X, APP_SIZE_Y))
        self.InputCC = []
        self.InputNote = []
        self.InputOSC = []

        self.InitMidi()
        self.InitPanels()
    def InitPanels(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.Media = MediaPanel(self)
        self.Table = TablePanel(self)
        self.Sequencer = SequencerPanel(self)
        hbox.Add(self.Media, flag=wx.EXPAND)
        hbox.Add(self.Table, flag=wx.EXPAND)
        hbox.Add(self.Sequencer, flag=wx.EXPAND)
        self.SetSizer(hbox)
    def InitMidi(self):
        self.MidiConnect = Connections(self.MidiInputRefresh)
    def MidiInputRefresh(self, data):
        wx.CallAfter(self.MidiInDispatch, data)
    def MidiOutputRefresh(self, data):
        wx.CallAfter(self.MidiOutDispatch, data)
    def MidiOutDispatch(self, data):
        print data
        for m in data:
            self.MidiConnect.sendMessage(m)
    def MidiDispatch(self, MidiData):
        if MidiData.isController():
            for C in self.InputCC:
                if MidiData.isForChannel(C[0][0]):
                    if MidiData.getControllerNumber() == C[0][1]:
                        C[1](value=MidiData.getControllerValue())
        elif MidiData.isNoteOnOrOff():
            for N in self.InputNote:
                if MidiData.isForChannel(N[0][0]):
                    if MidiData.getNoteNumber() == N[0][1]:
                        if MidiData.isNoteOn():
                            N[1](value=MidiData.getControllerValue())
                        else:
                            N[1](value=0)
    def SetControls(self, Callback, Inputs):
        for CCin in Inputs['CC']:
            self.InputCC.append([CCin, Callback])
        for Notein in Inputs['Note']:
            self.InputNote.append([Notein, Callback])
        for OSCin in Inputs['OSC']:
            self.InputOSC.append([OSCin, Callback])
    def SetPlayer(self, event):
        print("New Player : %s" % event.GetEventObject().GetValue())
         
class MyApp(wx.App):
    def OnInit(self, *args, **kwargs):
        self.MainFrame = MyFrame(None, -1, "Midi Router/Sequencer")
        self.MainFrame.Show(True)
        self.SetTopWindow(self.MainFrame)
        return True

app = MyApp(0)
app.MainLoop()
