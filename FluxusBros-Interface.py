#!/usr/bin/python

from os import popen
import wx
import re
import rtmidi
from MidiConnectionsRtMidi import Connections
from TableGui import TablePanel

APP_SIZE_X = 300
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
        self.Table = TablePanel(self)
    def InitMidi(self):
        self.MidiConnect = Connections(self.MidiRefresh)
    def MidiRefresh(self, data):
        wx.CallAfter(self.MidiDispatch, data)
    def MidiDispatch(self, MidiData):
        if MidiData.isController():
            for C in self.InputCC:
                if MidiData.isForChannel(C[0][0]):
                    if MidiData.getControllerNumber() == C[0][1]:
                        C[1](MidiData.getControllerValue())
        elif MidiData.isNoteOnOrOff():
            for N in self.InputNote:
                if MidiData.isForChannel(N[0][0]):
                    if MidiData.getNoteNumber() == N[0][1]:
                        if MidiData.isNoteOn():
                            N[1](MidiData.getControllerValue())
                        else:
                            N[1](0)
    def SetControls(self, Callback, Inputs):
        for CCin in Inputs['CC']:
            self.InputCC.append([CCin, Callback])
        for Notein in Inputs['Note']:
            self.InputNote.append([Notein, Callback])
        for OSCin in Inputs['OSC']:
            self.InputOSC.append([OSCin, Callback])
        
         
class MyApp(wx.App):
    def OnInit(self, *args, **kwargs):
        self.MainFrame = MyFrame(None, -1, "Midi Router/Sequencer")
        self.MainFrame.Show(True)
        self.SetTopWindow(self.MainFrame)
        return True

app = MyApp(0)
app.MainLoop()
